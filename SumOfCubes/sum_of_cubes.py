from manim import *
import numpy as np

# ============================================================
# 字型設定（系統已安裝「源石黑體 GenSekiGothic TW」）
# ============================================================
CHINESE_FONT = "GenSekiGothic TW"


class SumOfCubes(ThreeDScene):

    # ---------------------------------------------------------
    # 畫面下方字幕（固定在螢幕二維圖層，支援中文與數學式混排）
    # ---------------------------------------------------------
    def make_caption(self, *items):
        parts = []
        for item in items:
            if isinstance(item, Mobject):
                parts.append(item)
            elif isinstance(item, tuple) and item[0] == "math":
                parts.append(MathTex(item[1]).scale(0.88))
            else:
                parts.append(Text(str(item), font=CHINESE_FONT, font_size=28))

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
        # 基本參數設定：a=3.8, b=1.6，使 a-b=2.2 與 b 有明顯視覺區別
        # =====================================================
        a = 3.8
        b = 1.6
        t = a - b          # 2.2
        L = a + b          # 5.4

        color_A = BLUE_D
        color_B = ORANGE
        color_col = TEAL_C
        color_L1 = PURPLE_C
        color_L2 = BLUE_C

        # 初始 3D 視角
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.85
        )

        # =====================================================
        # ① 一開始兩個立方體並列
        # =====================================================
        cap1 = self.make_caption(
            "先考慮邊長為", ("math", "a"),
            "與", ("math", "b"),
            "的兩個正方體"
        )
        self.play(FadeIn(cap1))

        pos_A = np.array([-1.5, 0.0, 0.0])
        cube_A = Cube(side_length=a)
        cube_A.move_to(pos_A)
        cube_A.set_fill(color_A, opacity=0.55)
        cube_A.set_stroke(BLUE_E, width=2)

        label_a3 = MathTex(r"a^3").scale(0.95)
        label_a3.move_to(pos_A + np.array([0, 0, a / 2 + 0.35]))
        self.add_fixed_orientation_mobjects(label_a3)

        # Cube B 最初位於右側
        init_pos_B = np.array([3.2, 0.0, -a / 2 + b / 2])
        cube_B = Cube(side_length=b)
        cube_B.move_to(init_pos_B)
        cube_B.set_fill(color_B, opacity=0.75)
        cube_B.set_stroke(ORANGE, width=2)

        label_b3 = MathTex(r"b^3").scale(0.85)
        label_b3.move_to(init_pos_B + np.array([0, 0, b / 2 + 0.35]))
        self.add_fixed_orientation_mobjects(label_b3)

        top_formula = self.make_top_formula(r"a^3 + b^3", scale=1.05)

        self.play(
            DrawBorderThenFill(cube_A),
            DrawBorderThenFill(cube_B),
            FadeIn(label_a3),
            FadeIn(label_b3),
            FadeIn(top_formula),
            run_time=2.0
        )
        self.wait(1.0)

        # =====================================================
        # ② 兩個立方體靠著角落貼合在一起
        # =====================================================
        self.play(FadeOut(cap1))
        cap2 = self.make_caption("將兩個正方體靠著角落緊密貼合在一起")
        self.play(FadeIn(cap2))

        # Cube A 範圍：
        # X: [-1.5 - a/2, -1.5 + a/2] = [-3.4, 0.4]
        # Y: [-a/2, a/2] = [-1.9, 1.9]
        # Z: [-a/2, a/2] = [-1.9, 1.9]
        # 角落座標（+X, +Y, 頂部 +Z）：
        # X corner: [0.4 - b, 0.4] = [-1.2, 0.4]，中心為 -0.4
        # Y corner: [1.9 - b, 1.9] = [0.3, 1.9]，中心為 1.1
        corner_x = pos_A[0] + a / 2 - b / 2   # -0.4
        corner_y = pos_A[1] + a / 2 - b / 2   # 1.1
        target_pos_B = np.array([corner_x, corner_y, a / 2 + b / 2])

        self.play(
            FadeOut(label_b3),
            cube_B.animate.move_to(target_pos_B),
            run_time=1.8
        )
        self.wait(0.8)

        # =====================================================
        # ③ 直接切出 b² × (a+b) 的角柱，並顯示長度標記
        # =====================================================
        self.play(FadeOut(cap2))
        cap3 = self.make_caption(
            "直接切出一根截面為", ("math", "b^2"),
            "、長度為", ("math", "a+b"),
            "的長方角柱"
        )
        self.play(FadeIn(cap3))

        # 預先在 Cube A 內部建立無縫拼接的三部分：
        # strip_inside_A: 尺寸 [b, b, a]，中心為 [corner_x, corner_y, 0]
        # part_L1: 尺寸 [t, a, a]，中心為 [pos_A[0] - a/2 + t/2, 0, 0] = [-2.3, 0, 0]
        # part_L2: 尺寸 [b, t, a]，中心為 [corner_x, pos_A[1] - a/2 + t/2, 0] = [-0.4, -0.8, 0]
        strip_inside_A = Prism(dimensions=[b, b, a])
        strip_inside_A.move_to(np.array([corner_x, corner_y, 0.0]))
        strip_inside_A.set_fill(color_col, opacity=0.75)
        strip_inside_A.set_stroke(TEAL_E, width=2)

        part_L1 = Prism(dimensions=[t, a, a])
        part_L1.move_to(np.array([pos_A[0] - a / 2 + t / 2, 0.0, 0.0]))
        part_L1.set_fill(color_L1, opacity=0.70)
        part_L1.set_stroke(PURPLE_E, width=2)

        part_L2 = Prism(dimensions=[b, t, a])
        part_L2.move_to(np.array([corner_x, pos_A[1] - a / 2 + t / 2, 0.0]))
        part_L2.set_fill(color_L2, opacity=0.70)
        part_L2.set_stroke(BLUE_E, width=2)

        # 無縫替換 cube_A
        self.remove(cube_A)
        self.add(part_L1, part_L2, strip_inside_A)

        # 組合整根角柱：strip_inside_A (長度 a) + cube_B (長度 b) = 總長 a+b
        full_column = VGroup(strip_inside_A, cube_B)

        # 抽出角柱向右方外移
        extract_offset = np.array([2.8, 0.6, 0.0])
        self.play(
            FadeOut(label_a3),
            full_column.animate.shift(extract_offset),
            run_time=2.0
        )

        col_center = np.array([corner_x, corner_y, b / 2]) + extract_offset
        # 標記：下段長度 a、上段長度 b、總長度 a+b、截面 b x b
        p_bot = col_center + np.array([b / 2 + 0.15, 0, -L / 2])
        p_mid = col_center + np.array([b / 2 + 0.15, 0, -L / 2 + a])
        p_top = col_center + np.array([b / 2 + 0.15, 0, L / 2])

        brace_a = BraceBetweenPoints(p_bot, p_mid, direction=RIGHT)
        label_brace_a = MathTex(r"a").scale(0.8).next_to(brace_a, RIGHT, buff=0.12)
        self.add_fixed_orientation_mobjects(label_brace_a)

        brace_b = BraceBetweenPoints(p_mid, p_top, direction=RIGHT)
        label_brace_b = MathTex(r"b").scale(0.8).next_to(brace_b, RIGHT, buff=0.12)
        self.add_fixed_orientation_mobjects(label_brace_b)

        label_col_sec = VGroup(
            Text("截面 ", font=CHINESE_FONT, font_size=22),
            MathTex(r"b \times b").scale(0.75)
        ).arrange(RIGHT, buff=0.1)
        label_col_sec.move_to(p_top + np.array([-b / 2, 0, 0.45]))
        self.add_fixed_orientation_mobjects(label_col_sec)

        self.play(
            GrowFromCenter(brace_a),
            FadeIn(label_brace_a),
            GrowFromCenter(brace_b),
            FadeIn(label_brace_b),
            FadeIn(label_col_sec),
            run_time=1.5
        )
        self.wait(1.5)

        # =====================================================
        # ④ 視角移到平面圖（先切換到 2D 俯視角）
        # =====================================================
        self.play(
            FadeOut(cap3),
            FadeOut(brace_a),
            FadeOut(label_brace_a),
            FadeOut(brace_b),
            FadeOut(label_brace_b),
            FadeOut(label_col_sec)
        )
        cap4 = self.make_caption("視角切換至平面圖，檢視剩下的 L 形截面")
        self.play(FadeIn(cap4))

        # 平滑過渡至頂部俯視角 (phi=0, theta=-90)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.92, run_time=2.0)
        self.wait(0.6)

        # =====================================================
        # ⑤ 在平面圖中展示外圍邊長 a 和被挖去的邊長 b
        # =====================================================
        self.play(FadeOut(cap4))
        cap5 = self.make_caption(
            "回頭看剩下的 L 形截面：外圍邊長為", ("math", "a"),
            "，被挖去的邊長為", ("math", "b")
        )
        self.play(FadeIn(cap5))

        z_top = a / 2 + 0.05
        # 外圍邊長 a 標記（底邊 X 從 -3.4 到 0.4）
        brace_outer_a = BraceBetweenPoints(
            np.array([-3.4, -1.9 - 0.15, z_top]),
            np.array([0.4, -1.9 - 0.15, z_top]),
            direction=DOWN
        )
        label_outer_a = MathTex(r"a").scale(0.85).next_to(brace_outer_a, DOWN, buff=0.1)
        self.add_fixed_orientation_mobjects(label_outer_a)

        # 被挖去角落的邊長 b 標記（內凹缺角處頂邊）
        brace_inner_b = BraceBetweenPoints(
            np.array([0.4 - b, 1.9 + 0.15, z_top]),
            np.array([0.4, 1.9 + 0.15, z_top]),
            direction=UP
        )
        label_inner_b = MathTex(r"b").scale(0.85).next_to(brace_inner_b, UP, buff=0.1)
        self.add_fixed_orientation_mobjects(label_inner_b)

        self.play(
            GrowFromCenter(brace_outer_a),
            FadeIn(label_outer_a),
            GrowFromCenter(brace_inner_b),
            FadeIn(label_inner_b),
            run_time=1.3
        )
        self.wait(1.5)

        # =====================================================
        # ⑥ 平面分割 L 形：面積說明寫在右邊空白處，不遮擋柱體
        # =====================================================
        self.play(
            FadeOut(cap5),
            FadeOut(brace_outer_a),
            FadeOut(label_outer_a),
            FadeOut(brace_inner_b),
            FadeOut(label_inner_b)
        )
        cap6 = self.make_caption(
            "將 L 形切成兩塊：一塊為", ("math", "(a-b) \\times a"),
            "，另一塊為", ("math", "b \\times (a-b)")
        )
        self.play(FadeIn(cap6))

        # 面積說明寫在右邊空白處 (X=2.1 處)，避免遮擋柱體
        desc_purple = VGroup(
            Dot(color=color_L1, radius=0.1),
            Text("紫色：", font=CHINESE_FONT, font_size=24),
            MathTex(r"(a-b) \times a").scale(0.85)
        ).arrange(RIGHT, buff=0.1)

        desc_blue = VGroup(
            Dot(color=color_L2, radius=0.1),
            Text("藍色：", font=CHINESE_FONT, font_size=24),
            MathTex(r"b \times (a-b)").scale(0.85)
        ).arrange(RIGHT, buff=0.1)

        desc_box = VGroup(desc_purple, desc_blue).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        desc_box.move_to(np.array([2.1, -0.6, z_top]))
        self.add_fixed_orientation_mobjects(desc_box)

        self.play(FadeIn(desc_box), run_time=1.2)
        self.wait(1.2)

        # =====================================================
        # ⑦ 剛體重組：藍色方塊直接往上移動並旋轉 90度，拼接在紫色上方
        # =====================================================
        self.play(FadeOut(cap6))
        cap7 = self.make_caption(
            "藍色長方形直接往上移並旋轉，重組為", ("math", "(a+b) \\times (a-b)")
        )
        self.play(FadeIn(cap7))

        target_pos_L2_2D = np.array([
            pos_A[0] - a / 2 + t / 2,   # -2.3
            a / 2 + b / 2,              # 2.7
            0.0
        ])

        # 藍方塊分離時直接向上移 -> 原地旋轉 90度 -> 平移無縫接在紫色頂部
        self.play(
            part_L2.animate.shift(UP * 2.5),
            run_time=1.0
        )
        self.play(
            Rotate(part_L2, angle=90 * DEGREES, axis=OUT, about_point=part_L2.get_center()),
            run_time=1.0
        )
        self.play(
            part_L2.animate.move_to(target_pos_L2_2D),
            run_time=1.2
        )

        # 右側說明平滑變更為拼合總面積
        desc_total = VGroup(
            Text("拼合總面積：", font=CHINESE_FONT, font_size=24),
            MathTex(r"(a+b)(a-b)").scale(0.88).set_color(YELLOW)
        ).arrange(RIGHT, buff=0.1)
        desc_total.move_to(np.array([2.1, -0.6, z_top]))
        self.add_fixed_orientation_mobjects(desc_total)

        # 標註重組後的長邊 a+b 與短邊 a-b
        brace_recomb_L = BraceBetweenPoints(
            np.array([pos_A[0] - a / 2 - 0.15, -a / 2, z_top]),
            np.array([pos_A[0] - a / 2 - 0.15, a / 2 + b, z_top]),
            direction=LEFT
        )
        label_recomb_L = MathTex(r"a+b").scale(0.85).next_to(brace_recomb_L, LEFT, buff=0.12)
        self.add_fixed_orientation_mobjects(label_recomb_L)

        brace_recomb_W = BraceBetweenPoints(
            np.array([pos_A[0] - a / 2, -a / 2 - 0.15, z_top]),
            np.array([pos_A[0] - a / 2 + t, -a / 2 - 0.15, z_top]),
            direction=DOWN
        )
        label_recomb_W = MathTex(r"a-b").scale(0.85).next_to(brace_recomb_W, DOWN, buff=0.12)
        self.add_fixed_orientation_mobjects(label_recomb_W)

        self.play(
            ReplacementTransform(desc_box, desc_total),
            GrowFromCenter(brace_recomb_L),
            FadeIn(label_recomb_L),
            GrowFromCenter(brace_recomb_W),
            FadeIn(label_recomb_W),
            run_time=1.4
        )
        self.wait(1.8)

        # =====================================================
        # ⑧ 回到 3D 視角：長方體向另一方向旋轉 90度（+90度）
        #    讓藍色與橘色（高 b）在上方對齊，紫色與綠色（高 a）在下方對齊！
        # =====================================================
        self.play(FadeOut(cap7))
        cap8 = self.make_caption(
            "回到立體視角，將兩大長方體旋轉對齊，共同長度為", ("math", "a+b")
        )
        self.play(FadeIn(cap8))

        self.play(
            FadeOut(brace_recomb_L),
            FadeOut(label_recomb_L),
            FadeOut(brace_recomb_W),
            FadeOut(label_recomb_W),
            FadeOut(desc_total)
        )
        # 相機以 theta=-90 正對前方平滑升起至 phi=75
        self.move_camera(phi=75 * DEGREES, theta=-90 * DEGREES, zoom=0.82, run_time=2.0)

        # 將重組後的 L形角柱 (part_L1 + part_L2) 與抽出的角柱 (full_column) 確實對齊：
        # 1. c2_group 繞 X 軸向正方向旋轉 90 度，使藍色 (b) 升至上方，紫色 (a) 落於下方
        # 2. full_column 亦為橘色 (b) 在上、綠色 (a) 在下，兩者分層高度完全同步！
        c2_group = VGroup(part_L1, part_L2)
        flush_pos_c2 = np.array([-t / 2, 0.0, 0.0])
        initial_pos_c2 = flush_pos_c2 + LEFT * 0.9

        flush_pos_col = np.array([b / 2, -a / 2 + b / 2, 0.0])
        initial_pos_col = flush_pos_col + RIGHT * 0.9

        # 向正方向旋轉 90 度 (+90度)
        self.play(
            Rotate(c2_group, angle=90 * DEGREES, axis=RIGHT),
            run_time=1.4
        )
        self.play(
            c2_group.animate.move_to(initial_pos_c2),
            full_column.animate.move_to(initial_pos_col),
            run_time=1.6
        )

        # 標註確實對齊後的共同高度 a+b（位於右側柱體右緣）
        p_brace_bot = np.array([initial_pos_col[0] + b / 2 + 0.25, -a / 2 + b / 2, -L / 2])
        p_brace_top = np.array([initial_pos_col[0] + b / 2 + 0.25, -a / 2 + b / 2, L / 2])
        arrow_common_H = DoubleArrow(p_brace_bot, p_brace_top, tip_length=0.18, color=YELLOW, buff=0)
        label_common_H = VGroup(
            Text("共同長度 = ", font=CHINESE_FONT, font_size=24),
            MathTex(r"a+b").scale(0.85)
        ).arrange(RIGHT, buff=0.1)
        label_common_H.next_to(arrow_common_H, RIGHT, buff=0.15)
        self.add_fixed_orientation_mobjects(label_common_H)

        self.play(
            GrowFromCenter(arrow_common_H),
            FadeIn(label_common_H),
            run_time=1.2
        )
        self.wait(1.5)

        # 兩大柱體平移拼合，在 X=0 處無縫貼合，藍色橘色齊平在上方，紫色綠色齊平在下方！
        self.play(
            FadeOut(arrow_common_H),
            FadeOut(label_common_H),
            c2_group.animate.move_to(flush_pos_c2),
            full_column.animate.move_to(flush_pos_col),
            run_time=1.5
        )
        self.wait(1.0)

        # =====================================================
        # ⑦ 檢視頂部截面積：對齊後的組合截面為 a(a-b) + b²
        # =====================================================
        self.play(FadeOut(cap8))
        cap9 = self.make_caption("觀察對齊後的頂部截面，總截面積為", ("math", "a(a-b) + b^2"))
        self.play(FadeIn(cap9))

        # 純仰俯運鏡垂直俯視頂部截面 (phi=0, theta=-90)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.92, run_time=2.0)

        # 頂部截面面積標註（正對各塊頂面中心）
        z_top = L / 2 + 0.05
        sec_label_1 = MathTex(r"a(a-b)").scale(0.88).set_color(YELLOW)
        sec_label_1.move_to(np.array([-t / 2, 0.0, z_top]))
        self.add_fixed_orientation_mobjects(sec_label_1)

        sec_label_2 = MathTex(r"b^2").scale(0.88).set_color(YELLOW)
        sec_label_2.move_to(np.array([b / 2, -a / 2 + b / 2, z_top]))
        self.add_fixed_orientation_mobjects(sec_label_2)

        # 虛線框標註缺角矩形 b × (a-b)，直觀輔助理解 (a-b)a + b² = a² - ab + b²
        missing_corner = DashedVMobject(
            Rectangle(width=b, height=a - b).set_stroke(YELLOW, width=2, opacity=0.75),
            num_dashes=16
        )
        missing_corner.move_to(np.array([b / 2, a / 2 - (a - b) / 2, z_top]))

        formula_top_sec = self.make_top_formula(r"a(a-b) + b^2", scale=1.0)

        self.play(
            FadeOut(top_formula),
            FadeIn(formula_top_sec),
            FadeIn(sec_label_1),
            FadeIn(sec_label_2),
            Create(missing_corner),
            run_time=1.5
        )
        self.wait(1.5)

        # =====================================================
        # ⑧ 化簡截面積為 a² - ab + b²
        # =====================================================
        self.play(FadeOut(cap9))
        cap10 = self.make_caption(
            "展開並化簡截面積：", ("math", "a(a-b) + b^2 = a^2 - ab + b^2")
        )
        self.play(FadeIn(cap10))

        formula_simplified = self.make_top_formula(r"a^2 - ab + b^2", scale=1.0)

        self.play(
            TransformMatchingTex(formula_top_sec, formula_simplified),
            run_time=1.6
        )
        self.wait(1.5)

        # =====================================================
        # ⑨ 得到立方和公式：(a+b)(a²-ab+b²)
        # =====================================================
        self.play(FadeOut(cap10))
        cap_final = self.make_caption("總體積等於底面積乘上高，由此證得立方和公式！")

        self.play(
            FadeIn(cap_final),
            FadeOut(sec_label_1),
            FadeOut(sec_label_2),
            FadeOut(missing_corner)
        )
        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=0.82, run_time=2.0)

        # 3B1B 步進展開
        f_mid = MathTex(
            r"(a+b)",
            r"(a^2 - ab + b^2)"
        ).scale(1.0).to_edge(UP, buff=0.45)
        f_mid[0].set_color(YELLOW)
        f_mid[1].set_color(WHITE)
        self.camera.add_fixed_in_frame_mobjects(f_mid)

        self.play(
            ReplacementTransform(formula_simplified, f_mid[1]),
            FadeIn(f_mid[0], shift=RIGHT * 0.3),
            run_time=1.3
        )
        self.wait(1.0)

        f_final = MathTex(
            r"a^3 + b^3",
            r"=",
            r"(a+b)",
            r"(a^2 - ab + b^2)"
        ).scale(1.05).to_edge(UP, buff=0.45).set_color(YELLOW)
        self.camera.add_fixed_in_frame_mobjects(f_final)

        self.play(
            ReplacementTransform(f_mid[0], f_final[2]),
            ReplacementTransform(f_mid[1], f_final[3]),
            FadeIn(f_final[0:2], shift=RIGHT * 0.3),
            run_time=1.3
        )

        final_box = SurroundingRectangle(f_final, buff=0.22, color=YELLOW)
        self.camera.add_fixed_in_frame_mobjects(final_box)

        self.play(Create(final_box), run_time=1.5)
        self.wait(5.0)
