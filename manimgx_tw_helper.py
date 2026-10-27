"""台灣繁體中文數學幾何動畫 ManimGX 核心輔助模組 (manimgx_tw_helper.py).

整合功能：
1. 台灣雲哲 (zh-TW-YunJheNeural) Edge-TTS 原生 ManimGX Voice 引擎，支援自動快取與 `self.say()`。
2. 數學破音字發音自動校正器（「為 -> 唯」、「立方和 -> 立方核」、「和角 -> 禾角」、「差角 -> 插角」），
   僅於送入 TTS 合成時替換，保持程式碼、畫面字幕與 .srt 字幕為標準正體中文。
3. 2D / 3D 場景基底類別 (`TWScene`, `TWThreeDScene`)，內建：
   - `make_caption` / `set_caption`（繁中與 MathTex 混排底部 HUD 字幕）
   - `make_top_formula`（頂部 HUD 動態公式）
   - `add_fixed_orientation_mobjects`（3D 空間 Billboard 標籤，永遠正對鏡頭且支援位移與相機旋轉）
4. 現代科技卡片簡報風格 (`TWInfographicScene`)：
   - 深色科技感微網格背景 (`setup_slide_background`)
   - 頂部導航狀態欄與進度計數器 (`make_slide_hud` / `update_slide_step`)
   - 左側強調色條大標題組 (`make_title_hero`)
   - 區域色塊卡片元件 (`make_zone_card`) 與圓角代碼膠囊 (`make_code_pill`)
   - 資訊降噪聚焦控制 (`focus_cards`：自動高亮當前主角卡片並將非重點卡片半透明壓暗)
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from typing import Sequence, Union

import edge_tts
import manimgx as m
import numpy as np
from manimgx.rendering.feed import rotation as _camera_rotation

# 預設繁體中文字型（Windows 系統字型「源石黑體」，若無則自動回退至 ManimGX 內建 Noto Sans CJK）
CHINESE_FONT = "GenSekiGothic TW"
MONO_FONT = "Cascadia Code"

# ── 現代科技卡片簡報風格色票 (Tech Infographic / Command Map Palette) ──
SLIDE_BG = "#0B0F17"            # 深灰藍暗黑底色（非死黑）
SLIDE_GRID_COLOR = "#1E293B"    # 背景微弱科技格線色
SLIDE_CARD_BG = "#111827"       # 卡片半透明深色底
SLIDE_CARD_STROKE = "#1F2937"   # 卡片預設細邊框色
SLIDE_PILL_BG = "#0F172A"       # 膠囊標籤底色
SLIDE_TEXT_MAIN = "#F8FAFC"     # 主標題亮白
SLIDE_TEXT_MUTED = "#94A3B8"    # 副標題 / 頂部導航灰白

# 四大主題色標 (Accent Colors：橘、天藍、薄荷青綠、亮紫)
SLIDE_ACCENT_ORANGE = "#FB923C"
SLIDE_ACCENT_CYAN = "#38BDF8"
SLIDE_ACCENT_MINT = "#34D399"
SLIDE_ACCENT_PURPLE = "#A855F7"
SLIDE_PALETTE: tuple[str, ...] = (
    SLIDE_ACCENT_ORANGE,
    SLIDE_ACCENT_CYAN,
    SLIDE_ACCENT_MINT,
    SLIDE_ACCENT_PURPLE,
)

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

    設定值：pitch: -15Hz, rate: +25%
    聽感：降調後保留咬字溫和度，散發沉著內斂的講課質感，語速輕快俐落、不拖泥帶水。
    """

    voice_id: str = "zh-TW-HsiaoChenNeural"
    rate: str = "+25%"
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


class TWInfographicScene(TWScene):
    """現代科技卡片簡報與指令地圖風格基底場景 (Tech Infographic / Map Slide Style).

    設計靈感：高對比深灰藍科技底色、微弱矩陣格線、頂部 HUD 章節進度欄、
    彩色色標卡片 (Zone Cards)、圓角指令膠囊 (Code Pills)，以及透過「動態焦點高亮 +
    非主角半透明壓暗 (Dimming)」徹底解決傳統高密度資訊圖表視覺過載的問題。
    """

    hud_group: m.VGroup | None = None
    hud_section_label: m.Text | None = None
    hud_counter_label: m.Text | None = None

    def setup_slide_background(self, show_grid: bool = True) -> m.VGroup:
        """初始化深色科技感背景與極低透明度格線。"""
        self.camera.background_color = SLIDE_BG
        bg_group = m.VGroup()
        if show_grid:
            grid = m.NumberPlane(
                x_range=(-8, 8, 1),
                y_range=(-4.5, 4.5, 1),
                background_line_style={
                    "stroke_color": SLIDE_GRID_COLOR,
                    "stroke_width": 1.0,
                    "stroke_opacity": 0.28,
                },
                axis_config={
                    "stroke_color": SLIDE_GRID_COLOR,
                    "stroke_width": 1.0,
                    "stroke_opacity": 0.28,
                },
            )
            bg_group.add(grid)
            self.add(bg_group)
        return bg_group

    def make_slide_hud(
        self,
        series_title: str,
        section_title: str,
        step: int = 1,
        total_steps: int = 10,
        accent_color: m.ParsableManimColor = SLIDE_ACCENT_MINT,
    ) -> m.VGroup:
        """建立頂部 HUD 導航狀態欄（左上系列與章節名稱、右上進度計數、底部分隔細線）。"""
        icon_bars = m.VGroup(
            m.Line(m.ORIGIN, m.RIGHT * 0.14, stroke_width=3, color=SLIDE_ACCENT_ORANGE),
            m.Line(m.ORIGIN, m.RIGHT * 0.22, stroke_width=3, color=accent_color),
            m.Line(m.ORIGIN, m.RIGHT * 0.18, stroke_width=3, color=SLIDE_ACCENT_PURPLE),
        ).arrange(m.DOWN, buff=0.05, aligned_edge=m.LEFT)

        t_series = m.Text(
            series_title,
            font=CHINESE_FONT,
            font_size=18,
            color=SLIDE_TEXT_MAIN,
        )
        sep = m.Line(m.UP * 0.12, m.DOWN * 0.12, stroke_width=1.5, color=SLIDE_CARD_STROKE)
        t_section = m.Text(
            section_title,
            font=CHINESE_FONT,
            font_size=18,
            color=accent_color,
        )
        left_nav = m.VGroup(icon_bars, t_series, sep, t_section).arrange(m.RIGHT, buff=0.16)
        left_nav.to_corner(m.UL, buff=0.38)

        counter_str = f"{step:02d} / {total_steps:02d}"
        t_counter = m.Text(
            counter_str,
            font=MONO_FONT,
            font_size=18,
            color=SLIDE_TEXT_MUTED,
        )
        t_counter.to_corner(m.UR, buff=0.38)
        t_counter.match_y(left_nav)

        divider = m.Line(
            [-6.7, left_nav.get_bottom()[1] - 0.16, 0],
            [6.7, left_nav.get_bottom()[1] - 0.16, 0],
            stroke_width=1.0,
            color=SLIDE_CARD_STROKE,
        )

        self.hud_section_label = t_section
        self.hud_counter_label = t_counter
        self.hud_group = m.VGroup(left_nav, t_counter, divider)
        return self.hud_group

    def make_title_hero(
        self,
        main_prefix: str,
        main_highlight: str,
        subtitle: str,
        accent_color: m.ParsableManimColor = SLIDE_ACCENT_MINT,
    ) -> m.VGroup:
        """建立開場大字報標題組（頂部短色條 + 雙色主標題 + 清晰副標題）。"""
        top_bar = m.Line(m.ORIGIN, m.RIGHT * 0.55, stroke_width=4, color=accent_color)
        t1 = m.Text(main_prefix, font=CHINESE_FONT, font_size=56, color=SLIDE_TEXT_MAIN)
        t2 = m.Text(main_highlight, font=CHINESE_FONT, font_size=56, color=accent_color)
        title_row = m.VGroup(t1, t2).arrange(m.RIGHT, buff=0.22)
        sub = m.Text(subtitle, font=CHINESE_FONT, font_size=24, color=SLIDE_TEXT_MUTED)

        hero = m.VGroup(top_bar, title_row, sub).arrange(
            m.DOWN, buff=0.28, aligned_edge=m.LEFT
        )
        return hero

    def make_zone_card(
        self,
        title: str,
        subtitle: str = "",
        accent_color: m.ParsableManimColor = SLIDE_ACCENT_CYAN,
        width: float = 3.0,
        height: float = 3.6,
    ) -> m.VGroup:
        """建立具備頂部主題色標 (Accent Bar) 與半透明深色底的區域卡片元件。"""
        bg = m.RoundedRectangle(
            corner_radius=0.14,
            width=width,
            height=height,
            fill_color=SLIDE_CARD_BG,
            fill_opacity=0.82,
            stroke_color=SLIDE_CARD_STROKE,
            stroke_width=1.6,
        )
        accent_bar = m.Line(
            m.ORIGIN,
            m.RIGHT * 0.65,
            stroke_width=4.5,
            color=accent_color,
        )
        accent_bar.move_to(
            bg.get_corner(m.UL) + m.RIGHT * (0.32 + 0.325) + m.DOWN * 0.32
        )

        lbl_title = m.Text(
            title,
            font=CHINESE_FONT,
            font_size=22,
            color=SLIDE_TEXT_MAIN,
        )
        lbl_title.next_to(accent_bar, m.DOWN, buff=0.18, aligned_edge=m.LEFT)

        card = m.VGroup(bg, accent_bar, lbl_title)
        if subtitle:
            lbl_sub = m.Text(
                subtitle,
                font=CHINESE_FONT,
                font_size=15,
                color=SLIDE_TEXT_MUTED,
            )
            lbl_sub.next_to(lbl_title, m.DOWN, buff=0.10, aligned_edge=m.LEFT)
            card.add(lbl_sub)
        return card

    def make_code_pill(
        self,
        code_text: str,
        accent_color: m.ParsableManimColor = SLIDE_ACCENT_CYAN,
        font_size: float = 17,
        h_pad: float = 0.32,
        v_pad: float = 0.18,
    ) -> m.VGroup:
        """建立圓角指令膠囊 / 公式標籤 (Code Pill / Badge)。"""
        txt = m.Text(code_text, font=MONO_FONT, font_size=font_size, color=accent_color)
        pill_bg = m.RoundedRectangle(
            corner_radius=0.10,
            width=float(txt.width) + h_pad,
            height=float(txt.height) + v_pad,
            fill_color=SLIDE_PILL_BG,
            fill_opacity=0.95,
            stroke_color=accent_color,
            stroke_width=1.4,
        )
        txt.move_to(pill_bg.get_center())
        return m.VGroup(pill_bg, txt)

    def focus_cards(
        self,
        cards: Sequence[m.VGroup] | m.VGroup,
        active_indices: Sequence[int],
        dim_opacity: float = 0.22,
    ) -> list[m.Animation]:
        """資訊降噪控制：高亮 `active_indices` 中的主角卡片，並將其餘卡片半透明壓暗。"""
        anims: list[m.Animation] = []
        active_set = set(active_indices)
        for idx, card in enumerate(cards):
            target_op = 1.0 if idx in active_set else dim_opacity
            anims.append(card.animate.set_opacity(target_op))
        return anims

