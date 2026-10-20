from manim import *
import numpy as np


class DifferenceOfCubes(ThreeDScene):

    # ---------------------------------------------------------
    # 畫面下方字幕（固定在螢幕二維圖層，支援前綴文字 + 數學式 + 後綴文字）
    # 使用 camera.add_fixed_in_frame_mobjects，避免預先將物件加進場景造成搶先顯示
    # ---------------------------------------------------------
    def make_caption(self, pre_text, math_tex=None, post_text=None):
        parts = [Text(pre_text, font_size=28)]
        if math_tex is not None:
            parts.append(MathTex(math_tex).scale(0.88))
        if post_text is not None:
            parts.append(Text(post_text, font_size=28))

        group = VGroup(*parts).arrange(RIGHT, buff=0.18)
        group.to_edge(DOWN, buff=0.45)
        self.camera.add_fixed_in_frame_mobjects(group)
        return group

    # ---------------------------------------------------------
    # 畫面上方公式（固定在螢幕二維圖層）
    # ---------------------------------------------------------
    def make_top_formula(self, tex, scale=1.0, color=YELLOW):
        obj = MathTex(tex).scale(scale)
        obj.to_edge(UP, buff=0.45)
        obj.set_color(color)
        self.camera.add_fixed_in_frame_mobjects(obj)
        return obj

    def construct(self):

        # =====================================================
        # 基本參數
        # =====================================================
        a = 4.0
        b = 2.25
        t = a - b

        color1 = PURPLE
        color2 = GREEN
        color3 = ORANGE

        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.92
        )

        # =====================================================
        # 預先建立「缺角後」的三塊
        # =====================================================
        wall1 = Prism(dimensions=[t, a, a])
        wall1.move_to(np.array([-b / 2, 0, 0]))
        wall1.set_fill(color1, opacity=0.70)
        wall1.set_stroke(PURPLE_E, width=2)

        wall2 = Prism(dimensions=[b, t, a])
        wall2.move_to(np.array([
            a / 2 - b / 2,
            -b / 2,
            0
        ]))
        wall2.set_fill(color2, opacity=0.70)
        wall2.set_stroke(GREEN_E, width=2)

        wall3 = Prism(dimensions=[b, b, t])
        wall3.move_to(np.array([
            a / 2 - b / 2,
            a / 2 - b / 2,
            -b / 2
        ]))
        wall3.set_fill(color3, opacity=0.82)
        wall3.set_stroke(ORANGE, width=2)

        carved_A = VGroup(wall1, wall2, wall3)

        # =====================================================
        # ① 完整 a³
        # =====================================================
        cap1 = self.make_caption(
            "先考慮一個邊長為",
            r"a",
            "的正方體"
        )
        self.play(FadeIn(cap1))

        cube_A = Cube(side_length=a)
        cube_A.set_fill(BLUE_D, opacity=0.45)
        cube_A.set_stroke(BLUE_E, width=2)

        top_formula = self.make_top_formula(
            r"a^3",
            scale=1.05
        )

        self.play(
            DrawBorderThenFill(cube_A),
            FadeIn(top_formula),
            run_time=1.5
        )
        self.wait(1.0)

        # =====================================================
        # ② b³ 在角落慢慢亮起
        # 同時 A 準備變成缺角立體
        # =====================================================
        cap2 = self.make_caption(
            "角落挖掉一個邊長為",
            r"b",
            "的小立方體"
        )

        corner_center = np.array([
            a / 2 - b / 2,
            a / 2 - b / 2,
            a / 2 - b / 2
        ])

        cube_B = Cube(side_length=b)
        cube_B.move_to(corner_center)
        cube_B.set_fill(RED, opacity=0.0)
        cube_B.set_stroke(RED_E, width=2, opacity=0.0)

        b3_label = MathTex(r"b^3").scale(0.9)
        b3_label.move_to(
            corner_center + np.array([0, 0, b * 0.72])
        )
        self.add_fixed_orientation_mobjects(b3_label)

        self.play(
            FadeOut(cap1),
            FadeIn(cap2)
        )

        self.play(
            cube_B.animate
                .set_fill(RED, opacity=0.72)
                .set_stroke(RED_E, opacity=1),
            FadeIn(b3_label),
            run_time=1.3
        )

        self.wait(0.6)

        # =====================================================
        # 關鍵銜接：
        # B 還在角落時，就把完整 A 換成缺角 A
        # =====================================================
        self.play(
            FadeOut(cube_A),
            FadeIn(carved_A),
            run_time=0.8
        )

        self.wait(0.4)

        # =====================================================
        # ③ b³ 從角落抽出
        # =====================================================
        cap3 = self.make_caption(
            "把這個小立方體抽離出去"
        )

        self.play(
            FadeOut(cap2),
            FadeIn(cap3)
        )

        extract_vec = RIGHT * 2.4 + UP * 1.15 + OUT * 1.35

        self.play(
            cube_B.animate.shift(extract_vec),
            b3_label.animate.shift(extract_vec),
            run_time=1.5
        )

        self.wait(0.4)

        # 上方公式由 a^3 切換成 a^3-b^3
        new_formula = self.make_top_formula(
            r"a^3-b^3",
            scale=1.05
        )

        self.play(
            FadeOut(top_formula),
            FadeIn(new_formula),
            FadeOut(cube_B),
            FadeOut(b3_label)
        )

        top_formula = new_formula

        self.wait(0.6)

        # =====================================================
        # ④ 鏡頭繞到凹槽方向
        # =====================================================
        cap4 = self.make_caption(
            "轉動視角，剩餘部分體積為",
            r"a^3-b^3"
        )

        self.play(
            FadeOut(cap3),
            FadeIn(cap4)
        )

        self.move_camera(
            phi=68 * DEGREES,
            theta=-18 * DEGREES,
            zoom=0.95,
            run_time=1.8
        )

        self.wait(1.0)

        # =====================================================
        # ⑤ 看清楚留下的三部分
        # =====================================================
        cap5 = self.make_caption(
            "剩下的部分可以分成三個長方體"
        )

        self.play(
            FadeOut(cap4),
            FadeIn(cap5)
        )

        self.wait(1.0)

        # =====================================================
        # 預先計算最終橫列的 X 軸與空間錨點（由左至右：a²、ab、b²）
        # =====================================================
        gap = 0.55
        total_width = a + b + b + 2 * gap
        left_edge = -total_width / 2

        final_pos1 = np.array([left_edge + a / 2, 0, t / 2])
        final_pos2 = np.array([left_edge + a + gap + b / 2, 0, t / 2])
        final_pos3 = np.array([left_edge + a + gap + b + gap + b / 2, 0, t / 2])

        # =====================================================
        # ⑥ 三塊依序拆開（方向與最終攤平一致，絕不交錯）
        # wall1 往左移至最終左欄 (X1)
        # wall2 往前移脫離凹槽，保持在正中欄 (X2)
        # wall3 往右上方移至最終右欄 (X3)
        # =====================================================
        cap6 = self.make_caption(
            "把三個長方體依序拆開"
        )

        self.play(
            FadeOut(cap5),
            FadeIn(cap6)
        )

        sep_pos1 = np.array([final_pos1[0], 0, 0])
        sep_pos2 = np.array([final_pos2[0], -2.0, 0])
        sep_pos3 = np.array([final_pos3[0], 0.875, 0])

        # 1. 紫色塊往左脫離
        self.play(
            wall1.animate.move_to(sep_pos1),
            run_time=0.9
        )
        self.wait(0.15)

        # 2. 綠色塊往前脫離，維持在正中
        self.play(
            wall2.animate.move_to(sep_pos2),
            run_time=0.9
        )
        self.wait(0.15)

        # 3. 橘色塊往右上方脫離
        self.play(
            wall3.animate.move_to(sep_pos3),
            run_time=0.9
        )
        self.wait(0.5)

        # =====================================================
        # ⑦ 剛體變換：旋轉攤平，使共同厚度 a-b 朝上呈現等高
        # （原地剛體旋轉 + 平行滑動排齊，動線完全一致）
        # =====================================================
        cap7 = self.make_caption(
            "旋轉攤平，三個長方體都有相同的厚度",
            r"a-b"
        )

        self.play(
            FadeOut(cap6),
            FadeIn(cap7)
        )

        # 1. 原地剛體旋轉：wall1 與 wall2 翻倒躺平
        # wall1 繞 UP (Y軸) 旋轉 90° -> 厚度 t 朝向 Z (高度)
        # wall2 繞 RIGHT (X軸) 旋轉 90° -> 厚度 t 朝向 Z (高度)
        # wall3 本身厚度 t 已朝向 Z (高度)，維持不變
        self.play(
            Rotate(wall1, angle=PI / 2, axis=UP),
            Rotate(wall2, angle=PI / 2, axis=RIGHT),
            run_time=1.2
        )

        self.wait(0.3)

        # 2. 剛體平移排齊：各自分別沿 Y/Z 軸滑入同一直線，X 軸保持平行，絕無交錯
        self.play(
            wall1.animate.move_to(final_pos1),
            wall2.animate.move_to(final_pos2),
            wall3.animate.move_to(final_pos3),
            run_time=1.1
        )

        self.wait(0.5)

        # =====================================================
        # ⑧ 鏡頭切換為正視角：清楚確認三者共同高度 a-b
        # =====================================================
        self.move_camera(
            phi=82 * DEGREES,
            theta=-90 * DEGREES,
            zoom=1.0,
            run_time=2.0
        )

        self.wait(0.4)

        y_front = -a / 2
        x_line = left_edge - 0.45

        thickness_line = Line(
            np.array([x_line, y_front, 0]),
            np.array([x_line, y_front, t]),
            color=YELLOW
        )
        tick_top = Line(
            np.array([left_edge, y_front, t]),
            np.array([x_line - 0.15, y_front, t]),
            color=YELLOW,
            stroke_width=2
        )
        tick_bot = Line(
            np.array([left_edge, y_front, 0]),
            np.array([x_line - 0.15, y_front, 0]),
            color=YELLOW,
            stroke_width=2
        )

        thickness_label = MathTex(r"a-b").scale(0.85)
        thickness_label.move_to(
            np.array([x_line - 0.55, y_front, t / 2])
        )
        self.add_fixed_orientation_mobjects(thickness_label)

        self.play(
            Create(thickness_line),
            Create(tick_top),
            Create(tick_bot),
            FadeIn(thickness_label)
        )

        self.wait(1.0)

        # =====================================================
        # ⑨ 鏡頭切換為俯視角：觀察頂部面積
        # 在鏡頭轉動前，立即將厚度標示線與舊字幕收掉
        # =====================================================
        cap8 = self.make_caption(
            "從上面看，三塊的面積分別是",
            r"a^2,\ ab,\ b^2"
        )

        self.play(
            FadeOut(cap7),
            FadeIn(cap8),
            FadeOut(thickness_line),
            FadeOut(tick_top),
            FadeOut(tick_bot),
            FadeOut(thickness_label),
            run_time=0.8
        )

        # 乾淨俐落地切換至俯視鏡頭
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            zoom=1.0,
            run_time=1.8
        )

        self.wait(0.4)

        area1 = MathTex(r"a^2").scale(0.95)
        area2 = MathTex(r"ab").scale(0.95)
        area3 = MathTex(r"b^2").scale(0.95)

        area1.move_to(
            wall1.get_center() + np.array([0, 0, t * 0.55])
        )
        area2.move_to(
            wall2.get_center() + np.array([0, 0, t * 0.55])
        )
        area3.move_to(
            wall3.get_center() + np.array([0, 0, t * 0.55])
        )

        self.add_fixed_orientation_mobjects(
            area1,
            area2,
            area3
        )

        self.play(
            FadeIn(area1),
            FadeIn(area2),
            FadeIn(area3)
        )

        self.wait(0.8)

        # =====================================================
        # ⑩ 公式經典 3B1B 連續移位展開（按步就班，到位後才呈現）
        # =====================================================
        # 1. 頂部先呈現底面積和：a^2+ab+b^2
        f1 = MathTex(r"a^2+ab+b^2").scale(1.0).to_edge(UP, buff=0.45)
        self.camera.add_fixed_in_frame_mobjects(f1)

        self.play(
            FadeOut(top_formula),
            FadeIn(f1)
        )
        self.wait(1.0)

        # 2. 加上括號後右移，左側出現 (a-b)，體積 = (a-b)(a^2+ab+b^2)
        cap9 = self.make_caption(
            "因此剩餘體積也可以寫成"
        )

        f2 = MathTex(
            r"(a-b)",
            r"(a^2+ab+b^2)"
        ).scale(1.0).to_edge(UP, buff=0.45)
        f2[0].set_color(YELLOW)
        f2[1].set_color(WHITE)
        self.camera.add_fixed_in_frame_mobjects(f2)

        self.play(
            FadeOut(cap8),
            FadeIn(cap9),
            ReplacementTransform(f1, f2[1]),
            FadeIn(f2[0], shift=RIGHT * 0.3),
            run_time=1.2
        )
        self.wait(1.2)

        # 3. 內容再往右移，左側出現 a^3-b^3 = 
        final_caption = self.make_caption("因此得到立方差公式")

        f3 = MathTex(
            r"a^3-b^3",
            r"=",
            r"(a-b)",
            r"(a^2+ab+b^2)"
        ).scale(1.05).to_edge(UP, buff=0.45)
        f3.set_color(YELLOW)
        self.camera.add_fixed_in_frame_mobjects(f3)

        self.play(
            FadeOut(cap9),
            FadeOut(area1),
            FadeOut(area2),
            FadeOut(area3),
            FadeIn(final_caption),
            ReplacementTransform(f2[0], f3[2]),
            ReplacementTransform(f2[1], f3[3]),
            FadeIn(f3[0:2], shift=RIGHT * 0.3),
            run_time=1.3
        )

        final_box = SurroundingRectangle(
            f3,
            buff=0.2,
            color=YELLOW
        )
        self.camera.add_fixed_in_frame_mobjects(final_box)

        self.play(Create(final_box))
        self.wait(3)