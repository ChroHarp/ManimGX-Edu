from manimgx import *
import numpy as np

CHINESE_FONT = "GenSekiGothic TW"

class AngleSumDifferenceGX(Scene):
    def make_caption(self, *items):
        """底部繁中與數學公式混排字幕，統一字體大小與水平對齊"""
        parts = []
        for item in items:
            if isinstance(item, Mobject):
                parts.append(item)
            elif isinstance(item, tuple) and item[0] == "math":
                parts.append(MathTex(item[1], font_size=25))
            else:
                parts.append(Text(str(item), font=CHINESE_FONT, font_size=23))
        group = VGroup(*parts).arrange(RIGHT, buff=0.10)
        group.to_edge(DOWN, buff=0.65)
        return group

    def set_caption(self, new_caption, run_time=0.4):
        """平滑切換字幕：舊字幕淡出、新字幕淡入，解決文字形變飄移問題"""
        if hasattr(self, "current_caption") and self.current_caption is not None:
            old_caption = self.current_caption
            self.current_caption = new_caption
            self.play(
                FadeOut(old_caption, shift=DOWN * 0.08),
                FadeIn(new_caption, shift=UP * 0.08),
                run_time=run_time
            )
        else:
            self.current_caption = new_caption
            self.play(FadeIn(new_caption, shift=UP * 0.08), run_time=run_time)

    def make_right_angle(self, corner, p1, p2, size=0.22, color=WHITE):
        """直角符號輔助函式"""
        v1 = (p1 - corner) / np.linalg.norm(p1 - corner)
        v2 = (p2 - corner) / np.linalg.norm(p2 - corner)
        p_a = corner + v1 * size
        p_b = corner + v1 * size + v2 * size
        p_c = corner + v2 * size
        return VMobject().set_points_as_corners([p_a, p_b, p_c]).set_stroke(color, 1.8)

    def make_step_title(self, prefix_math, label_text, math_expr, pos, color=BLUE_B):
        """混合排版標題（支援 LaTeX 符號與中文，符合台灣線段記號）"""
        parts = []
        if prefix_math:
            parts.append(MathTex(prefix_math, font_size=24, color=color))
        parts.append(Text(label_text, font=CHINESE_FONT, font_size=22, color=color))
        parts.append(MathTex(math_expr, font_size=24, color=WHITE))
        grp = VGroup(*parts).arrange(RIGHT, buff=0.10).move_to(pos)
        return grp

    def construct(self):
        # =====================================================
        # 0. 全局幾何參數與調色盤
        # =====================================================
        alpha_deg = 40.0
        beta_deg = 22.0
        alpha = np.radians(alpha_deg)
        beta = np.radians(beta_deg)
        sum_ang = alpha + beta
        diff_ang = alpha - beta

        # 縮放長度（AF = R = 3.9）
        R = 3.9
        cos_b = np.cos(beta)
        sin_b = np.sin(beta)
        cos_a = np.cos(alpha)
        sin_a = np.sin(alpha)

        # 顏色體系
        C_BLUE = "#3498DB"       # 主三角形 AEF (beta)
        C_BLUE_STROKE = "#85C1E9"
        C_YELLOW = "#F39C12"     # 底部三角形 ABE (alpha * cos_beta)
        C_YELLOW_STROKE = "#FAD7A0"
        C_PINK = "#E91E63"       # 右上三角形 EFC (alpha * sin_beta)
        C_PINK_STROKE = "#F48FB1"
        C_RECT = "#95A5A6"       # 外框矩形
        C_HL_A = "#FFE600"       # 高亮色金黃
        C_HL_B = "#00E676"       # 高亮色亮綠
        C_HL_C = "#FF5252"       # 高亮色亮紅

        # =====================================================
        # 鏡頭 0：片頭標題與目標
        # =====================================================
        title_main = Text("和角與差角公式的幾何圖解", font=CHINESE_FONT, font_size=36, weight=BOLD).set_color(YELLOW_C)
        title_sub = MathTex(
            r"\sin(\alpha \pm \beta) = {?}, \qquad \cos(\alpha \pm \beta) = {?}",
            font_size=30, color=BLUE_B
        )
        title_grp = VGroup(title_main, title_sub).arrange(DOWN, buff=0.35)
        
        self.play(FadeIn(title_grp, shift=UP * 0.3), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(title_grp, shift=UP * 0.5), run_time=0.8)

        # 頂部 HUD 標題
        hud_title = Text("和角公式的幾何推導", font=CHINESE_FONT, font_size=24, weight=BOLD).set_color(YELLOW_C)
        hud_title.to_edge(UP, buff=0.25)
        self.play(FadeIn(hud_title), run_time=0.6)

        # =====================================================
        # 鏡頭 1：先出現兩個「單位直角三角形」
        # =====================================================
        cap1 = self.make_caption("準備兩個斜邊為 1 的單位直角三角形")
        self.set_caption(cap1, run_time=0.6)

        # 左側 alpha 單位三角形
        u_scale = 2.4
        o_left = np.array([-4.5, -0.8, 0])
        p_a1 = o_left
        p_b1 = o_left + np.array([u_scale * cos_a, 0, 0])
        p_e1 = o_left + np.array([u_scale * cos_a, u_scale * sin_a, 0])
        tri_alpha = Polygon(p_a1, p_b1, p_e1, fill_color=C_YELLOW, fill_opacity=0.35, stroke_color=C_YELLOW_STROKE, stroke_width=2.5)
        ra_1 = self.make_right_angle(p_b1, p_a1, p_e1, size=0.2)
        arc_a1 = Arc(start_angle=0, angle=alpha, radius=0.6, arc_center=p_a1, color=YELLOW)
        lbl_a1 = MathTex(r"\alpha", font_size=22, color=YELLOW).next_to(arc_a1, RIGHT, buff=0.08).shift(UP * 0.08)
        mid_hyp_1 = (p_a1 + p_e1) / 2
        lbl_h1 = MathTex("1", font_size=22, color=WHITE).move_to(mid_hyp_1 + 0.22 * np.array([-sin_a, cos_a, 0]))
        lbl_w1 = MathTex(r"\cos\alpha", font_size=22, color=C_YELLOW_STROKE).next_to(tri_alpha, DOWN, buff=0.15)
        lbl_v1 = MathTex(r"\sin\alpha", font_size=22, color=C_YELLOW_STROKE).next_to(tri_alpha, RIGHT, buff=0.15)
        grp_unit_alpha = VGroup(tri_alpha, ra_1, arc_a1, lbl_a1, lbl_h1, lbl_w1, lbl_v1)

        # 右側 beta 單位三角形
        o_right = np.array([1.5, -0.8, 0])
        p_a2 = o_right
        p_b2 = o_right + np.array([u_scale * cos_b, 0, 0])
        p_e2 = o_right + np.array([u_scale * cos_b, u_scale * sin_b, 0])
        tri_beta = Polygon(p_a2, p_b2, p_e2, fill_color=C_BLUE, fill_opacity=0.35, stroke_color=C_BLUE_STROKE, stroke_width=2.5)
        ra_2 = self.make_right_angle(p_b2, p_a2, p_e2, size=0.2)
        arc_b2 = Arc(start_angle=0, angle=beta, radius=0.7, arc_center=p_a2, color=BLUE_B)
        lbl_b2 = MathTex(r"\beta", font_size=22, color=BLUE_B).next_to(arc_b2, RIGHT, buff=0.08).shift(UP * 0.08)
        mid_hyp_2 = (p_a2 + p_e2) / 2
        lbl_h2 = MathTex("1", font_size=22, color=WHITE).move_to(mid_hyp_2 + 0.22 * np.array([-sin_b, cos_b, 0]))
        lbl_w2 = MathTex(r"\cos\beta", font_size=22, color=C_BLUE_STROKE).next_to(tri_beta, DOWN, buff=0.15)
        lbl_v2 = MathTex(r"\sin\beta", font_size=22, color=C_BLUE_STROKE).next_to(tri_beta, RIGHT, buff=0.15)
        grp_unit_beta = VGroup(tri_beta, ra_2, arc_b2, lbl_b2, lbl_h2, lbl_w2, lbl_v2)

        self.play(Create(tri_alpha), Create(tri_beta), run_time=1.0)
        self.play(
            FadeIn(ra_1), FadeIn(arc_a1), FadeIn(lbl_a1), FadeIn(lbl_h1), FadeIn(lbl_w1), FadeIn(lbl_v1),
            FadeIn(ra_2), FadeIn(arc_b2), FadeIn(lbl_b2), FadeIn(lbl_h2), FadeIn(lbl_w2), FadeIn(lbl_v2),
            run_time=0.8
        )
        self.wait(1.5)

        # =====================================================
        # 鏡頭 2：以 beta 三角形作骨架（剛體變換到位，兩股標籤移入內側）
        # =====================================================
        cap2 = self.make_caption("以", ("math", r"\beta"), "三角形為藍色骨架，旋轉", ("math", r"\alpha"), "角放置於中央")
        self.set_caption(cap2)

        p_A = np.array([-4.2, -1.9, 0])
        p_E = p_A + np.array([R * cos_b * cos_a, R * cos_b * sin_a, 0])
        p_F = p_A + np.array([R * np.cos(sum_ang), R * np.sin(sum_ang), 0])

        tri_AEF = Polygon(p_A, p_E, p_F, fill_color=C_BLUE, fill_opacity=0.4, stroke_color=C_BLUE_STROKE, stroke_width=2.5)
        ra_E = self.make_right_angle(p_E, p_A, p_F, size=0.22)
        
        lbl_AF = MathTex("1", font_size=22, color=WHITE).move_to(
            (p_A + p_F)/2 + 0.25 * np.array([-np.sin(sum_ang), np.cos(sum_ang), 0])
        )
        lbl_AE = MathTex(r"\cos\beta", font_size=22, color=C_BLUE_STROKE).move_to(
            (p_A + p_E)/2 + 0.30 * np.array([-sin_a, cos_a, 0])
        )
        lbl_EF = MathTex(r"\sin\beta", font_size=22, color=C_BLUE_STROKE).move_to(
            (p_E + p_F)/2 + 0.35 * np.array([-cos_a, -sin_a, 0])
        )

        arc_beta_main = Arc(start_angle=alpha, angle=beta, radius=1.0, arc_center=p_A, color=BLUE_B)
        lbl_beta_main = MathTex(r"\beta", font_size=22, color=BLUE_B).move_to(
            p_A + 1.25 * np.array([np.cos(alpha + beta/2), np.sin(alpha + beta/2), 0])
        )

        self.play(
            grp_unit_alpha.animate.scale(0.65).to_corner(UL, buff=0.8),
            ReplacementTransform(tri_beta, tri_AEF),
            ReplacementTransform(ra_2, ra_E),
            ReplacementTransform(arc_b2, arc_beta_main),
            ReplacementTransform(lbl_b2, lbl_beta_main),
            ReplacementTransform(lbl_h2, lbl_AF),
            ReplacementTransform(lbl_w2, lbl_AE),
            ReplacementTransform(lbl_v2, lbl_EF),
            run_time=1.4
        )
        self.wait(2.2)

        # =====================================================
        # 鏡頭 3：將 alpha 三角形縮放成兩份並貼合
        # =====================================================
        cap3 = self.make_caption("將", ("math", r"\alpha"), "三角形縮放", ("math", r"\cos\beta"), "倍，貼於底部成為黃色直角三角形")
        self.set_caption(cap3)

        p_B = np.array([p_E[0], p_A[1], 0])
        tri_ABE = Polygon(p_A, p_B, p_E, fill_color=C_YELLOW, fill_opacity=0.4, stroke_color=C_YELLOW_STROKE, stroke_width=2.5)
        ra_B = self.make_right_angle(p_B, p_A, p_E, size=0.22)
        arc_alpha_bot = Arc(start_angle=0, angle=alpha, radius=0.7, arc_center=p_A, color=YELLOW)
        lbl_alpha_bot = MathTex(r"\alpha", font_size=22, color=YELLOW).move_to(
            p_A + 0.9 * np.array([np.cos(alpha/2), np.sin(alpha/2), 0])
        )

        lbl_AB = MathTex(r"\cos\beta\cos\alpha", font_size=22, color=C_YELLOW_STROKE).next_to(Line(p_A, p_B), DOWN, buff=0.15)
        lbl_BE = MathTex(r"\cos\beta\sin\alpha", font_size=22, color=C_YELLOW_STROKE).next_to(Line(p_B, p_E), RIGHT, buff=0.15)

        ghost1 = tri_alpha.copy().set_color(YELLOW).set_stroke(YELLOW, 2)
        self.play(Transform(ghost1, tri_ABE), run_time=1.0)
        self.remove(ghost1)
        self.add(tri_ABE)
        self.play(Create(ra_B), Create(arc_alpha_bot), FadeIn(lbl_alpha_bot), FadeIn(lbl_AB), FadeIn(lbl_BE), run_time=0.8)
        self.wait(2.2)

        cap4 = self.make_caption("再將", ("math", r"\alpha"), "三角形縮放", ("math", r"\sin\beta"), "倍，貼於右上角成為粉色直角三角形")
        self.set_caption(cap4)

        p_C = np.array([p_B[0], p_F[1], 0])
        tri_EFC = Polygon(p_E, p_F, p_C, fill_color=C_PINK, fill_opacity=0.4, stroke_color=C_PINK_STROKE, stroke_width=2.5)
        ra_C = self.make_right_angle(p_C, p_F, p_E, size=0.22)
        
        arc_alpha_top = Arc(start_angle=np.pi/2, angle=alpha, radius=0.45, arc_center=p_E, color=PINK)
        lbl_alpha_top = MathTex(r"\alpha", font_size=20, color=PINK).move_to(
            p_E + 0.65 * np.array([-np.sin(alpha/2), np.cos(alpha/2), 0])
        )

        lbl_EC = MathTex(r"\sin\beta\cos\alpha", font_size=21, color=C_PINK_STROKE).next_to(Line(p_E, p_C), RIGHT, buff=0.15)
        lbl_FC = MathTex(r"\sin\beta\sin\alpha", font_size=21, color=C_PINK_STROKE).next_to(Line(p_F, p_C), UP, buff=0.15)

        ghost2 = tri_alpha.copy().set_color(PINK).set_stroke(PINK, 2)
        self.play(Transform(ghost2, tri_EFC), run_time=1.0)
        self.remove(ghost2)
        self.add(tri_EFC)
        self.play(Create(ra_C), Create(arc_alpha_top), FadeIn(lbl_alpha_top), FadeIn(lbl_EC), FadeIn(lbl_FC), run_time=0.8)
        self.play(FadeOut(grp_unit_alpha), run_time=0.5)
        self.wait(2.0)

        # =====================================================
        # 鏡頭 4：補出外框矩形 ABCD 與總夾角 alpha + beta
        # =====================================================
        cap5 = self.make_caption("補齊矩形", ("math", "ABCD"), "，斜邊", ("math", r"\overline{AF}=1"), "與水平夾角為", ("math", r"\alpha+\beta"))
        self.set_caption(cap5)

        p_D = np.array([p_A[0], p_F[1], 0])
        rect_outer = VMobject().set_points_as_corners([p_A, p_B, p_C, p_D, p_A]).set_stroke(C_RECT, 2.0)
        line_DF = Line(p_D, p_F, stroke_color=C_RECT, stroke_width=2.0)
        ra_D = self.make_right_angle(p_D, p_A, p_F, size=0.22)

        t_A = MathTex("A", font_size=22, color=WHITE).next_to(p_A, DOWN+LEFT, buff=0.1)
        t_B = MathTex("B", font_size=22, color=WHITE).next_to(p_B, DOWN+RIGHT, buff=0.1)
        t_C = MathTex("C", font_size=22, color=WHITE).next_to(p_C, UP+RIGHT, buff=0.1)
        t_D = MathTex("D", font_size=22, color=WHITE).next_to(p_D, UP+LEFT, buff=0.1)
        t_E = MathTex("E", font_size=22, color=WHITE).next_to(p_E, RIGHT, buff=0.12)
        t_F = MathTex("F", font_size=22, color=WHITE).next_to(p_F, UP+LEFT, buff=0.08)
        grp_labels = VGroup(t_A, t_B, t_C, t_D, t_E, t_F)

        self.play(Create(rect_outer), Create(line_DF), Create(ra_D), FadeIn(grp_labels), run_time=1.0)

        arc_total = Arc(start_angle=0, angle=sum_ang, radius=1.15, arc_center=p_A, color=C_HL_A)
        lbl_total = MathTex(r"\alpha+\beta", font_size=20, color=C_HL_A).move_to(
            p_A + 1.45 * np.array([np.cos(sum_ang/2), np.sin(sum_ang/2), 0])
        )
        self.play(Create(arc_total), FadeIn(lbl_total), run_time=0.8)
        self.wait(1.2)

        arc_DFA = Arc(start_angle=-np.pi, angle=sum_ang, radius=0.55, arc_center=p_F, color=C_HL_A)
        lbl_DFA = MathTex(r"\alpha+\beta", font_size=20, color=C_HL_A).move_to(
            p_F + 0.82 * np.array([np.cos(-np.pi + sum_ang/2), np.sin(-np.pi + sum_ang/2), 0])
        )
        cap5_sub = self.make_caption("由平行內錯角可知，", ("math", r"\angle DFA = \alpha+\beta"), "，確立直角三角形邊長！")
        self.set_caption(cap5_sub)
        self.play(Create(arc_DFA), FadeIn(lbl_DFA), run_time=0.8)
        self.wait(1.2)

        lbl_AD = MathTex(r"\sin(\alpha+\beta)", font_size=23, color=C_HL_B).next_to(Line(p_A, p_D), LEFT, buff=0.15)
        lbl_DF = MathTex(r"\cos(\alpha+\beta)", font_size=23, color=C_HL_A).next_to(Line(p_D, p_F), UP, buff=0.15)
        self.play(FadeIn(lbl_AD), FadeIn(lbl_DF), run_time=0.8)
        self.wait(1.2)

        # =====================================================
        # 鏡頭 5：推導 sin(alpha + beta)
        # =====================================================
        cap6 = self.make_caption("觀察垂直高度：", ("math", r"\overline{AD} = \overline{BE} + \overline{EC}"))
        self.set_caption(cap6)

        hl_AD = Line(p_A, p_D, stroke_color=C_HL_B, stroke_width=5.0)
        hl_BE = Line(p_B, p_E, stroke_color=C_YELLOW, stroke_width=5.0)
        hl_EC = Line(p_E, p_C, stroke_color=C_PINK, stroke_width=5.0)

        self.play(Create(hl_AD), run_time=0.6)
        self.play(Create(hl_BE), Create(hl_EC), run_time=0.6)

        formula_pos = np.array([3.4, 1.2, 0])
        f_sin_step1 = self.make_step_title(None, "垂直高度：", r"\overline{AD} = \overline{BE} + \overline{EC}", formula_pos, color=BLUE_B)
        f_sin_step2 = MathTex(
            r"\sin(\alpha+\beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta",
            font_size=26, color=YELLOW_C
        ).next_to(f_sin_step1, DOWN, buff=0.35)
        box_sin = SurroundingRectangle(f_sin_step2, color=YELLOW, buff=0.15)

        self.play(FadeIn(f_sin_step1), run_time=0.8)
        self.play(Write(f_sin_step2), Create(box_sin), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(hl_AD), FadeOut(hl_BE), FadeOut(hl_EC), run_time=0.5)

        # =====================================================
        # 鏡頭 6：推導 cos(alpha + beta)
        # =====================================================
        cap7 = self.make_caption("觀察水平寬度：", ("math", r"\overline{DF} = \overline{AB} - \overline{FC}"), "，右上扣除粉色邊！")
        self.set_caption(cap7)

        hl_DF = Line(p_D, p_F, stroke_color=C_HL_A, stroke_width=5.0)
        hl_AB = Line(p_A, p_B, stroke_color=C_YELLOW, stroke_width=5.0)
        hl_FC = Line(p_F, p_C, stroke_color=C_PINK, stroke_width=5.0)

        self.play(Create(hl_DF), run_time=0.6)
        self.play(Create(hl_AB), Create(hl_FC), run_time=0.6)

        formula_cos_pos = np.array([3.4, -1.2, 0])
        f_cos_step1 = self.make_step_title(None, "水平寬度：", r"\overline{DF} = \overline{AB} - \overline{FC}", formula_cos_pos, color=BLUE_B)
        f_cos_step2 = MathTex(
            r"\cos(\alpha+\beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta",
            font_size=26, color=YELLOW_C
        ).next_to(f_cos_step1, DOWN, buff=0.35)
        box_cos = SurroundingRectangle(f_cos_step2, color=YELLOW, buff=0.15)

        self.play(FadeIn(f_cos_step1), run_time=0.8)
        self.play(Write(f_cos_step2), Create(box_cos), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(hl_DF), FadeOut(hl_AB), FadeOut(hl_FC), run_time=0.5)

        # =====================================================
        # 鏡頭 7：和角公式總結過渡
        # =====================================================
        grp_sum_derivations = VGroup(
            f_sin_step1, f_sin_step2, box_sin,
            f_cos_step1, f_cos_step2, box_cos
        )
        self.play(FadeOut(grp_sum_derivations), run_time=0.8)

        # =====================================================
        # 鏡頭 8：差角公式——鏡像翻轉改造！
        # =====================================================
        hud_title_diff = Text("差角公式的幾何推導（鏡像翻轉）", font=CHINESE_FONT, font_size=24, weight=BOLD).set_color(GREEN_B)
        hud_title_diff.to_edge(UP, buff=0.25)
        self.play(Transform(hud_title, hud_title_diff), run_time=0.5)

        cap8 = self.make_caption("保持基準邊", ("math", r"\overline{AE}"), "，將", ("math", r"\beta"), "結構沿", ("math", r"\overline{AE}"), "鏡像翻轉至下方！")
        self.set_caption(cap8)

        sum_specific = VGroup(
            rect_outer, line_DF, ra_D, ra_C, t_C, t_D, t_F,
            arc_total, lbl_total, arc_DFA, lbl_DFA, lbl_AD, lbl_DF, lbl_EC, lbl_FC,
            arc_alpha_top, lbl_alpha_top, lbl_BE
        )
        self.play(FadeOut(sum_specific), run_time=0.8)

        p_F_diff = p_A + np.array([R * np.cos(diff_ang), R * np.sin(diff_ang), 0])
        p_C_diff = np.array([p_B[0], p_F_diff[1], 0])
        p_D_diff = np.array([p_F_diff[0], p_A[1], 0])

        u_ae = np.array([cos_a, sin_a, 0])
        v_AC = p_C - p_A
        p_C_mid = p_A + 2 * np.dot(v_AC, u_ae) * u_ae - v_AC

        tri_AEF_diff = Polygon(p_A, p_E, p_F_diff, fill_color=C_BLUE, fill_opacity=0.4, stroke_color=C_BLUE_STROKE, stroke_width=2.5)
        ra_E_diff = self.make_right_angle(p_E, p_F_diff, p_A, size=0.22)
        arc_beta_diff = Arc(start_angle=alpha, angle=-beta, radius=1.0, arc_center=p_A, color=BLUE_B)
        lbl_beta_diff = MathTex(r"\beta", font_size=22, color=BLUE_B).move_to(
            p_A + 1.25 * np.array([np.cos(alpha - beta/2), np.sin(alpha - beta/2), 0])
        )
        lbl_AF_diff = MathTex("1", font_size=22, color=WHITE).move_to(
            p_A + 2.5 * np.array([np.cos(diff_ang), np.sin(diff_ang), 0]) + np.array([-0.1, 0.22, 0])
        )
        lbl_AE_diff = MathTex(r"\cos\beta", font_size=22, color=C_BLUE_STROKE).move_to(
            (p_A + p_E)/2 + 0.30 * np.array([sin_a, -cos_a, 0])
        )
        lbl_EF_diff = MathTex(r"\sin\beta", font_size=22, color=C_BLUE_STROKE).move_to(
            (p_E + p_F_diff)/2 + 0.35 * np.array([-cos_a, -sin_a, 0])
        )

        tri_EFC_mid = Polygon(p_E, p_F_diff, p_C_mid, fill_color=C_PINK, fill_opacity=0.4, stroke_color=C_PINK_STROKE, stroke_width=2.5)

        self.play(
            ReplacementTransform(tri_AEF, tri_AEF_diff),
            ReplacementTransform(ra_E, ra_E_diff),
            ReplacementTransform(arc_beta_main, arc_beta_diff),
            ReplacementTransform(lbl_beta_main, lbl_beta_diff),
            ReplacementTransform(lbl_AF, lbl_AF_diff),
            ReplacementTransform(lbl_AE, lbl_AE_diff),
            ReplacementTransform(lbl_EF, lbl_EF_diff),
            ReplacementTransform(tri_EFC, tri_EFC_mid),
            run_time=1.3
        )

        tri_EFC_diff = Polygon(p_E, p_F_diff, p_C_diff, fill_color=C_PINK, fill_opacity=0.4, stroke_color=C_PINK_STROKE, stroke_width=2.5)
        ra_C_diff = self.make_right_angle(p_C_diff, p_E, p_F_diff, size=0.2)
        line_F_diff_proj = DashedLine(p_F_diff, p_D_diff, stroke_color=C_HL_A, stroke_width=2.0)

        t_F_diff = MathTex("F'", font_size=22, color=WHITE).next_to(p_F_diff, RIGHT, buff=0.1)
        t_C_diff = MathTex("C'", font_size=22, color=WHITE).next_to(p_C_diff, LEFT, buff=0.1)
        t_D_diff = MathTex("D'", font_size=22, color=WHITE).next_to(p_D_diff, DOWN, buff=0.1)

        p_EC_mid = (p_E + p_C_diff) / 2
        callout_EC_start = p_EC_mid + RIGHT * 0.05
        callout_EC_end = callout_EC_start + np.array([0.90, 0.40, 0])
        line_callout_EC = Line(callout_EC_start, callout_EC_end, stroke_color=C_PINK_STROKE, stroke_width=1.6)
        lbl_EC_diff = MathTex(r"\sin\beta\cos\alpha", font_size=21, color=C_PINK_STROKE).next_to(callout_EC_end, RIGHT, buff=0.1)

        p_FC_mid = (p_C_diff + p_F_diff) / 2
        callout_FC_start = p_FC_mid + RIGHT * 0.05
        callout_FC_end = callout_FC_start + np.array([0.90, 0.15, 0])
        line_callout_FC = Line(callout_FC_start, callout_FC_end, stroke_color=C_PINK_STROKE, stroke_width=1.6)
        lbl_FC_diff = MathTex(r"\sin\beta\sin\alpha", font_size=21, color=C_PINK_STROKE).next_to(callout_FC_end, RIGHT, buff=0.1)

        self.play(
            ReplacementTransform(tri_EFC_mid, tri_EFC_diff),
            Create(ra_C_diff), Create(line_F_diff_proj),
            FadeIn(t_F_diff), FadeIn(t_C_diff), FadeIn(t_D_diff),
            Create(line_callout_EC), FadeIn(lbl_EC_diff),
            Create(line_callout_FC), FadeIn(lbl_FC_diff),
            run_time=1.1
        )
        self.wait(1.0)

        arc_diff_main = Arc(start_angle=0, angle=diff_ang, radius=0.9, arc_center=p_A, color=C_HL_B)
        lbl_diff_main = MathTex(r"\alpha-\beta", font_size=20, color=C_HL_B).move_to(
            p_A + 1.25 * np.array([np.cos(diff_ang/2), np.sin(diff_ang/2), 0])
        )
        self.play(Create(arc_diff_main), FadeIn(lbl_diff_main), run_time=0.8)
        self.wait(1.8)

        # =====================================================
        # 鏡頭 9：推導 sin(alpha - beta)
        # =====================================================
        cap9 = self.make_caption("觀察垂直高度：", ("math", r"\overline{F'D'} = \overline{BE} - \overline{EC'}"))
        self.set_caption(cap9)

        hl_BE_diff = Line(p_B, p_E, stroke_color=C_YELLOW, stroke_width=5.0)
        hl_EC_sub = Line(p_C_diff, p_E, stroke_color=C_HL_C, stroke_width=5.0)
        hl_F_height = Line(p_D_diff, p_F_diff, stroke_color=C_HL_B, stroke_width=5.0)
        lbl_sin_diff = MathTex(r"\sin(\alpha-\beta)", font_size=23, color=C_HL_B).next_to(hl_F_height, RIGHT, buff=0.18).shift(DOWN * 0.3)

        self.play(Create(hl_BE_diff), run_time=0.5)
        self.play(Create(hl_EC_sub), run_time=0.6)
        self.play(Create(hl_F_height), FadeIn(lbl_sin_diff), run_time=0.6)

        f_sin_diff1 = self.make_step_title(None, "垂直高度：", r"\overline{F'D'} = \overline{BE} - \overline{EC'}", formula_pos, color=GREEN_B)
        f_sin_diff2 = MathTex(
            r"\sin(\alpha-\beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta",
            font_size=26, color=GREEN_B
        ).next_to(f_sin_diff1, DOWN, buff=0.35)
        box_sin_diff = SurroundingRectangle(f_sin_diff2, color=GREEN, buff=0.15)

        self.play(FadeIn(f_sin_diff1), run_time=0.8)
        self.play(Write(f_sin_diff2), Create(box_sin_diff), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(hl_BE_diff), FadeOut(hl_EC_sub), FadeOut(hl_F_height), run_time=0.5)

        # =====================================================
        # 鏡頭 10：推導 cos(alpha - beta)
        # =====================================================
        cap10 = self.make_caption("觀察水平寬度：", ("math", r"\overline{AD'} = \overline{AB} + \overline{BD'}"))
        self.set_caption(cap10)

        hl_AB_diff = Line(p_A, p_B, stroke_color=C_YELLOW, stroke_width=5.0)
        hl_FC_add = Line(p_B, p_D_diff, stroke_color=C_PINK, stroke_width=5.0)
        hl_AD_diff = Line(p_A, p_D_diff, stroke_color=C_HL_A, stroke_width=5.0)
        lbl_cos_diff = MathTex(r"\cos(\alpha-\beta)", font_size=23, color=C_HL_A).next_to(hl_AD_diff, DOWN, buff=0.45)

        self.play(Create(hl_AB_diff), run_time=0.5)
        self.play(Create(hl_FC_add), run_time=0.6)
        self.play(Create(hl_AD_diff), FadeIn(lbl_cos_diff), run_time=0.6)

        f_cos_diff1 = self.make_step_title(None, "水平寬度：", r"\overline{AD'} = \overline{AB} + \overline{BD'}", formula_cos_pos, color=GREEN_B)
        f_cos_diff2 = MathTex(
            r"\cos(\alpha-\beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta",
            font_size=26, color=GREEN_B
        ).next_to(f_cos_diff1, DOWN, buff=0.35)
        box_cos_diff = SurroundingRectangle(f_cos_diff2, color=GREEN, buff=0.15)

        self.play(FadeIn(f_cos_diff1), run_time=0.8)
        self.play(Write(f_cos_diff2), Create(box_cos_diff), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(hl_AB_diff), FadeOut(hl_FC_add), FadeOut(hl_AD_diff), run_time=0.5)

        # =====================================================
        # 鏡頭 11：全劇總結——四公式整理總表
        # =====================================================
        if hasattr(self, "current_caption") and self.current_caption is not None:
            self.play(FadeOut(self.current_caption), run_time=0.4)
            self.current_caption = None

        self.play(
            FadeOut(Group(*self.mobjects)),
            run_time=1.0
        )

        final_title = Text("和角與差角公式總結", font=CHINESE_FONT, font_size=32, weight=BOLD).set_color(YELLOW_C)
        final_title.to_edge(UP, buff=0.6)

        sum_block = VGroup(
            Text("【和角公式】", font=CHINESE_FONT, font_size=22, color=BLUE_B),
            MathTex(r"\sin(\alpha+\beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta", font_size=26),
            MathTex(r"\cos(\alpha+\beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        diff_block = VGroup(
            Text("【差角公式】", font=CHINESE_FONT, font_size=22, color=GREEN_B),
            MathTex(r"\sin(\alpha-\beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta", font_size=26),
            MathTex(r"\cos(\alpha-\beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        rule_box = VGroup(
            Text("記憶秘訣：", font=CHINESE_FONT, font_size=22, color=YELLOW_C),
            Text("• 正弦同號：加號對加號、減號對減號（高度累加或扣除）", font=CHINESE_FONT, font_size=20, color=WHITE),
            Text("• 餘弦異號：加號對減號、減號對加號（水平扣除或向右延伸）", font=CHINESE_FONT, font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        table_grp = VGroup(sum_block, diff_block).arrange(RIGHT, buff=1.2)
        all_final = VGroup(final_title, table_grp, rule_box).arrange(DOWN, buff=0.55)
        
        final_rect = SurroundingRectangle(table_grp, color=YELLOW_B, buff=0.35)

        self.play(FadeIn(final_title, shift=DOWN*0.2), run_time=0.8)
        self.play(FadeIn(sum_block, shift=RIGHT*0.3), FadeIn(diff_block, shift=LEFT*0.3), run_time=1.2)
        self.play(Create(final_rect), run_time=0.8)
        self.play(FadeIn(rule_box, shift=UP*0.2), run_time=1.0)
        self.wait(3.0)
