from manim import *
import numpy as np

# Windows 平台避免 LaTeX log 暫存檔鎖定報錯
config.no_latex_cleanup = True

# ============================================================
# 字型設定（系統支援「源石黑體 GenSekiGothic TW」）
# ============================================================
CHINESE_FONT = "GenSekiGothic TW"


class LawOfCosines(Scene):

    # ---------------------------------------------------------
    # 底部字幕輔助函式（支援中文文字與數學式混排）
    # ---------------------------------------------------------
    def make_caption(self, *items):
        parts = []
        for item in items:
            if isinstance(item, Mobject):
                parts.append(item)
            elif isinstance(item, tuple) and item[0] == "math":
                parts.append(MathTex(item[1]).scale(0.85))
            else:
                parts.append(Text(str(item), font=CHINESE_FONT, font_size=24))

        group = VGroup(*parts).arrange(RIGHT, buff=0.15)
        group.to_edge(DOWN, buff=0.35)
        return group

    def construct(self):
        # =====================================================
        # 1. 幾何基礎參數（精準設定，保證黃金比例與無重疊佈局）
        # =====================================================
        S = 0.80  # 空間縮放係數，為上方原圖與複製放大過程預留寬廣縱深

        b_val = 1.70
        c_val = 2.30
        A_deg = 55.0
        A_rad = np.radians(A_deg)

        cosA = np.cos(A_rad)
        sinA = np.sin(A_rad)
        a2_val = b_val**2 + c_val**2 - 2 * b_val * c_val * cosA
        a_val = np.sqrt(a2_val)

        # 幾何尺寸（乘上顯示縮放 S）
        rect_W = (b_val**2 + c_val**2) * S
        rect_H = (b_val * c_val * sinA) * S
        b2 = (b_val**2) * S
        c2 = (c_val**2) * S
        a2 = a2_val * S
        bc = (b_val * c_val) * S
        ab = (a_val * b_val) * S
        ac = (a_val * c_val) * S
        proj = (b_val * c_val * cosA) * S

        # 舞台基底座標（往下移至 y0 = -1.75，使頂端在 y = 0.81，徹底不與頂部原圖重疊）
        x0 = -rect_W / 2.0
        y0 = -1.75

        V_BL = np.array([x0, y0, 0])
        V_BR = np.array([x0 + rect_W, y0, 0])
        V_TL = np.array([x0, y0 + rect_H, 0])
        V_TR = np.array([x0 + rect_W, y0 + rect_H, 0])
        V_TopMid = np.array([x0 + b2, y0 + rect_H, 0])
        V_Bot1 = np.array([x0 + proj, y0, 0])
        V_Bot2 = np.array([x0 + proj + a2, y0, 0])

        # 精選和諧調色盤
        C_GREEN = "#2ECC71"
        C_GREEN_STROKE = "#A3E4D7"
        C_YELLOW = "#F39C12"
        C_YELLOW_STROKE = "#FAD7A0"
        C_BLUE = "#3498DB"
        C_BLUE_STROKE = "#AED6F1"
        C_RECT = "#D946EF"
        C_HIGHLIGHT = "#FFE600"
        C_RED = "#FF6B6B"

        # =====================================================
        # 頂部標題
        # =====================================================
        main_title = Text("餘弦定理的幾何視覺證明", font=CHINESE_FONT, font_size=28)
        main_title.to_edge(UP, buff=0.25).set_color(YELLOW_C)
        self.play(FadeIn(main_title), run_time=0.8)

        # =====================================================
        # 【Part 1】原始三角形與標示 (t = 0.8s ~ 6.8s)
        # =====================================================
        cap1 = self.make_caption(
            "先考慮任意三角形，三邊長為", ("math", "a, b, c"),
            "，夾角為", ("math", r"\angle A")
        )
        self.play(FadeIn(cap1), run_time=0.6)

        # 頂部參考三角形 T0（置於安全高位 y = 2.45，緊湊優雅）
        ref_scale = 0.72
        ref_A = np.array([0, 0, 0])
        ref_B = np.array([c_val * ref_scale, 0, 0])
        ref_C = np.array([b_val * cosA * ref_scale, b_val * sinA * ref_scale, 0])
        ref_center_target = np.array([0, 2.45, 0])

        ref_pts = [ref_A, ref_B, ref_C]
        ref_centroid = np.mean(ref_pts, axis=0)
        shift_vec = ref_center_target - ref_centroid

        P_A0 = ref_A + shift_vec
        P_B0 = ref_B + shift_vec
        P_C0 = ref_C + shift_vec

        tri_ref = Polygon(P_A0, P_B0, P_C0, fill_color="#34495E", fill_opacity=0.55, stroke_color=WHITE, stroke_width=2.5)

        # 標註邊長 a, b, c
        lbl_c0 = MathTex("c").scale(0.65).next_to(Line(P_A0, P_B0), DOWN, buff=0.08)
        lbl_b0 = MathTex("b").scale(0.65).next_to(Line(P_A0, P_C0).get_center(), UP + LEFT, buff=0.06)
        lbl_a0 = MathTex("a").scale(0.65).next_to(Line(P_B0, P_C0).get_center(), UP + RIGHT, buff=0.06)

        # 標註角 A、圓形標記(o)、叉號標記(x)
        arc_A0 = Arc(radius=0.28, start_angle=0, angle=A_rad, arc_center=P_A0, color=C_RED, stroke_width=2.5)
        lbl_A0 = MathTex("A").scale(0.60).set_color(C_RED).next_to(arc_A0, DOWN + LEFT, buff=0.04)
        mark_C0 = Circle(radius=0.07, color=YELLOW_B, stroke_width=2).move_to(P_C0 + np.array([0, -0.18, 0]))
        mark_B0 = MathTex(r"\times").scale(0.50).set_color(C_BLUE_STROKE).move_to(P_B0 + np.array([-0.18, 0.12, 0]))

        ref_group = VGroup(tri_ref, lbl_c0, lbl_b0, lbl_a0, arc_A0, lbl_A0, mark_C0, mark_B0)

        self.play(Create(tri_ref), run_time=1.2)
        self.play(
            FadeIn(lbl_c0), FadeIn(lbl_b0), FadeIn(lbl_a0),
            Create(arc_A0), FadeIn(lbl_A0),
            FadeIn(mark_C0), FadeIn(mark_B0),
            run_time=1.4
        )
        self.wait(2.2)

        # =====================================================
        # 【Part 2】第一份：複製後「往下移至中央過渡區再放大」，就定位於左側 (t = 6.8s ~ 13.8s)
        # =====================================================
        cap2 = self.make_caption(
            "複製第一份三角形，將邊長放大", ("math", "b"),
            "倍，得到", ("math", r"b^2, ab, bc"), "，就定位於左側"
        )
        self.play(ReplacementTransform(cap1, cap2), run_time=0.6)

        # 複製原三角形
        clone1_tri = Polygon(P_A0, P_B0, P_C0, fill_color=C_GREEN, fill_opacity=0.6, stroke_color=C_GREEN_STROKE, stroke_width=3)
        clone1_lbl_c = MathTex("c").scale(0.65).set_color(C_GREEN_STROKE).next_to(Line(P_A0, P_B0), DOWN, buff=0.08)
        clone1_lbl_b = MathTex("b").scale(0.65).set_color(C_GREEN_STROKE).next_to(Line(P_A0, P_C0).get_center(), UP + LEFT, buff=0.06)
        clone1_lbl_a = MathTex("a").scale(0.65).set_color(C_GREEN_STROKE).next_to(Line(P_B0, P_C0).get_center(), UP + RIGHT, buff=0.06)
        clone1_mark_C = Circle(radius=0.07, color=YELLOW_B, stroke_width=2).move_to(P_C0 + np.array([0, -0.18, 0]))
        clone1_mark_B = MathTex(r"\times").scale(0.50).set_color(C_BLUE_STROKE).move_to(P_B0 + np.array([-0.18, 0.12, 0]))
        clone1_arc_A = Arc(radius=0.28, start_angle=0, angle=A_rad, arc_center=P_A0, color=C_RED, stroke_width=2.5)
        clone1_lbl_A = MathTex("A").scale(0.60).set_color(C_RED).next_to(clone1_arc_A, DOWN + LEFT, buff=0.04)

        clone1 = VGroup(clone1_tri, clone1_lbl_c, clone1_lbl_b, clone1_lbl_a, clone1_mark_C, clone1_mark_B, clone1_arc_A, clone1_lbl_A)

        # ★ 解決問題 1：先往下移到空曠過渡區（y = 0.5），再進行放大就位，完全不遮擋上方原圖
        staging_pos1 = np.array([-0.8, 0.45, 0])
        self.play(clone1.animate.move_to(staging_pos1), run_time=1.0)

        # 目標頂點：V_TL(A), V_TopMid(C), V_Bot1(B)
        tri1_target = Polygon(V_TL, V_TopMid, V_Bot1, fill_color=C_GREEN, fill_opacity=0.6, stroke_color=C_GREEN_STROKE, stroke_width=3)
        lbl1_top_b2 = MathTex(r"b^2").scale(0.75).set_color(C_GREEN_STROKE).next_to(Line(V_TL, V_TopMid), UP, buff=0.10)
        # 0:12 bc 往左移，不壓到斜邊邊界
        lbl1_left_bc = MathTex(r"bc").scale(0.75).set_color(C_GREEN_STROKE).move_to(Line(V_TL, V_Bot1).get_center() + np.array([-0.48, 0.15, 0]))
        lbl1_right_ab = MathTex(r"ab").scale(0.75).set_color(C_GREEN_STROKE).move_to(Line(V_TopMid, V_Bot1).get_center() + np.array([-0.24, -0.12, 0]))
        mark1_C = Circle(radius=0.08, color=YELLOW_B, stroke_width=2).move_to(V_TopMid + np.array([-0.24, -0.14, 0]))
        mark1_B = MathTex(r"\times").scale(0.50).set_color(C_BLUE_STROKE).move_to(V_Bot1 + np.array([-0.06, 0.22, 0]))
        arc1_A = Arc(radius=0.40, start_angle=-A_rad, angle=A_rad, arc_center=V_TL, color=C_RED, stroke_width=2.5)
        # 0:12 A 往右移，不與弧線重疊
        lbl1_A = MathTex("A").scale(0.60).set_color(C_RED).move_to(V_TL + np.array([0.58, -0.20, 0]))

        final_grp1 = VGroup(tri1_target, lbl1_top_b2, lbl1_left_bc, lbl1_right_ab, mark1_C, mark1_B, arc1_A, lbl1_A)

        # 平滑過渡變換：由過渡區同步放大、旋轉、平移就位
        self.play(
            ReplacementTransform(clone1, final_grp1),
            run_time=2.2,
            rate_func=smooth
        )
        self.wait(1.8)

        # =====================================================
        # 【Part 3】第二份：複製後往下移再放大 a 倍，高亮 ab 接合 (t = 13.8s ~ 22.8s)
        # =====================================================
        cap3 = self.make_caption(
            "複製第二份，各邊長乘上", ("math", "a"),
            "；高亮共同邊", ("math", "ab"), "進行接合"
        )
        self.play(ReplacementTransform(cap2, cap3), run_time=0.6)

        # ★ 複製原圖並先往下移至右側空曠過渡區（y = 0.50）
        offset2 = np.array([1.0, 1.2, 0])
        P_Top2 = V_TopMid + offset2
        P_Bot1_2 = V_Bot1 + offset2
        P_Bot2_2 = V_Bot2 + offset2

        tri2_float = Polygon(P_Top2, P_Bot1_2, P_Bot2_2, fill_color=C_YELLOW, fill_opacity=0.6, stroke_color=C_YELLOW_STROKE, stroke_width=3)
        lbl2_ab = MathTex(r"ab").scale(0.75).set_color(C_YELLOW_STROKE).move_to(Line(P_Top2, P_Bot1_2).get_center() + np.array([0.24, 0.05, 0]))
        lbl2_a2 = MathTex(r"a^2").scale(0.75).set_color(C_YELLOW_STROKE).next_to(Line(P_Bot1_2, P_Bot2_2), DOWN, buff=0.10)
        lbl2_ac = MathTex(r"ac").scale(0.75).set_color(C_YELLOW_STROKE).next_to(Line(P_Top2, P_Bot2_2).get_center(), UP + RIGHT, buff=0.08)

        # 0:13 棕色三角形頂角 A 依兩側邊精確角度計算弧度與位置
        dx_ab = b_val * (c_val * cosA - b_val)
        dy_ab = -b_val * c_val * sinA
        theta_ab = np.arctan2(dy_ab, dx_ab)
        theta_mid2 = theta_ab + A_rad / 2.0
        mark2_A = Arc(radius=0.40, start_angle=theta_ab, angle=A_rad, arc_center=P_Top2, color=C_RED, stroke_width=2.5)
        lbl2_mark_A = MathTex("A").scale(0.55).set_color(C_RED).move_to(P_Top2 + np.array([0.62 * np.cos(theta_mid2), 0.62 * np.sin(theta_mid2), 0]))
        mark2_C = Circle(radius=0.08, color=YELLOW_B, stroke_width=2).move_to(P_Bot1_2 + np.array([0.20, 0.14, 0]))
        mark2_B = MathTex(r"\times").scale(0.50).set_color(C_BLUE_STROKE).move_to(P_Bot2_2 + np.array([-0.20, 0.14, 0]))

        grp2_float = VGroup(tri2_float, lbl2_ab, lbl2_a2, lbl2_ac, mark2_A, lbl2_mark_A, mark2_C, mark2_B)

        self.play(FadeIn(grp2_float), run_time=1.2)
        self.wait(0.5)

        # ★ 關鍵教學規則：接合前只高亮那一對即將重合的邊，其他邊稍微降亮！
        glow_ab_left = Line(V_TopMid, V_Bot1, color=C_HIGHLIGHT, stroke_width=7)
        glow_ab_right = Line(P_Top2, P_Bot1_2, color=C_HIGHLIGHT, stroke_width=7)

        self.play(
            tri1_target.animate.set_stroke(opacity=0.3).set_fill(opacity=0.25),
            tri2_float.animate.set_stroke(opacity=0.3).set_fill(opacity=0.25),
            lbl1_top_b2.animate.set_opacity(0.3),
            lbl1_left_bc.animate.set_opacity(0.3),
            lbl2_a2.animate.set_opacity(0.3),
            lbl2_ac.animate.set_opacity(0.3),
            Create(glow_ab_left),
            Create(glow_ab_right),
            lbl1_right_ab.animate.set_color(C_HIGHLIGHT).scale(1.15),
            lbl2_ab.animate.set_color(C_HIGHLIGHT).scale(1.15),
            run_time=1.2
        )
        self.wait(0.8)

        # 平移滑入靠攏，緊密接合
        grp2_with_glow = VGroup(grp2_float, glow_ab_right)
        self.play(
            grp2_with_glow.animate.shift(-offset2),
            run_time=1.8,
            rate_func=smooth
        )

        # 接好後：恢復正常亮度，淡出發光邊與內部重複的 ab 標籤
        self.play(
            tri1_target.animate.set_stroke(opacity=1.0).set_fill(opacity=0.6),
            tri2_float.animate.set_stroke(opacity=1.0).set_fill(opacity=0.6),
            lbl1_top_b2.animate.set_opacity(1.0),
            lbl1_left_bc.animate.set_opacity(1.0),
            lbl2_a2.animate.set_opacity(1.0).set_color(C_YELLOW_STROKE),
            lbl2_ac.animate.set_opacity(1.0).set_color(C_YELLOW_STROKE),
            FadeOut(glow_ab_left),
            FadeOut(glow_ab_right),
            FadeOut(lbl1_right_ab),
            FadeOut(lbl2_ab),
            run_time=1.2
        )
        self.wait(1.5)

        # =====================================================
        # 【Part 4】第三份：往下移放大 c 倍，高亮 ac 接合 (t = 22.8s ~ 30.5s)
        # =====================================================
        cap4 = self.make_caption(
            "複製第三份，各邊長乘上", ("math", "c"),
            "；高亮共同邊", ("math", "ac"), "旋轉平移接合"
        )
        self.play(ReplacementTransform(cap3, cap4), run_time=0.6)

        # ★ 複製原圖並先往下移至右側空曠過渡區
        offset3 = np.array([1.2, 1.2, 0])
        P_TopMid_3 = V_TopMid + offset3
        P_TR_3 = V_TR + offset3
        P_Bot2_3 = V_Bot2 + offset3

        tri3_float = Polygon(P_TopMid_3, P_TR_3, P_Bot2_3, fill_color=C_BLUE, fill_opacity=0.6, stroke_color=C_BLUE_STROKE, stroke_width=3)
        # 0:21 ac 左移，不壓到發光邊
        lbl3_ac = MathTex(r"ac").scale(0.75).set_color(C_BLUE_STROKE).move_to(Line(P_TopMid_3, P_Bot2_3).get_center() + np.array([-0.46, 0.05, 0]))
        lbl3_c2 = MathTex(r"c^2").scale(0.75).set_color(C_BLUE_STROKE).next_to(Line(P_TopMid_3, P_TR_3), UP, buff=0.10)
        # 0:21 bc 右移，不壓到斜邊邊界
        lbl3_bc = MathTex(r"bc").scale(0.75).set_color(C_BLUE_STROKE).move_to(Line(P_TR_3, P_Bot2_3).get_center() + np.array([0.50, 0.15, 0]))
        mark3_B = MathTex(r"\times").scale(0.50).set_color(C_BLUE_STROKE).move_to(P_TopMid_3 + np.array([0.24, -0.14, 0]))
        arc3_A = Arc(radius=0.40, start_angle=-np.pi, angle=A_rad, arc_center=P_TR_3, color=C_RED, stroke_width=2.5)
        # 0:21 A 往左一個字寬，圓圈標記往左移
        lbl3_mark_A = MathTex("A").scale(0.60).set_color(C_RED).move_to(P_TR_3 + np.array([-0.58, -0.20, 0]))
        mark3_C = Circle(radius=0.08, color=YELLOW_B, stroke_width=2).move_to(P_Bot2_3 + np.array([-0.12, 0.22, 0]))

        grp3_float = VGroup(tri3_float, lbl3_ac, lbl3_c2, lbl3_bc, mark3_B, arc3_A, lbl3_mark_A, mark3_C)

        self.play(FadeIn(grp3_float), run_time=1.2)
        self.wait(0.5)

        # ★ 高亮共同邊 ac
        glow_ac_mid = Line(V_TopMid, V_Bot2, color=C_HIGHLIGHT, stroke_width=7)
        glow_ac_right = Line(P_TopMid_3, P_Bot2_3, color=C_HIGHLIGHT, stroke_width=7)

        self.play(
            tri2_float.animate.set_stroke(opacity=0.3).set_fill(opacity=0.25),
            tri3_float.animate.set_stroke(opacity=0.3).set_fill(opacity=0.25),
            lbl2_a2.animate.set_opacity(0.3),
            lbl3_c2.animate.set_opacity(0.3),
            lbl3_bc.animate.set_opacity(0.3),
            Create(glow_ac_mid),
            Create(glow_ac_right),
            lbl2_ac.animate.set_color(C_HIGHLIGHT).scale(1.15),
            lbl3_ac.animate.set_color(C_HIGHLIGHT).scale(1.15),
            run_time=1.2
        )
        self.wait(0.8)

        # 平移旋轉滑入靠攏接合
        grp3_with_glow = VGroup(grp3_float, glow_ac_right)
        self.play(
            grp3_with_glow.animate.shift(-offset3),
            run_time=1.8,
            rate_func=smooth
        )

        # 接好後：恢復亮度，淡出發光邊與內部 ac
        self.play(
            tri2_float.animate.set_stroke(opacity=1.0).set_fill(opacity=0.6),
            tri3_float.animate.set_stroke(opacity=1.0).set_fill(opacity=0.6),
            lbl2_a2.animate.set_opacity(1.0).set_color(C_YELLOW_STROKE),
            lbl3_c2.animate.set_opacity(1.0).set_color(C_BLUE_STROKE),
            lbl3_bc.animate.set_opacity(1.0).set_color(C_BLUE_STROKE),
            FadeOut(glow_ac_mid),
            FadeOut(glow_ac_right),
            FadeOut(lbl2_ac),
            FadeOut(lbl3_ac),
            run_time=1.2
        )
        self.wait(1.5)

        # =====================================================
        # 【Part 5】檢視外框：頂部平整直線與底邊中央 (t = 30.5s ~ 40.5s)
        # =====================================================
        cap5 = self.make_caption(
            "三塊拼合！頂部內角和為", ("math", r"180^\circ"),
            "，成一水平直線；上邊為", ("math", r"b^2, c^2"),
            "，下邊中央為", ("math", r"a^2")
        )
        self.play(
            ReplacementTransform(cap4, cap5),
            FadeOut(ref_group),  # 頂部參考圖淡出，騰出廣闊視覺空間
            run_time=1.2
        )

        # 頂部三角聚合演示：圓形(C)、角A、叉號(B)在 V_TopMid 處相遇成 180 度直線
        top_straight_line = Line(V_TL, V_TR, color=WHITE, stroke_width=4)
        self.play(Create(top_straight_line), run_time=1.2)
        self.play(FadeOut(top_straight_line), run_time=0.8)

        # 上邊尺寸標註大括號：b^2 與 c^2
        brace_b2 = BraceBetweenPoints(V_TL, V_TopMid, UP, buff=0.10)
        tex_b2 = brace_b2.get_tex(r"b^2").scale(0.80).set_color(C_GREEN)

        brace_c2 = BraceBetweenPoints(V_TopMid, V_TR, UP, buff=0.10)
        tex_c2 = brace_c2.get_tex(r"c^2").scale(0.80).set_color(C_BLUE)

        # 下邊中央尺寸標註大括號：a^2
        brace_a2 = BraceBetweenPoints(V_Bot1, V_Bot2, DOWN, buff=0.10)
        tex_a2 = brace_a2.get_tex(r"a^2").scale(0.80).set_color(C_YELLOW)

        # 依分鏡規則：此時外框只看 b^2, c^2 與 a^2，其餘內部細碎角標淡出，聚焦大結構
        self.play(
            FadeOut(lbl1_top_b2), FadeOut(lbl3_c2), FadeOut(lbl2_a2),
            FadeOut(mark1_C), FadeOut(mark1_B), FadeOut(arc1_A), FadeOut(lbl1_A),
            FadeOut(mark2_A), FadeOut(lbl2_mark_A), FadeOut(mark2_C), FadeOut(mark2_B),
            FadeOut(mark3_B), FadeOut(arc3_A), FadeOut(lbl3_mark_A), FadeOut(mark3_C),
            GrowFromCenter(brace_b2), FadeIn(tex_b2),
            GrowFromCenter(brace_c2), FadeIn(tex_c2),
            GrowFromCenter(brace_a2), FadeIn(tex_a2),
            run_time=2.2
        )
        self.wait(3.0)

        # =====================================================
        # 【Part 6】左側 bc 投影出 bc cos A (t = 40.5s ~ 49.5s)
        # =====================================================
        cap6 = self.make_caption(
            "觀察左側邊長", ("math", "bc"),
            "，與水平線夾角為", ("math", "A"),
            "；向下作垂線，投影出水平長度", ("math", r"bc \cos A")
        )
        self.play(ReplacementTransform(cap5, cap6), run_time=0.8)

        # 高亮左側邊長 bc
        hypot_L = Line(V_TL, V_Bot1, color=C_GREEN, stroke_width=6)
        self.play(Create(hypot_L), lbl1_left_bc.animate.set_color(C_HIGHLIGHT).scale(1.2), run_time=1.2)

        # 顯示底邊夾角 A
        arc_bot_L = Arc(radius=0.40, start_angle=np.pi, angle=-A_rad, arc_center=V_Bot1, color=C_RED, stroke_width=2.5)
        lbl_bot_LA = MathTex("A").scale(0.60).set_color(C_RED).next_to(arc_bot_L, LEFT, buff=0.06)
        self.play(Create(arc_bot_L), FadeIn(lbl_bot_LA), run_time=1.0)

        # 作垂直線向下投影至 baseline
        perp_L = DashedLine(V_TL, V_BL, color=C_RECT, stroke_width=3)
        ra_sz = 0.22
        elbow_L = VGroup(
            Line(V_BL + np.array([0, ra_sz, 0]), V_BL + np.array([ra_sz, ra_sz, 0]), color=C_RECT, stroke_width=2),
            Line(V_BL + np.array([ra_sz, ra_sz, 0]), V_BL + np.array([ra_sz, 0, 0]), color=C_RECT, stroke_width=2)
        )
        self.play(Create(perp_L), Create(elbow_L), run_time=1.4)

        # 動畫投影出水平長度 bc cos A
        proj_L_line = Line(V_BL, V_Bot1, color=C_RECT, stroke_width=4)
        brace_proj_L = BraceBetweenPoints(V_BL, V_Bot1, DOWN, buff=0.10)
        tex_proj_L = brace_proj_L.get_tex(r"bc \cos A").scale(0.72).set_color(C_RECT)

        self.play(
            Create(proj_L_line),
            GrowFromCenter(brace_proj_L),
            FadeIn(tex_proj_L),
            FadeOut(hypot_L),
            lbl1_left_bc.animate.set_color(C_GREEN_STROKE).scale(1/1.2),
            run_time=2.0
        )
        self.wait(2.5)

        # =====================================================
        # 【Part 7】右側 bc 投影出另一個 bc cos A (t = 49.5s ~ 57.5s)
        # =====================================================
        cap7 = self.make_caption(
            "右側邊長同為", ("math", "bc"),
            "，同樣向下垂直投影，得到另一個", ("math", r"bc \cos A")
        )
        self.play(ReplacementTransform(cap6, cap7), run_time=0.8)

        # 高亮右側邊長 bc
        hypot_R = Line(V_TR, V_Bot2, color=C_BLUE, stroke_width=6)
        self.play(Create(hypot_R), lbl3_bc.animate.set_color(C_HIGHLIGHT).scale(1.2), run_time=1.2)

        # 顯示底邊夾角 A
        arc_bot_R = Arc(radius=0.40, start_angle=0, angle=A_rad, arc_center=V_Bot2, color=C_RED, stroke_width=2.5)
        lbl_bot_RA = MathTex("A").scale(0.60).set_color(C_RED).next_to(arc_bot_R, RIGHT, buff=0.06)
        self.play(Create(arc_bot_R), FadeIn(lbl_bot_RA), run_time=1.0)

        # 作垂直線向下投影
        perp_R = DashedLine(V_TR, V_BR, color=C_RECT, stroke_width=3)
        elbow_R = VGroup(
            Line(V_BR + np.array([0, ra_sz, 0]), V_BR + np.array([-ra_sz, ra_sz, 0]), color=C_RECT, stroke_width=2),
            Line(V_BR + np.array([-ra_sz, ra_sz, 0]), V_BR + np.array([-ra_sz, 0, 0]), color=C_RECT, stroke_width=2)
        )
        self.play(Create(perp_R), Create(elbow_R), run_time=1.4)

        # 動畫投影出水平長度 bc cos A
        proj_R_line = Line(V_Bot2, V_BR, color=C_RECT, stroke_width=4)
        brace_proj_R = BraceBetweenPoints(V_Bot2, V_BR, DOWN, buff=0.10)
        tex_proj_R = brace_proj_R.get_tex(r"bc \cos A").scale(0.72).set_color(C_RECT)

        self.play(
            Create(proj_R_line),
            GrowFromCenter(brace_proj_R),
            FadeIn(tex_proj_R),
            FadeOut(hypot_R),
            lbl3_bc.animate.set_color(C_BLUE_STROKE).scale(1/1.2),
            run_time=2.0
        )
        self.wait(2.2)

        # =====================================================
        # 【Part 8】比較上下邊，移項即得餘弦定理 (t = 57.5s ~ 68.0s)
        # =====================================================
        cap8 = self.make_caption(
            "外框為矩形，上邊長等於下邊長，移項即證得餘弦定理！"
        )
        self.play(ReplacementTransform(cap7, cap8), run_time=0.8)

        # 高亮完整矩形外框
        full_rect = Polygon(V_BL, V_BR, V_TR, V_TL, stroke_color=C_RECT, stroke_width=3.5)
        self.play(Create(full_rect), run_time=1.8)

        # 頂部公式推導
        eq1 = MathTex(r"b^2 + c^2 = a^2 + 2bc \cos A").scale(0.95).to_edge(UP, buff=0.30).set_color(YELLOW_B)
        self.play(
            FadeOut(main_title),
            Write(eq1),
            run_time=2.0
        )
        self.wait(1.2)

        # 整理移項為標準餘弦定理形式：a^2 = b^2 + c^2 - 2bc cos A
        eq2 = MathTex(r"a^2 = b^2 + c^2 - 2bc \cos A").scale(1.05).to_edge(UP, buff=0.30).set_color(YELLOW)
        final_box = SurroundingRectangle(eq2, color=YELLOW, buff=0.18, stroke_width=2.5)

        self.play(
            ReplacementTransform(eq1, eq2),
            run_time=1.5
        )
        self.play(
            Create(final_box),
            run_time=1.2
        )
        self.wait(2.5)

        # =====================================================
        # 【Part 9】特例延伸：當角 A=90 度時，圖形動態變形密合成矩形，化簡為畢氏定理！ (t = 68.0s ~ 84.0s)
        # =====================================================
        cap9 = self.make_caption(
            "特例探討：當夾角", ("math", r"A = 90^\circ"),
            "，圖形變形為三個直角三角形，外框密合成矩形！"
        )
        self.play(ReplacementTransform(cap8, cap9), run_time=0.8)

        # 1. 公式代入 cos(90) = 0
        eq_step1 = MathTex(r"a^2 = b^2 + c^2 - 2bc \cos(90^\circ)").scale(1.05).to_edge(UP, buff=0.30).set_color(YELLOW)
        self.play(
            ReplacementTransform(eq2, eq_step1),
            final_box.animate.surround(eq_step1, buff=0.18),
            run_time=1.5
        )
        self.wait(0.8)

        # 2. 圖形上兩側 bc cos A 投影變為 0 (標註 0 並轉紅)
        t_zero_L = MathTex(r"0").scale(0.75).set_color(RED_C).move_to(tex_proj_L.get_center())
        t_zero_R = MathTex(r"0").scale(0.75).set_color(RED_C).move_to(tex_proj_R.get_center())

        self.play(
            ReplacementTransform(tex_proj_L, t_zero_L),
            ReplacementTransform(tex_proj_R, t_zero_R),
            brace_proj_L.animate.set_color(RED_C),
            brace_proj_R.animate.set_color(RED_C),
            run_time=1.2
        )
        self.wait(0.6)

        # 3. 直角狀態幾何頂點與目標物體 (A = 90 deg: cos(90) = 0, sin(90) = 1)
        rect_H_90 = bc  # 高度變為 bc * S (sin 90 = 1)
        V_TL_90 = np.array([x0, y0 + rect_H_90, 0])
        V_TR_90 = np.array([x0 + rect_W, y0 + rect_H_90, 0])
        V_TopMid_90 = np.array([x0 + b2, y0 + rect_H_90, 0])
        V_Bot1_90 = V_BL
        V_Bot2_90 = V_BR

        tri1_90 = Polygon(V_TL_90, V_TopMid_90, V_Bot1_90, fill_color=C_GREEN, fill_opacity=0.6, stroke_color=C_GREEN_STROKE, stroke_width=3)
        tri2_90 = Polygon(V_TopMid_90, V_Bot1_90, V_Bot2_90, fill_color=C_YELLOW, fill_opacity=0.6, stroke_color=C_YELLOW_STROKE, stroke_width=3)
        tri3_90 = Polygon(V_TopMid_90, V_TR_90, V_Bot2_90, fill_color=C_BLUE, fill_opacity=0.6, stroke_color=C_BLUE_STROKE, stroke_width=3)
        rect_90 = Polygon(V_BL, V_BR, V_TR_90, V_TL_90, stroke_color=C_RECT, stroke_width=3.5)

        brace_b2_90 = BraceBetweenPoints(V_TL_90, V_TopMid_90, UP, buff=0.10)
        tex_b2_90 = brace_b2_90.get_tex(r"b^2").scale(0.80).set_color(C_GREEN)

        brace_c2_90 = BraceBetweenPoints(V_TopMid_90, V_TR_90, UP, buff=0.10)
        tex_c2_90 = brace_c2_90.get_tex(r"c^2").scale(0.80).set_color(C_BLUE)

        brace_a2_90 = BraceBetweenPoints(V_BL, V_BR, DOWN, buff=0.10)
        tex_a2_90 = brace_a2_90.get_tex(r"a^2").scale(0.85).set_color(C_YELLOW)

        lbl1_left_bc_90 = MathTex(r"bc").scale(0.75).set_color(C_GREEN_STROKE).next_to(Line(V_TL_90, V_BL), LEFT, buff=0.15)
        lbl3_bc_90 = MathTex(r"bc").scale(0.75).set_color(C_BLUE_STROKE).next_to(Line(V_TR_90, V_BR), RIGHT, buff=0.15)

        # 四個角落直角符號與棕色三角形頂角 A 直角符號 (1:15 棕色三角形角 A 標記直角)
        ra_sz = 0.22
        ra_BL = VGroup(
            Line(V_BL + np.array([0, ra_sz, 0]), V_BL + np.array([ra_sz, ra_sz, 0]), color=WHITE, stroke_width=2),
            Line(V_BL + np.array([ra_sz, ra_sz, 0]), V_BL + np.array([ra_sz, 0, 0]), color=WHITE, stroke_width=2)
        )
        ra_BR = VGroup(
            Line(V_BR + np.array([0, ra_sz, 0]), V_BR + np.array([-ra_sz, ra_sz, 0]), color=WHITE, stroke_width=2),
            Line(V_BR + np.array([-ra_sz, ra_sz, 0]), V_BR + np.array([-ra_sz, 0, 0]), color=WHITE, stroke_width=2)
        )
        ra_TL = VGroup(
            Line(V_TL_90 + np.array([0, -ra_sz, 0]), V_TL_90 + np.array([ra_sz, -ra_sz, 0]), color=WHITE, stroke_width=2),
            Line(V_TL_90 + np.array([ra_sz, -ra_sz, 0]), V_TL_90 + np.array([ra_sz, 0, 0]), color=WHITE, stroke_width=2)
        )
        ra_TR = VGroup(
            Line(V_TR_90 + np.array([0, -ra_sz, 0]), V_TR_90 + np.array([-ra_sz, -ra_sz, 0]), color=WHITE, stroke_width=2),
            Line(V_TR_90 + np.array([-ra_sz, -ra_sz, 0]), V_TR_90 + np.array([-ra_sz, 0, 0]), color=WHITE, stroke_width=2)
        )
        # 棕色三角形頂角 A 直角標記
        u_mid1 = np.array([-b_val, -c_val, 0]) / np.sqrt(b_val**2 + c_val**2)
        u_mid2 = np.array([c_val, -b_val, 0]) / np.sqrt(b_val**2 + c_val**2)
        p1_mid = V_TopMid_90 + ra_sz * u_mid1
        p2_mid = V_TopMid_90 + ra_sz * u_mid2
        pc_mid = V_TopMid_90 + ra_sz * u_mid1 + ra_sz * u_mid2
        ra_TopMid = VGroup(
            Line(p1_mid, pc_mid, color=WHITE, stroke_width=2),
            Line(p2_mid, pc_mid, color=WHITE, stroke_width=2)
        )
        rect_elbows = VGroup(ra_BL, ra_BR, ra_TL, ra_TR, ra_TopMid)

        # 4. 動態變形動畫：斜邊直立化、底邊 a^2 鋪滿全底、投影項消逝，三三角形無縫鋪滿矩形
        self.play(
            FadeOut(brace_proj_L), FadeOut(t_zero_L), FadeOut(elbow_L), FadeOut(perp_L), FadeOut(proj_L_line), FadeOut(arc_bot_L), FadeOut(lbl_bot_LA),
            FadeOut(brace_proj_R), FadeOut(t_zero_R), FadeOut(elbow_R), FadeOut(perp_R), FadeOut(proj_R_line), FadeOut(arc_bot_R), FadeOut(lbl_bot_RA),
            Transform(tri1_target, tri1_90),
            Transform(tri2_float, tri2_90),
            Transform(tri3_float, tri3_90),
            Transform(full_rect, rect_90),
            Transform(brace_b2, brace_b2_90),
            Transform(tex_b2, tex_b2_90),
            Transform(brace_c2, brace_c2_90),
            Transform(tex_c2, tex_c2_90),
            Transform(brace_a2, brace_a2_90),
            Transform(tex_a2, tex_a2_90),
            Transform(lbl1_left_bc, lbl1_left_bc_90),
            Transform(lbl3_bc, lbl3_bc_90),
            run_time=2.5,
            rate_func=smooth
        )
        self.play(
            Create(rect_elbows),
            run_time=1.0
        )
        self.wait(1.0)

        # 5. 公式化簡為畢氏定理：a^2 = b^2 + c^2
        cap9_2 = self.make_caption(
            "投影歸零，下邊長", ("math", "a^2"),
            "等於上邊長", ("math", "b^2 + c^2"),
            "，即為畢氏定理！"
        )
        eq_pyth = MathTex(r"a^2 = b^2 + c^2").scale(1.15).to_edge(UP, buff=0.28).set_color(YELLOW_A)
        tag_pyth = Text("（畢氏定理 / 勾股定理）", font=CHINESE_FONT, font_size=22).next_to(eq_pyth, RIGHT, buff=0.35).set_color(GOLD_B)
        pyth_grp = VGroup(eq_pyth, tag_pyth)
        box_pyth = SurroundingRectangle(pyth_grp, color=GOLD_B, buff=0.18, stroke_width=3)

        self.play(
            ReplacementTransform(cap9, cap9_2),
            ReplacementTransform(eq_step1, eq_pyth),
            FadeIn(tag_pyth),
            ReplacementTransform(final_box, box_pyth),
            run_time=1.8
        )

        # 完結停頓（保留充足靜音與定格鑑賞時間）
        self.wait(6.5)
