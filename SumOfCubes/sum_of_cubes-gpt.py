from manim import *
import numpy as np


CHINESE_FONT = "GenSekiGothic TW"
CAPTION_SIZE = 30
BG_COLOR = "#1E1E1E"


class SumOfCubesGpt(ThreeDScene):

    # =========================================================
    # HUD helpers
    # =========================================================
    def make_caption(self, text, formula=None):
        parts = [
            Text(
                text,
                font=CHINESE_FONT,
                font_size=CAPTION_SIZE,
            )
        ]

        if formula:
            parts.append(
                MathTex(formula).scale(0.9)
            )

        group = VGroup(*parts).arrange(
            RIGHT,
            buff=0.18
        )
        group.to_edge(DOWN, buff=0.45)
        return group

    def change_caption(self, old, new):
        self.add_fixed_in_frame_mobjects(new)
        self.play(
            FadeOut(old),
            FadeIn(new),
            run_time=0.4
        )
        return new

    def make_top_formula(self, tex, scale=1.0, color=YELLOW):
        obj = MathTex(tex).scale(scale)
        obj.set_color(color)
        obj.to_edge(UP, buff=0.45)
        return obj

    def change_formula(self, old, new):
        self.add_fixed_in_frame_mobjects(new)
        self.play(
            FadeOut(old),
            FadeIn(new),
            run_time=0.5
        )
        return new

    # =========================================================
    # MAIN
    # =========================================================
    def construct(self):

        config.background_color = BG_COLOR

        # =====================================================
        # Geometry
        # =====================================================
        a = 4.0
        b = 2.0
        d = a - b

        COLOR_A = BLUE_D
        COLOR_B = RED
        COLOR_COLUMN1 = ORANGE
        COLOR_L1 = PURPLE
        COLOR_L2 = GREEN
        COLOR_COLUMN2 = GOLD

        # -----------------------------------------------------
        # Coordinate convention
        #
        # Big cube A:
        # x from -a to 0
        # y from -a/2 to +a/2
        # z from -a/2 to +a/2
        #
        # Camera sees front-lower corner near:
        # y = -a/2
        # z = -a/2
        #
        # Small cube B attaches at A's right-front-lower corner.
        # -----------------------------------------------------

        big_center = np.array([
            -a / 2,
            0,
            0
        ])

        small_center = np.array([
            b / 2,
            -a / 2 + b / 2,
            -a / 2 + b / 2
        ])

        # =====================================================
        # 1. Initial isometric view
        # =====================================================
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.90
        )

        caption = self.make_caption(
            "先把兩個立方體沿同一條前下緣排好"
        )
        self.add_fixed_in_frame_mobjects(caption)

        cube_a = Cube(side_length=a)
        cube_a.move_to(big_center)
        cube_a.set_fill(COLOR_A, opacity=0.45)
        cube_a.set_stroke(BLUE_E, width=2)

        cube_b = Cube(side_length=b)
        cube_b.move_to(small_center)
        cube_b.set_fill(COLOR_B, opacity=0.70)
        cube_b.set_stroke(RED_E, width=2)

        label_a = MathTex(r"a^3").scale(0.95)
        label_b = MathTex(r"b^3").scale(0.90)

        label_a.move_to(big_center + OUT * 2.4)
        label_b.move_to(small_center + OUT * 1.3)

        self.add_fixed_orientation_mobjects(
            label_a,
            label_b
        )

        top_formula = self.make_top_formula(
            r"a^3+b^3",
            scale=1.05
        )
        self.add_fixed_in_frame_mobjects(top_formula)

        self.play(
            FadeIn(caption),
            DrawBorderThenFill(cube_a),
            DrawBorderThenFill(cube_b),
            FadeIn(label_a),
            FadeIn(label_b),
            FadeIn(top_formula),
            run_time=1.6
        )

        self.wait(0.8)

        # =====================================================
        # Mark a+b along the front-lower aligned edge
        # =====================================================
        front_y = -a / 2
        lower_z = -a / 2

        length_line = Line3D(
            start=np.array([-a, front_y - 0.30, lower_z]),
            end=np.array([b, front_y - 0.30, lower_z]),
            color=YELLOW,
            thickness=0.025
        )

        length_label = MathTex(r"a+b").scale(0.85)
        length_label.move_to(
            np.array([
                (b - a) / 2,
                front_y - 0.65,
                lower_z
            ])
        )
        self.add_fixed_orientation_mobjects(length_label)

        new_caption = self.make_caption(
            "這條前下緣的總長度就是",
            r"a+b"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(
            Create(length_line),
            FadeIn(length_label)
        )
        self.wait(1.0)

        # =====================================================
        # 2. Only now cut out the a × b × b prism
        # =====================================================
        new_caption = self.make_caption(
            "現在才從大立方體切出一根底面為",
            r"b^2"
        )
        caption = self.change_caption(caption, new_caption)

        # This prism occupies the front-lower b × b corner
        # and extends the full length a along x.
        slab_center = np.array([
            -a / 2,
            -a / 2 + b / 2,
            -a / 2 + b / 2
        ])

        slab = Prism(dimensions=[a, b, b])
        slab.move_to(slab_center)
        slab.set_fill(COLOR_COLUMN1, opacity=0.0)
        slab.set_stroke(ORANGE, width=2, opacity=0.0)
        self.add(slab)

        self.play(
            slab.animate
            .set_fill(COLOR_COLUMN1, opacity=0.78)
            .set_stroke(ORANGE, opacity=1),
            run_time=1.1
        )

        self.wait(0.5)

        # =====================================================
        # Replace A with:
        # - slab
        # - L-shaped remaining prism represented by two prisms
        #
        # They remain visually assembled.
        # =====================================================
        l1 = Prism(dimensions=[a, d, a])
        l1.move_to(
            np.array([
                -a / 2,
                b / 2,
                0
            ])
        )
        l1.set_fill(COLOR_L1, opacity=0.67)
        l1.set_stroke(PURPLE_E, width=2)

        l2 = Prism(dimensions=[a, b, d])
        l2.move_to(
            np.array([
                -a / 2,
                -a / 2 + b / 2,
                b / 2
            ])
        )
        l2.set_fill(COLOR_L2, opacity=0.70)
        l2.set_stroke(GREEN_E, width=2)

        self.play(
            FadeOut(cube_a),
            FadeOut(label_a),
            FadeIn(l1),
            FadeIn(l2),
            run_time=0.8
        )

        self.wait(0.4)

        # =====================================================
        # slab + cube_b = b²(a+b)
        # =====================================================
        new_caption = self.make_caption(
            "這根角柱與小立方體合在一起，形成"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(
            slab.animate.set_fill(
                COLOR_COLUMN1,
                opacity=0.82
            ),
            cube_b.animate.set_fill(
                COLOR_COLUMN1,
                opacity=0.82
            ),
            FadeOut(label_b),
            run_time=0.5
        )

        column1_label = MathTex(
            r"b^2(a+b)"
        ).scale(0.9)

        column1_label.move_to(
            np.array([
                (b - a) / 2,
                front_y - 1.0,
                lower_z + 0.8
            ])
        )

        self.add_fixed_orientation_mobjects(
            column1_label
        )

        self.play(FadeIn(column1_label))
        self.wait(0.8)

        # =====================================================
        # Move the completed b²(a+b) column away
        # =====================================================
        new_caption = self.make_caption(
            "先把這根完成的柱體移到一旁"
        )
        caption = self.change_caption(caption, new_caption)

        column1_group = VGroup(
            slab,
            cube_b
        )

        move_column1 = RIGHT * 4.0 + UP * 0.8

        self.play(
            column1_group.animate.shift(move_column1),
            column1_label.animate.shift(move_column1),
            run_time=1.2
        )

        self.play(
            FadeOut(length_line),
            FadeOut(length_label),
            FadeOut(column1_label)
        )

        self.wait(0.4)

        # =====================================================
        # 3. Focus on L-shaped base
        # =====================================================
        new_caption = self.make_caption(
            "接著只看剩下凹形柱的底面"
        )
        caption = self.change_caption(caption, new_caption)

        # Look along the x-axis toward the L-shaped cross section
        self.move_camera(
            phi=90 * DEGREES,
            theta=0 * DEGREES,
            zoom=1.05,
            run_time=1.8
        )

        self.wait(0.6)

        # =====================================================
        # Label outer a and inner b
        # =====================================================
        outer_a_h = MathTex(r"a").scale(0.85)
        outer_a_v = MathTex(r"a").scale(0.85)
        inner_b_h = MathTex(r"b").scale(0.85)
        inner_b_v = MathTex(r"b").scale(0.85)

        # Since camera is looking along x,
        # y/z act like 2D coordinates on screen.
        outer_a_h.move_to(
            np.array([
                -a / 2,
                0,
                a / 2 + 0.45
            ])
        )

        outer_a_v.move_to(
            np.array([
                -a / 2,
                -a / 2 - 0.45,
                0
            ])
        )

        inner_b_h.move_to(
            np.array([
                -a / 2,
                -a / 2 + b / 2,
                -a / 2 + b + 0.40
            ])
        )

        inner_b_v.move_to(
            np.array([
                -a / 2,
                -a / 2 + b + 0.40,
                -a / 2 + b / 2
            ])
        )

        self.add_fixed_orientation_mobjects(
            outer_a_h,
            outer_a_v,
            inner_b_h,
            inner_b_v
        )

        new_caption = self.make_caption(
            "外正方形邊長是",
            r"a"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(
            FadeIn(outer_a_h),
            FadeIn(outer_a_v)
        )
        self.wait(0.6)

        new_caption = self.make_caption(
            "挖去的小正方形邊長是",
            r"b"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(
            FadeIn(inner_b_h),
            FadeIn(inner_b_v)
        )
        self.wait(0.8)

        base_formula = self.make_top_formula(
            r"a^2-b^2",
            scale=1.0,
            color=WHITE
        )
        top_formula = self.change_formula(
            top_formula,
            base_formula
        )

        self.wait(0.8)

        # =====================================================
        # The L cross section is already represented by l1 and l2.
        #
        # l1 cross section: (a-b) × a
        # l2 cross section: b × (a-b)
        #
        # We now make the cut visually explicit.
        # =====================================================
        new_caption = self.make_caption(
            "沿著缺角邊緣切開，就得到兩個長方形"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(
            l1.animate.set_fill(
                COLOR_L1,
                opacity=0.82
            ),
            l2.animate.set_fill(
                COLOR_L2,
                opacity=0.82
            ),
            run_time=0.6
        )

        self.wait(0.6)

        self.play(
            FadeOut(outer_a_h),
            FadeOut(outer_a_v),
            FadeOut(inner_b_h),
            FadeOut(inner_b_v)
        )

        # =====================================================
        # Return to 3D perspective
        # =====================================================
        self.move_camera(
            phi=65 * DEGREES,
            theta=-30 * DEGREES,
            zoom=0.95,
            run_time=1.5
        )

        self.wait(0.4)

        # =====================================================
        # Correct rigid rearrangement of a²-b²
        #
        # Keep l1 in place.
        # Pull l2 out along x-ish direction,
        # rotate it 90 degrees about the x-axis,
        # then slide it next to l1.
        # =====================================================
        new_caption = self.make_caption(
            "先把較小的一塊抽離"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(
            l2.animate.shift(
                OUT * 1.5 + UP * 0.6
            ),
            run_time=0.9
        )

        self.wait(0.3)

        new_caption = self.make_caption(
            "再沿柱子的長軸旋轉九十度"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(
            Rotate(
                l2,
                angle=PI / 2,
                axis=RIGHT,
                about_point=l2.get_center()
            ),
            run_time=1.1
        )

        self.wait(0.3)

        # =====================================================
        # Reassemble cross section into (a+b) × (a-b)
        #
        # After rotation:
        # l2 has orientation a × d × b
        #
        # l1 is a × d × a
        #
        # Put them side-by-side along z,
        # so total z-length becomes a+b.
        # =====================================================
        new_caption = self.make_caption(
            "把它平移到另一塊旁邊，拼成一個完整長方形"
        )
        caption = self.change_caption(caption, new_caption)

        target_center = np.array([
            -1.0,
            0,
            0
        ])

        l1_target = target_center + IN * (b / 2)
        l2_target = target_center + OUT * (a / 2)

        self.play(
            l1.animate.move_to(l1_target),
            l2.animate.move_to(l2_target),
            run_time=1.2
        )

        column2_group = VGroup(
            l1,
            l2
        )

        self.play(
            l1.animate.set_fill(
                COLOR_COLUMN2,
                opacity=0.78
            ),
            l2.animate.set_fill(
                COLOR_COLUMN2,
                opacity=0.78
            ),
            run_time=0.5
        )

        column2_label = MathTex(
            r"a(a+b)(a-b)"
        ).scale(0.85)

        column2_label.move_to(
            column2_group.get_center()
            + UP * 2.0
        )

        self.add_fixed_orientation_mobjects(
            column2_label
        )

        new_caption = self.make_caption(
            "這根柱體的體積就是"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(FadeIn(column2_label))
        self.wait(0.8)

        # =====================================================
        # 4. Bring back b²(a+b) column
        # =====================================================
        new_caption = self.make_caption(
            "現在把剛才移開的柱體帶回來"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(
            FadeOut(column2_label)
        )

        # bring column 1 back near column 2
        self.play(
            column1_group.animate.shift(
                -move_column1 + RIGHT * 2.0
            ),
            run_time=1.2
        )

        self.wait(0.4)

        # =====================================================
        # Rotate b²(a+b) column so its a+b direction matches
        # column2's a+b direction.
        # =====================================================
        new_caption = self.make_caption(
            "旋轉第一根柱體，讓兩者的",
            r"a+b",
        )
        caption = self.change_caption(caption, new_caption)

        # rotate around Y axis
        self.play(
            Rotate(
                column1_group,
                angle=PI / 2,
                axis=UP,
                about_point=column1_group.get_center()
            ),
            run_time=1.1
        )

        self.wait(0.3)

        # =====================================================
        # Slide column1 to touch column2
        # =====================================================
        new_caption = self.make_caption(
            "最後平移，讓兩根柱體沿著共同長度貼合"
        )
        caption = self.change_caption(caption, new_caption)

        # Put column2 on left, column1 on right
        column2_group.generate_target()
        column2_group.target.move_to(
            LEFT * 1.6
        )

        column1_group.generate_target()
        column1_group.target.move_to(
            RIGHT * 1.6
        )

        self.play(
            MoveToTarget(column2_group),
            MoveToTarget(column1_group),
            run_time=1.2
        )

        self.wait(0.5)

        # =====================================================
        # Align camera to emphasize common a+b
        # =====================================================
        self.move_camera(
            phi=82 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.92,
            run_time=1.6
        )

        self.wait(0.5)

        common_label_1 = MathTex(r"a+b").scale(0.8)
        common_label_2 = MathTex(r"a+b").scale(0.8)

        common_label_1.move_to(
            column1_group.get_center()
            + DOWN * 1.6
        )

        common_label_2.move_to(
            column2_group.get_center()
            + DOWN * 1.6
        )

        self.add_fixed_orientation_mobjects(
            common_label_1,
            common_label_2
        )

        new_caption = self.make_caption(
            "現在兩根柱體都有共同長度",
            r"a+b"
        )
        caption = self.change_caption(caption, new_caption)

        self.play(
            FadeIn(common_label_1),
            FadeIn(common_label_2)
        )

        self.wait(0.8)

        # =====================================================
        # Formula only now
        # =====================================================
        formula1 = self.make_top_formula(
            r"(a+b)\left[a(a-b)+b^2\right]",
            scale=0.95,
            color=YELLOW
        )
        top_formula = self.change_formula(
            top_formula,
            formula1
        )

        new_caption = self.make_caption(
            "所以總體積可以直接提出共同因子"
        )
        caption = self.change_caption(caption, new_caption)

        self.wait(1.0)

        formula2 = self.make_top_formula(
            r"(a+b)(a^2-ab+b^2)",
            scale=1.0,
            color=YELLOW
        )
        top_formula = self.change_formula(
            top_formula,
            formula2
        )

        self.wait(1.0)

        # =====================================================
        # Final identity
        # =====================================================
        final_formula = self.make_top_formula(
            r"a^3+b^3=(a+b)(a^2-ab+b^2)",
            scale=1.08,
            color=YELLOW
        )
        top_formula = self.change_formula(
            top_formula,
            final_formula
        )

        final_caption = self.make_caption(
            "因此得到立方和公式"
        )
        caption = self.change_caption(
            caption,
            final_caption
        )

        self.play(
            FadeOut(common_label_1),
            FadeOut(common_label_2)
        )

        final_box = SurroundingRectangle(
            final_formula,
            buff=0.2,
            color=YELLOW
        )
        self.add_fixed_in_frame_mobjects(final_box)

        self.play(
            Create(final_box),
            run_time=0.8
        )

        self.wait(3)