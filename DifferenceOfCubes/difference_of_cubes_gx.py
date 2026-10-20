"""立方差公式 (a³ - b³) 3D 幾何拆解與台灣雲哲配音同步動畫 — ManimGX 移植標竿版."""

from __future__ import annotations

import os
import sys

# 確保可匯入專案根目錄之 manimgx_tw_helper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import manimgx as m
import numpy as np

from manimgx_tw_helper import TWThreeDScene, YunJheVoice


class DifferenceOfCubesGX(TWThreeDScene):
    """使用 ManimGX + Rust wgpu 3D 核心與內建 self.say() 雲哲配音同步之立方差證明。"""

    voice = YunJheVoice(rate="+15%")

    def construct(self) -> None:
        # =====================================================
        # 基本參數
        # =====================================================
        a = 4.0
        b = 2.25
        t = a - b

        color1 = m.PURPLE
        color2 = m.GREEN
        color3 = m.ORANGE

        self.set_camera_orientation(
            phi=65 * m.DEGREES,
            theta=-45 * m.DEGREES,
            zoom=0.92,
        )

        # =====================================================
        # 預先建立「缺角後」的三塊
        # =====================================================
        wall1 = m.Prism(dimensions=[t, a, a])
        wall1.move_to(np.array([-b / 2, 0.0, 0.0]))
        wall1.set_fill(color1, opacity=0.70)
        wall1.set_stroke(m.PURPLE_E, width=2)

        wall2 = m.Prism(dimensions=[b, t, a])
        wall2.move_to(np.array([a / 2 - b / 2, -b / 2, 0.0]))
        wall2.set_fill(color2, opacity=0.70)
        wall2.set_stroke(m.GREEN_E, width=2)

        wall3 = m.Prism(dimensions=[b, b, t])
        wall3.move_to(np.array([a / 2 - b / 2, a / 2 - b / 2, -b / 2]))
        wall3.set_fill(color3, opacity=0.82)
        wall3.set_stroke(m.ORANGE, width=2)

        carved_A = m.VGroup(wall1, wall2, wall3)

        # =====================================================
        # ① 完整 a³（透過 self.say 自動同步語音與動畫）
        # =====================================================
        cap1 = self.make_caption("先考慮一個邊長為", r"a", "的正方體")
        cube_A = m.Cube(side_length=a)
        cube_A.set_fill(m.BLUE_D, opacity=0.45)
        cube_A.set_stroke(m.BLUE_E, width=2)
        top_formula = self.make_top_formula(r"a^3", scale=1.05)

        self.say(
            "先考慮一個邊長為 a 的正方體，體積為 a 三方。",
            m.FadeIn(cap1),
            m.DrawBorderThenFill(cube_A, run_time=1.5),
            m.FadeIn(top_formula, run_time=1.5),
        )
        self.wait(0.4)

        # =====================================================
        # ② b³ 在角落慢慢亮起
        # =====================================================
        cap2 = self.make_caption("角落挖掉一個邊長為", r"b", "的小立方體")
        corner_center = np.array([a / 2 - b / 2, a / 2 - b / 2, a / 2 - b / 2])

        cube_B = m.Cube(side_length=b)
        cube_B.move_to(corner_center)
        cube_B.set_fill(m.RED, opacity=0.0)
        cube_B.set_stroke(m.RED_E, width=2, opacity=0.0)

        b3_label = m.MathTex(r"b^3").scale(0.9)
        b3_label.move_to(corner_center + np.array([0.0, 0.0, b * 0.72]))
        self.add_fixed_orientation_mobjects(b3_label)

        self.say(
            "從角落標出一個邊長為 b 的小正方體，體積為 b 三方。",
            m.FadeOut(cap1, run_time=0.5),
            m.FadeIn(cap2, run_time=0.5),
            cube_B.animate.set_fill(m.RED, opacity=0.72).set_stroke(m.RED_E, opacity=1.0),
            m.FadeIn(b3_label),
        )

        # 關鍵銜接：B 還在角落時，將完整 A 無縫換成缺角 A
        self.play(
            m.FadeOut(cube_A),
            m.FadeIn(carved_A),
            run_time=0.6,
        )

        # =====================================================
        # ③ b³ 從角落抽出
        # =====================================================
        cap3 = self.make_caption("把這個小立方體抽離出去")
        extract_vec = m.RIGHT * 2.4 + m.UP * 1.15 + m.OUT * 1.35

        self.say(
            "把這個小正方體抽離出去。",
            m.FadeOut(cap2, run_time=0.4),
            m.FadeIn(cap3, run_time=0.4),
            cube_B.animate.shift(extract_vec),
            b3_label.animate.shift(extract_vec),
        )

        new_formula = self.make_top_formula(r"a^3-b^3", scale=1.05)
        self.play(
            m.FadeOut(top_formula),
            m.FadeIn(new_formula),
            m.FadeOut(cube_B),
            m.FadeOut(b3_label),
            run_time=0.8,
        )
        top_formula = new_formula

        # =====================================================
        # ④ 鏡頭繞到凹槽方向
        # =====================================================
        cap4 = self.make_caption("轉動視角，剩餘部分體積為", r"a^3-b^3")
        self.play(m.FadeOut(cap3), m.FadeIn(cap4), run_time=0.5)
        self.move_camera(
            phi=68 * m.DEGREES,
            theta=-18 * m.DEGREES,
            zoom=0.95,
            run_time=1.6,
        )
        self.say("轉動視角觀察，剩餘部分的體積為 a 三方減 b 三方。")

        # =====================================================
        # ⑤ 看清楚留下的三部分 & ⑥ 依序拆開
        # =====================================================
        cap5 = self.make_caption("剩下的部分可以分成三個長方體")
        self.say(
            "剩下的結構，剛好可以分割為三個長方體。",
            m.FadeOut(cap4, run_time=0.5),
            m.FadeIn(cap5, run_time=0.5),
        )

        gap = 0.55
        total_width = a + b + b + 2 * gap
        left_edge = -total_width / 2

        final_pos1 = np.array([left_edge + a / 2, 0.0, t / 2])
        final_pos2 = np.array([left_edge + a + gap + b / 2, 0.0, t / 2])
        final_pos3 = np.array([left_edge + a + gap + b + gap + b / 2, 0.0, t / 2])

        cap6 = self.make_caption("把三個長方體依序拆開")
        sep_pos1 = np.array([final_pos1[0], 0.0, 0.0])
        sep_pos2 = np.array([final_pos2[0], -2.0, 0.0])
        sep_pos3 = np.array([final_pos3[0], 0.875, 0.0])

        self.say(
            "現在將這三個長方體依序往外拆開。",
            m.FadeOut(cap5, run_time=0.4),
            m.FadeIn(cap6, run_time=0.4),
            m.Succession(
                wall1.animate(run_time=0.8).move_to(sep_pos1),
                wall2.animate(run_time=0.8).move_to(sep_pos2),
                wall3.animate(run_time=0.8).move_to(sep_pos3),
            ),
        )

        # =====================================================
        # ⑦ 剛體變換：旋轉攤平，使共同厚度 a-b 朝上呈現等高
        # =====================================================
        cap7 = self.make_caption("旋轉攤平，三個長方體都有相同的厚度", r"a-b")
        self.say(
            "將它們原地旋轉攤平並排齊，可以發現三塊都有相同的厚度 a 減 b。",
            m.FadeOut(cap6, run_time=0.4),
            m.FadeIn(cap7, run_time=0.4),
            m.Succession(
                m.AnimationGroup(
                    m.Rotate(wall1, angle=m.PI / 2, axis=m.UP, run_time=1.1),
                    m.Rotate(wall2, angle=m.PI / 2, axis=m.RIGHT, run_time=1.1),
                ),
                m.AnimationGroup(
                    wall1.animate(run_time=1.0).move_to(final_pos1),
                    wall2.animate(run_time=1.0).move_to(final_pos2),
                    wall3.animate(run_time=1.0).move_to(final_pos3),
                ),
            ),
        )

        # =====================================================
        # ⑧ 鏡頭切換為正視角：清楚確認三者共同高度 a-b
        # =====================================================
        self.move_camera(
            phi=82 * m.DEGREES,
            theta=-90 * m.DEGREES,
            zoom=1.0,
            run_time=1.6,
        )

        y_front = -a / 2
        x_line = left_edge - 0.45

        thickness_line = m.Line(
            np.array([x_line, y_front, 0.0]),
            np.array([x_line, y_front, t]),
            color=m.YELLOW,
        )
        tick_top = m.Line(
            np.array([left_edge, y_front, t]),
            np.array([x_line - 0.15, y_front, t]),
            color=m.YELLOW,
            stroke_width=2,
        )
        tick_bot = m.Line(
            np.array([left_edge, y_front, 0.0]),
            np.array([x_line - 0.15, y_front, 0.0]),
            color=m.YELLOW,
            stroke_width=2,
        )

        thickness_label = m.MathTex(r"a-b").scale(0.85)
        thickness_label.move_to(np.array([x_line - 0.55, y_front, t / 2]))
        self.add_fixed_orientation_mobjects(thickness_label)

        self.say(
            "從正面看，三塊的高度完全一致，皆為 a 減 b。",
            m.Create(thickness_line),
            m.Create(tick_top),
            m.Create(tick_bot),
            m.FadeIn(thickness_label),
        )

        # =====================================================
        # ⑨ 鏡頭切換為俯視角：觀察頂部面積
        # =====================================================
        cap8 = self.make_caption("從上面看，三塊的面積分別是", r"a^2,\ ab,\ b^2")
        self.play(
            m.FadeOut(cap7),
            m.FadeIn(cap8),
            m.FadeOut(thickness_line),
            m.FadeOut(tick_top),
            m.FadeOut(tick_bot),
            m.FadeOut(thickness_label),
            run_time=0.6,
        )

        self.move_camera(
            phi=0 * m.DEGREES,
            theta=-90 * m.DEGREES,
            zoom=1.0,
            run_time=1.5,
        )

        area1 = m.MathTex(r"a^2").scale(0.95)
        area2 = m.MathTex(r"ab").scale(0.95)
        area3 = m.MathTex(r"b^2").scale(0.95)

        area1.move_to(wall1.get_center() + np.array([0.0, 0.0, t * 0.55]))
        area2.move_to(wall2.get_center() + np.array([0.0, 0.0, t * 0.55]))
        area3.move_to(wall3.get_center() + np.array([0.0, 0.0, t * 0.55]))

        self.add_fixed_orientation_mobjects(area1, area2, area3)

        f1 = m.MathTex(r"a^2+ab+b^2").scale(1.0).to_edge(m.UP, buff=0.45)
        self.camera.add_fixed_in_frame_mobjects(f1)

        self.say(
            "再從正上方俯視，三塊的底面積分別為 a 平方、a b 與 b 平方。",
            m.FadeIn(area1),
            m.FadeIn(area2),
            m.FadeIn(area3),
            m.FadeOut(top_formula),
            m.FadeIn(f1),
        )

        # =====================================================
        # ⑩ 公式經典 3B1B 連續移位展開
        # =====================================================
        cap9 = self.make_caption("因此剩餘體積也可以寫成")
        f2 = (
            m.MathTex(r"(a-b)", r"(a^2+ab+b^2)")
            .scale(1.0)
            .to_edge(m.UP, buff=0.45)
        )
        f2[0].set_color(m.YELLOW)
        f2[1].set_color(m.WHITE)
        self.camera.add_fixed_in_frame_mobjects(f2)

        self.say(
            "將共同厚度乘上底面積總和，體積即可寫成 a 減 b，乘上 a 平方加 a b 加 b 平方。",
            m.FadeOut(cap8, run_time=0.5),
            m.FadeIn(cap9, run_time=0.5),
            m.ReplacementTransform(f1, f2[1], run_time=1.1),
            m.FadeIn(f2[0], shift=m.RIGHT * 0.3, run_time=1.1),
        )

        final_caption = self.make_caption("因此得到立方差公式")
        f3 = (
            m.MathTex(r"a^3-b^3", r"=", r"(a-b)", r"(a^2+ab+b^2)")
            .scale(1.05)
            .to_edge(m.UP, buff=0.45)
        )
        f3.set_color(m.YELLOW)
        self.camera.add_fixed_in_frame_mobjects(f3)

        final_box = m.SurroundingRectangle(f3, buff=0.2, color=m.YELLOW)
        self.camera.add_fixed_in_frame_mobjects(final_box)

        self.say(
            "由此直觀證得立方差公式！",
            m.FadeOut(cap9, run_time=0.5),
            m.FadeOut(area1, run_time=0.5),
            m.FadeOut(area2, run_time=0.5),
            m.FadeOut(area3, run_time=0.5),
            m.FadeIn(final_caption, run_time=0.5),
            m.ReplacementTransform(f2[0], f3[2], run_time=1.1),
            m.ReplacementTransform(f2[1], f3[3], run_time=1.1),
            m.FadeIn(f3[0:2], shift=m.RIGHT * 0.3, run_time=1.1),
            m.Create(final_box, run_time=1.2),
        )
        self.wait(1.5)
