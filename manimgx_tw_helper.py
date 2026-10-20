"""台灣繁體中文數學幾何動畫 ManimGX 核心輔助模組 (manimgx_tw_helper.py).

整合功能：
1. 台灣雲哲 (zh-TW-YunJheNeural) Edge-TTS 原生 ManimGX Voice 引擎，支援自動快取與 `self.say()`。
2. 數學破音字發音自動校正器（「為 -> 唯」、「立方和 -> 立方核」、「和角 -> 禾角」、「差角 -> 插角」），
   僅於送入 TTS 合成時替換，保持程式碼、畫面字幕與 .srt 字幕為標準正體中文。
3. 2D / 3D 場景基底類別 (`TWScene`, `TWThreeDScene`)，內建：
   - `make_caption` / `set_caption`（繁中與 MathTex 混排底部 HUD 字幕）
   - `make_top_formula`（頂部 HUD 動態公式）
   - `add_fixed_orientation_mobjects`（3D 空間 Billboard 標籤，永遠正對鏡頭且支援位移與相機旋轉）
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from typing import Union

import edge_tts
import manimgx as m
import numpy as np
from manimgx.rendering.feed import rotation as _camera_rotation

# 預設繁體中文字型（Windows 系統字型「源石黑體」，若無則自動回退至 ManimGX 內建 Noto Sans CJK）
CHINESE_FONT = "GenSekiGothic TW"

# 台灣國語數學破音字校正字典（僅作用於 TTS 合成音軌，不影響字幕文字）
TW_HETERONYM_RULES: tuple[tuple[str, str], ...] = (
    ("立方和", "立方核"),
    ("平方和", "平方核"),
    ("和角", "禾角"),
    ("差角", "插角"),
    ("總和", "總核"),
    ("邊長為", "邊長唯"),
    ("體積為", "體積唯"),
    ("面積為", "面積唯"),
    ("長度為", "長度唯"),
    ("高度為", "高度唯"),
    ("寬度為", "寬度唯"),
    ("半徑為", "半徑唯"),
    ("斜邊為", "斜邊唯"),
    ("夾角為", "夾角唯"),
    ("分別為", "分別唯"),
    ("為骨架", "唯骨架"),
    ("設定為", "設定唯"),
    ("記為", "記唯"),
    ("稱為", "稱唯"),
)

_WORD_RE = re.compile(r"\S+")


def fix_tw_heteronyms(text: str) -> str:
    """將數學敘述中的破音字替換為同音正讀字，確保台灣雲哲 TTS 讀音準確。"""
    out = text
    for src, dst in TW_HETERONYM_RULES:
        out = out.replace(src, dst)
    # 針對如「斜邊 A F 為 1」這類「為」後接數字或代號的情境做通用二聲校正
    out = re.sub(r"為(?=\s*[0-9a-zA-Zα-ωΑ-Ω])", "唯", out)
    return out


async def _synthesize_edge_tts_bytes(text: str, voice: str, rate: str, pitch: str = "+0Hz") -> bytes:
    """透過 edge-tts 串流合成 MP3 音訊 bytes（含自動重試機制）。"""
    last_err: Exception | None = None
    for attempt in range(1, 4):
        try:
            comm = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
            chunks: list[bytes] = []
            async for chunk in comm.stream():
                if chunk.get("type") == "audio" and "data" in chunk:
                    chunks.append(chunk["data"])
            if chunks:
                return b"".join(chunks)
        except Exception as e:
            last_err = e
            if attempt < 3:
                await asyncio.sleep(0.8)
    raise RuntimeError(f"Edge-TTS 合成失敗 ({text!r}): {last_err}")


def _estimate_chinese_words(text: str, samples: np.ndarray) -> tuple[m.voices.Word, ...]:
    """針對中文與中英混排句子的字數與標點停頓權重，精確估算每個空白分詞片段的時間區間。"""
    tokens = _WORD_RE.findall(text)
    if not tokens:
        return ()
    rate = 48_000
    level = np.abs(samples).max(axis=1) if samples.ndim > 1 else np.abs(samples)
    hop = rate // 100  # 10 ms
    frames = len(level) // hop
    loud = level[: frames * hop].reshape(frames, hop).max(axis=1) > 0.02
    voiced = np.flatnonzero(loud)
    if not len(voiced):
        total = len(samples) / rate
        return tuple(
            m.voices.Word(w, total * i / len(tokens), total * (i + 1) / len(tokens))
            for i, w in enumerate(tokens)
        )
    first, last = int(voiced[0]), int(voiced[-1]) + 1
    weights: list[float] = []
    for w in tokens:
        pause = (
            6.0
            if w[-1] in ".!?:;。！？；："
            else 3.0
            if w[-1] in ",，、—"
            else 1.0
        )
        weights.append(float(len(w)) + pause)
    total_weight = sum(weights)
    edges = np.concatenate([[0.0], np.cumsum(weights)]) / total_weight
    span = (last - first) / 100.0
    times = first / 100.0 + edges * span
    return tuple(
        m.voices.Word(
            w,
            float(times[i]),
            float(times[i + 1] - (weights[i] - len(w)) / total_weight * span),
        )
        for i, w in enumerate(tokens)
    )


@dataclass(frozen=True)
class YunJheVoice:
    """ManimGX 相容之台灣男聲 (zh-TW-YunJheNeural) 語音合成器。

    身為 frozen dataclass，ManimGX 的 `cached()` 會自動以 `repr(self)` 作為快取金鑰，
    將合成後的 MP3 與時間軸 JSON 儲存於場景旁的 `voice/` 資料夾，不重複請求網路。
    """

    voice_id: str = "zh-TW-YunJheNeural"
    rate: str = "+12%"
    pitch: str = "+8Hz"
    apply_heteronym_fix: bool = True

    def __call__(self, text: str) -> m.Speech:
        spoken_text = fix_tw_heteronyms(text) if self.apply_heteronym_fix else text
        mp3_bytes = asyncio.run(
            _synthesize_edge_tts_bytes(spoken_text, self.voice_id, self.rate, self.pitch)
        )
        temp_sound = m.Sound(mp3_bytes)
        words = _estimate_chinese_words(text, temp_sound.samples)
        return m.Speech(mp3_bytes, text=text, words=words)


@dataclass(frozen=True)
class HsiaoChenVoice:
    """ManimGX 相容之台灣女聲 (zh-TW-HsiaoChenNeural) 沉穩知性款語音合成器。

    設定值：pitch: -15Hz, rate: +5%
    聽感：降調後保留咬字溫和度，散發沉著內斂的講課質感，聽感極為舒適耐聽。
    """

    voice_id: str = "zh-TW-HsiaoChenNeural"
    rate: str = "+5%"
    pitch: str = "-15Hz"
    apply_heteronym_fix: bool = True

    def __call__(self, text: str) -> m.Speech:
        spoken_text = fix_tw_heteronyms(text) if self.apply_heteronym_fix else text
        mp3_bytes = asyncio.run(
            _synthesize_edge_tts_bytes(spoken_text, self.voice_id, self.rate, self.pitch)
        )
        temp_sound = m.Sound(mp3_bytes)
        words = _estimate_chinese_words(text, temp_sound.samples)
        return m.Speech(mp3_bytes, text=text, words=words)


CaptionItem = Union[str, m.Mobject, tuple[str, str]]


class TWScene(m.Scene):
    """具備台灣繁中教學字幕、直角標記與雲哲配音預設值的 2D 標準場景。"""

    voice = YunJheVoice()
    current_caption: m.VGroup | None = None

    def make_caption(
        self,
        *items: CaptionItem,
        font_size: float = 24,
        math_font_size: float = 26,
        buff: float = 0.12,
        edge_buff: float = 0.45,
    ) -> m.VGroup:
        """建立底部繁體中文與數學公式混排字幕。

        支援傳入：
        - 一般字串 `"先考慮邊長為"` -> 自動轉為 `m.Text`
        - 元組 `("math", r"a^2 + b^2")` -> 自動轉為 `m.MathTex`
        - 任意 `m.Mobject`
        """
        parts: list[m.Mobject] = []
        for item in items:
            if isinstance(item, m.Mobject):
                parts.append(item)
            elif isinstance(item, tuple) and len(item) == 2 and item[0] == "math":
                parts.append(m.MathTex(item[1], font_size=math_font_size))
            else:
                parts.append(
                    m.Text(str(item), font=CHINESE_FONT, font_size=font_size)
                )
        group = m.VGroup(*parts).arrange(m.RIGHT, buff=buff)
        group.to_edge(m.DOWN, buff=edge_buff)
        return group

    def set_caption(self, new_caption: m.VGroup, run_time: float = 0.4) -> None:
        """平滑切換底部字幕（舊字幕微幅下移淡出、新字幕上移淡入）。"""
        if self.current_caption is not None:
            old_caption = self.current_caption
            self.current_caption = new_caption
            self.play(
                m.FadeOut(old_caption, shift=m.DOWN * 0.08),
                m.FadeIn(new_caption, shift=m.UP * 0.08),
                run_time=run_time,
            )
        else:
            self.current_caption = new_caption
            self.play(
                m.FadeIn(new_caption, shift=m.UP * 0.08),
                run_time=run_time,
            )

    def make_right_angle(
        self,
        corner: np.ndarray,
        p1: np.ndarray,
        p2: np.ndarray,
        size: float = 0.22,
        color: m.ParsableManimColor = m.WHITE,
        stroke_width: float = 1.8,
    ) -> m.VMobject:
        """依據頂點與兩鄰邊端點座標，精確繪製直角符號。"""
        v1 = (p1 - corner) / float(np.linalg.norm(p1 - corner))
        v2 = (p2 - corner) / float(np.linalg.norm(p2 - corner))
        p_a = corner + v1 * size
        p_b = corner + v1 * size + v2 * size
        p_c = corner + v2 * size
        return (
            m.VMobject()
            .set_points_as_corners([p_a, p_b, p_c])
            .set_stroke(color, stroke_width)
        )


class TWThreeDScene(m.ThreeDScene):
    """具備 2D HUD 固定圖層與 3D 空間 Billboard 固定朝向標籤的 3D 標準場景。"""

    voice = YunJheVoice()

    def make_caption(
        self,
        pre_text: str,
        math_tex: str | None = None,
        post_text: str | None = None,
        font_size: float = 28,
        edge_buff: float = 0.45,
    ) -> m.VGroup:
        """建立固定於 2D 螢幕底部的字幕（註冊至 camera HUD 層，不提前加入 scene 以支援 FadeIn）。"""
        parts: list[m.Mobject] = [
            m.Text(pre_text, font=CHINESE_FONT, font_size=font_size)
        ]
        if math_tex is not None:
            parts.append(m.MathTex(math_tex).scale(0.88))
        if post_text is not None:
            parts.append(
                m.Text(post_text, font=CHINESE_FONT, font_size=font_size)
            )
        group = m.VGroup(*parts).arrange(m.RIGHT, buff=0.18)
        group.to_edge(m.DOWN, buff=edge_buff)
        self.camera.add_fixed_in_frame_mobjects(group)
        return group

    def make_top_formula(
        self,
        tex: str,
        scale: float = 1.0,
        color: m.ParsableManimColor = m.YELLOW,
        edge_buff: float = 0.45,
    ) -> m.MathTex:
        """建立固定於 2D 螢幕頂部的公式（註冊至 camera HUD 層，不提前加入 scene 以支援 FadeIn）。"""
        obj = m.MathTex(tex).scale(scale)
        obj.to_edge(m.UP, buff=edge_buff)
        obj.set_color(color)
        self.camera.add_fixed_in_frame_mobjects(obj)
        return obj

    def add_fixed_orientation_mobjects(self, *mobjects: m.Mobject) -> None:
        """使 3D 空間中的文字或數學標籤永遠正對鏡頭（Billboard 效果），同時保留其 3D 空間座標與位移。"""
        cam = self.camera
        for mob in mobjects:
            # 紀錄當前已套用的相機角度，初始建立於 XY 平面的物件對應 (phi=0, theta=-pi/2, gamma=0)
            state = [
                cam.get_phi(),
                cam.get_theta(),
                cam.get_gamma(),
            ]
            r_init = _camera_rotation(state[0], state[1], state[2])
            mob.apply_matrix(r_init.T, about_point=mob.get_center())

            def _face_camera(
                mobj: m.Mobject,
                _state: list[float] = state,
            ) -> None:
                phi, theta, gamma = (
                    cam.get_phi(),
                    cam.get_theta(),
                    cam.get_gamma(),
                )
                if (
                    phi != _state[0]
                    or theta != _state[1]
                    or gamma != _state[2]
                ):
                    r_prev = _camera_rotation(_state[0], _state[1], _state[2])
                    r_curr = _camera_rotation(phi, theta, gamma)
                    delta = r_curr.T @ r_prev
                    mobj.apply_matrix(delta, about_point=mobj.get_center())
                    _state[0], _state[1], _state[2] = phi, theta, gamma

            mob.add_updater(_face_camera)
