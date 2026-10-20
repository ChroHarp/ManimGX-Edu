"""托勒密定理 (Ptolemy's Theorem) 最美無字證明 - 9:16 直幅 Reels 動畫 (白底高對比主題版).

設計依據：William Derrick & James Hirstein, The College Mathematics Journal
以及 Matrix67: The Aha Moments (https://matrix67.com/blog/archives/5094)
特性：
1. 乾淨高對比白底主題 (White / Light Theme)，線條鮮明，色塊層次豐富。
2. 三角形依序「亮邊標示 -> 放大移位 -> 接續下一個」，節奏清晰明確。
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import manimgx as m
import numpy as np
from manimgx_tw_helper import CHINESE_FONT, CaptionItem, TWScene, YunJheVoice

# 9:16 短影音直幅設定 (1080x1920)
m.config.pixel_width = 1080
m.config.pixel_height = 1920
m.config.frame_height = 16.0  # 自動換算 frame_width = 9.0


class PtolemyTheoremVertical(TWScene):
    voice = YunJheVoice(rate="+12%", pitch="+8Hz")

    def make_caption(
        self,
        *items: CaptionItem,
        font_size: float = 28,
        math_font_size: float = 32,
        buff: float = 0.12,
        edge_buff: float = 0.85,
        text_color: str = "#1A202C",
    ) -> m.VGroup:
        """建立適用於白底主題的高對比深色字幕。"""
        parts: list[m.Mobject] = []
        for item in items:
            if isinstance(item, m.Mobject):
                parts.append(item)
            elif isinstance(item, tuple) and len(item) == 2 and item[0] == "math":
                parts.append(m.MathTex(item[1], font_size=math_font_size, color=text_color))
            else:
                parts.append(
                    m.Text(str(item), font=CHINESE_FONT, font_size=font_size, color=text_color)
                )
        group = m.VGroup(*parts).arrange(m.RIGHT, buff=buff)
        group.to_edge(m.DOWN, buff=edge_buff)
        return group

    def construct(self) -> None:
        # =========================================================================
        # 0. 白底主題視覺調色盤 (High-Contrast Clean Light Palette)
        # =========================================================================
        COLOR_BG = "#FFFFFF"
        COLOR_TEXT_MAIN = "#1A202C"      # 深炭灰主文字
        COLOR_TEXT_MUTED = "#718096"     # 次級標籤灰
        COLOR_CIRCLE = "#718096"         # 外接圓深灰
        COLOR_CHORD = "#1A202C"          # 四邊形外邊黑色實線
        COLOR_DIAG_E = "#2563EB"         # AC = e (鮮明皇室藍)
        COLOR_DIAG_F = "#EA580C"         # BD = f (鮮明琥珀橘)

        # 三大三角形主配色
        COLOR_TRI_MID_STROKE = "#475569"
        COLOR_TRI_MID_FILL = "#E2E8F0"   # 中間三角形 (清爽雅灰)

        COLOR_TRI_LEFT_STROKE = "#0284C7"
        COLOR_TRI_LEFT_FILL = "#BAE6FD"  # 左側三角形 (明亮晴空藍)

        COLOR_TRI_RIGHT_STROKE = "#E11D48"
        COLOR_TRI_RIGHT_FILL = "#FECDD3" # 右側三角形 (溫潤珊瑚粉)

        # 角度標註色 (深色飽和度，在白底上極清晰)
        COLOR_ALPHA = "#0D9488"          # α (深青綠)
        COLOR_BETA = "#D97706"           # β (溫暖金黃)
        COLOR_GAMMA = "#16A34A"          # γ (生機綠)
        COLOR_DELTA = "#7C3AED"          # δ (典雅紫)

        COLOR_GOLD = "#B45309"           # 強調金框 (深金黃)

        # 背景白底鋪設
        bg = m.Rectangle(
            width=9.0,
            height=16.0,
            fill_color=COLOR_BG,
            fill_opacity=1.0,
            stroke_width=0,
        )
        self.add(bg)

        # =========================================================================
        # 1. 頂部 HUD 標題與目標公式
        # =========================================================================
        title_badge = m.VGroup(
            m.Text("托勒密定理", font=CHINESE_FONT, font_size=38, weight="BOLD", color=COLOR_TEXT_MAIN),
            m.Text("Ptolemy 定理的無字證明", font=CHINESE_FONT, font_size=22, color=COLOR_TEXT_MUTED),
        ).arrange(m.DOWN, buff=0.12).move_to([0, 6.7, 0])

        target_formula_box = m.RoundedRectangle(
            corner_radius=0.18,
            width=6.8,
            height=0.95,
            fill_color="#F8FAFC",
            fill_opacity=1.0,
            stroke_color="#CBD5E1",
            stroke_width=1.8,
        ).move_to([0, 5.5, 0])

        target_formula = m.MathTex(
            r"a \cdot c + b \cdot d = e \cdot f",
            font_size=36,
            color=COLOR_TEXT_MAIN,
        ).move_to(target_formula_box.get_center())

        header_group = m.VGroup(title_badge, target_formula_box, target_formula)

        # =========================================================================
        # 2. 上方：圓內接四邊形精確幾何建立
        # =========================================================================
        R = 1.70
        center_circle = np.array([0.0, 2.75, 0.0])

        degA, degB, degC, degD = 200.0, 105.0, 15.0, 295.0
        radA = np.radians(degA)
        radB = np.radians(degB)
        radC = np.radians(degC)
        radD = np.radians(degD)

        posA = center_circle + R * np.array([np.cos(radA), np.sin(radA), 0.0])
        posB = center_circle + R * np.array([np.cos(radB), np.sin(radB), 0.0])
        posC = center_circle + R * np.array([np.cos(radC), np.sin(radC), 0.0])
        posD = center_circle + R * np.array([np.cos(radD), np.sin(radD), 0.0])

        circ = m.Circle(radius=R, color=COLOR_CIRCLE, stroke_width=2.4).move_to(center_circle)

        # 四邊與對角線
        line_AB = m.Line(posA, posB, color=COLOR_CHORD, stroke_width=3.2)
        line_BC = m.Line(posB, posC, color=COLOR_CHORD, stroke_width=3.2)
        line_CD = m.Line(posC, posD, color=COLOR_CHORD, stroke_width=3.2)
        line_DA = m.Line(posD, posA, color=COLOR_CHORD, stroke_width=3.2)

        line_AC = m.Line(posA, posC, color=COLOR_DIAG_E, stroke_width=2.5)  # e
        line_BD = m.Line(posB, posD, color=COLOR_DIAG_F, stroke_width=2.5)  # f

        # 頂點圓點與字母
        dots = m.VGroup(
            m.Dot(posA, radius=0.075, color=COLOR_TEXT_MAIN),
            m.Dot(posB, radius=0.075, color=COLOR_TEXT_MAIN),
            m.Dot(posC, radius=0.075, color=COLOR_TEXT_MAIN),
            m.Dot(posD, radius=0.075, color=COLOR_TEXT_MAIN),
        ).set_z_index(6)

        lbl_A = m.MathTex("A", font_size=36, color=COLOR_TEXT_MAIN).move_to(posA + np.array([-0.34, -0.16, 0.0])).set_z_index(7)
        lbl_B = m.MathTex("B", font_size=36, color=COLOR_TEXT_MAIN).move_to(posB + np.array([0.0, 0.36, 0.0])).set_z_index(7)
        lbl_C = m.MathTex("C", font_size=36, color=COLOR_TEXT_MAIN).move_to(posC + np.array([0.36, 0.06, 0.0])).set_z_index(7)
        lbl_D = m.MathTex("D", font_size=36, color=COLOR_TEXT_MAIN).move_to(posD + np.array([0.22, -0.32, 0.0])).set_z_index(7)
        vertex_labels = m.VGroup(lbl_A, lbl_B, lbl_C, lbl_D)

        # 邊長標籤 (徑向向外，絕不干擾圓周)
        r_lbl = R + 0.30
        ang_mid_a = np.radians((degA + degB) / 2.0)
        ang_mid_b = np.radians((degB + degC) / 2.0)
        ang_mid_c = np.radians((degC + degD - 360.0) / 2.0)
        ang_mid_d = np.radians((degD + degA) / 2.0)

        lbl_a = m.MathTex("a", font_size=32, color=COLOR_TEXT_MAIN).move_to(center_circle + r_lbl * np.array([np.cos(ang_mid_a), np.sin(ang_mid_a), 0.0])).set_z_index(7)
        lbl_b = m.MathTex("b", font_size=32, color=COLOR_TEXT_MAIN).move_to(center_circle + r_lbl * np.array([np.cos(ang_mid_b), np.sin(ang_mid_b), 0.0])).set_z_index(7)
        lbl_c = m.MathTex("c", font_size=32, color=COLOR_TEXT_MAIN).move_to(center_circle + r_lbl * np.array([np.cos(ang_mid_c), np.sin(ang_mid_c), 0.0])).set_z_index(7)
        lbl_d = m.MathTex("d", font_size=32, color=COLOR_TEXT_MAIN).move_to(center_circle + r_lbl * np.array([np.cos(ang_mid_d), np.sin(ang_mid_d), 0.0])).set_z_index(7)

        lbl_e = m.MathTex("e", font_size=32, color=COLOR_DIAG_E).move_to((posA + posC) / 2 + np.array([0.05, -0.28, 0.0])).set_z_index(7)
        lbl_f = m.MathTex("f", font_size=32, color=COLOR_DIAG_F).move_to((posB + posD) / 2 + np.array([-0.28, 0.10, 0.0])).set_z_index(7)
        edge_labels = m.VGroup(lbl_a, lbl_b, lbl_c, lbl_d, lbl_e, lbl_f)

        quad_group = m.VGroup(
            circ, line_AB, line_BC, line_CD, line_DA, line_AC, line_BD, dots, vertex_labels, edge_labels
        )

        # =========================================================================
        # 3. 圓周角扇形與標註 (α, β, γ, δ)
        # =========================================================================
        def make_sector_mark(
            p_vertex: np.ndarray,
            p1: np.ndarray,
            p2: np.ndarray,
            radius: float,
            label_tex: str,
            label_dist: float = 0.54,
            color: str = COLOR_TEXT_MAIN,
            font_size: int = 26,
            z_index: int = 4,
        ) -> m.VGroup:
            v1 = (p1 - p_vertex)[:2]
            v2 = (p2 - p_vertex)[:2]
            a1 = float(np.arctan2(v1[1], v1[0]))
            a2 = float(np.arctan2(v2[1], v2[0]))
            dth = (a2 - a1) % (2.0 * np.pi)
            if dth > np.pi:
                start = a2
                sweep = 2.0 * np.pi - dth
            else:
                start = a1
                sweep = dth

            sec = m.Sector(
                radius=radius,
                start_angle=start,
                angle=sweep,
                arc_center=p_vertex,
                fill_color=color,
                fill_opacity=0.30,
                stroke_color=color,
                stroke_width=1.5,
            ).set_z_index(z_index)
            mid_ang = start + sweep / 2.0
            pos_lbl = p_vertex + np.array([np.cos(mid_ang), np.sin(mid_ang), 0.0]) * label_dist
            txt = m.MathTex(label_tex, font_size=font_size, color=color).move_to(pos_lbl).set_z_index(z_index + 1)
            return m.VGroup(sec, txt)

        # 4 對圓周角
        ang_alpha_D = make_sector_mark(posD, posB, posA, 0.40, r"\alpha", 0.62, COLOR_ALPHA)
        ang_alpha_C = make_sector_mark(posC, posB, posA, 0.40, r"\alpha", 0.62, COLOR_ALPHA)

        ang_beta_A = make_sector_mark(posA, posC, posB, 0.40, r"\beta", 0.62, COLOR_BETA)
        ang_beta_D = make_sector_mark(posD, posC, posB, 0.40, r"\beta", 0.62, COLOR_BETA)

        ang_gamma_A = make_sector_mark(posA, posD, posC, 0.40, r"\gamma", 0.62, COLOR_GAMMA)
        ang_gamma_B = make_sector_mark(posB, posD, posC, 0.40, r"\gamma", 0.62, COLOR_GAMMA)

        ang_delta_B = make_sector_mark(posB, posA, posD, 0.40, r"\delta", 0.62, COLOR_DELTA)
        ang_delta_C = make_sector_mark(posC, posA, posD, 0.40, r"\delta", 0.62, COLOR_DELTA)

        angles_group = m.VGroup(
            ang_alpha_D, ang_alpha_C,
            ang_beta_A, ang_beta_D,
            ang_gamma_A, ang_gamma_B,
            ang_delta_B, ang_delta_C,
        )

        # 內角和 180 度公式牌
        sum_box = m.RoundedRectangle(
            corner_radius=0.15,
            width=5.2,
            height=0.75,
            fill_color="#F1F5F9",
            fill_opacity=1.0,
            stroke_color="#CBD5E1",
            stroke_width=1.6,
        ).move_to([0, 0.35, 0])

        sum_angles_eq = m.MathTex(
            r"\alpha + \beta + \gamma + \delta = 180^\circ",
            font_size=32,
            color=COLOR_BETA,
        ).move_to(sum_box.get_center())

        angle_sum_badge = m.VGroup(sum_box, sum_angles_eq)

        # =========================================================================
        # 4. 下方：平行四邊形拼接精確幾何計算
        # =========================================================================
        a0 = 2.0 * np.sin(np.radians((degA - degB) % 360 / 2.0))
        b0 = 2.0 * np.sin(np.radians((degB - degC) % 360 / 2.0))
        c0 = 2.0 * np.sin(np.radians((degC - degD) % 360 / 2.0))
        d0 = 2.0 * np.sin(np.radians((degD - degA) % 360 / 2.0))
        e0 = 2.0 * np.sin(np.radians((degA - degC) % 360 / 2.0))
        f0 = 2.0 * np.sin(np.radians((degB - degD) % 360 / 2.0))

        val_beta = np.arcsin(b0 / 2.0)
        val_gamma = np.arcsin(c0 / 2.0)

        scale_p = 1.35
        w_base = e0 * f0 * scale_p
        h_poly = a0 * b0 * np.sin(val_beta + val_gamma) * scale_p
        dx_side = a0 * b0 * np.cos(val_beta + val_gamma) * scale_p

        x_left = -0.5 * (w_base + dx_side)
        y_bottom = -2.55 - 0.5 * h_poly

        P_BL = np.array([x_left, y_bottom, 0.0])
        P_BR = P_BL + np.array([w_base, 0.0, 0.0])
        P_TL = P_BL + np.array([dx_side, h_poly, 0.0])
        P_TR = P_BR + np.array([dx_side, h_poly, 0.0])
        P_top = P_TL + np.array([a0 * c0 * scale_p, 0.0, 0.0])

        # 下方三大實體三角形
        poly_mid = m.Polygon(
            P_BL, P_BR, P_top,
            fill_color=COLOR_TRI_MID_FILL,
            fill_opacity=0.60,
            stroke_color=COLOR_TRI_MID_STROKE,
            stroke_width=2.5,
        )

        poly_left = m.Polygon(
            P_BL, P_top, P_TL,
            fill_color=COLOR_TRI_LEFT_FILL,
            fill_opacity=0.60,
            stroke_color=COLOR_TRI_LEFT_STROKE,
            stroke_width=2.5,
        )

        poly_right = m.Polygon(
            P_BR, P_TR, P_top,
            fill_color=COLOR_TRI_RIGHT_FILL,
            fill_opacity=0.60,
            stroke_color=COLOR_TRI_RIGHT_STROKE,
            stroke_width=2.5,
        )

        # 下方邊長標籤 (提高 z_index 確保永遠位於多邊形色塊之上，色彩深濃清晰)
        lbl_ef = m.MathTex(r"e \cdot f", font_size=32, color=COLOR_TEXT_MAIN).next_to(
            m.Line(P_BL, P_BR), m.DOWN, buff=0.22
        ).set_z_index(10)
        lbl_af = m.MathTex(r"a \cdot f", font_size=30, color=COLOR_TEXT_MAIN).move_to(
            (P_BL + P_top) / 2 + np.array([-0.36, 0.12, 0.0])
        ).set_z_index(10)
        lbl_bf = m.MathTex(r"b \cdot f", font_size=30, color=COLOR_TEXT_MAIN).move_to(
            (P_BR + P_top) / 2 + np.array([0.36, 0.12, 0.0])
        ).set_z_index(10)

        lbl_ac = m.MathTex(r"a \cdot c", font_size=32, color=COLOR_TRI_LEFT_STROKE).next_to(
            m.Line(P_TL, P_top), m.UP, buff=0.20
        ).set_z_index(10)
        lbl_bd = m.MathTex(r"b \cdot d", font_size=32, color=COLOR_TRI_RIGHT_STROKE).next_to(
            m.Line(P_top, P_TR), m.UP, buff=0.20
        ).set_z_index(10)
        lbl_ab_left = m.MathTex(r"a \cdot b", font_size=32, color=COLOR_TEXT_MAIN).next_to(
            m.Line(P_BL, P_TL), m.LEFT, buff=0.22
        ).set_z_index(10)
        lbl_ab_right = m.MathTex(r"a \cdot b", font_size=32, color=COLOR_TEXT_MAIN).next_to(
            m.Line(P_BR, P_TR), m.RIGHT, buff=0.22
        ).set_z_index(10)

        # 頂部各角標記 (β, γ+δ, α)
        ang_top_beta = make_sector_mark(P_top, P_BL, P_TL, 0.42, r"\beta", 0.65, COLOR_BETA, font_size=24, z_index=10)
        ang_top_mid = make_sector_mark(P_top, P_BR, P_BL, 0.38, r"\gamma+\delta", 0.70, COLOR_TEXT_MUTED, font_size=24, z_index=10)
        ang_top_alpha = make_sector_mark(P_top, P_TR, P_BR, 0.42, r"\alpha", 0.65, COLOR_ALPHA, font_size=24, z_index=10)
        top_angles_group = m.VGroup(ang_top_beta, ang_top_mid, ang_top_alpha)

        # 四角落角度標記
        ang_bl_gamma = make_sector_mark(P_BL, P_TL, P_top, 0.48, r"\gamma", 0.75, COLOR_GAMMA, font_size=24, z_index=10)
        ang_bl_beta = make_sector_mark(P_BL, P_top, P_BR, 0.48, r"\beta", 0.75, COLOR_BETA, font_size=24, z_index=10)

        ang_br_alpha = make_sector_mark(P_BR, P_BL, P_top, 0.48, r"\alpha", 0.75, COLOR_ALPHA, font_size=24, z_index=10)
        ang_br_delta = make_sector_mark(P_BR, P_top, P_TR, 0.48, r"\delta", 0.75, COLOR_DELTA, font_size=24, z_index=10)

        ang_tl_comb = make_sector_mark(P_TL, P_top, P_BL, 0.45, r"\alpha+\delta", 0.78, COLOR_ALPHA, font_size=24, z_index=10)
        ang_tr_comb = make_sector_mark(P_TR, P_BR, P_top, 0.45, r"\beta+\gamma", 0.78, COLOR_BETA, font_size=24, z_index=10)

        corner_angles_group = m.VGroup(
            ang_bl_gamma, ang_bl_beta,
            ang_br_alpha, ang_br_delta,
            ang_tl_comb, ang_tr_comb,
        )

        # 頂部整段長度
        top_full_line = m.Line(P_TL, P_TR, color=COLOR_GOLD, stroke_width=3.6).set_z_index(11)
        lbl_top_sum = m.MathTex(
            r"a \cdot c + b \cdot d",
            font_size=34,
            color=COLOR_GOLD,
        ).next_to(top_full_line, m.UP, buff=0.36).set_z_index(12)

        bot_full_line = m.Line(P_BL, P_BR, color=COLOR_GOLD, stroke_width=3.6).set_z_index(11)

        # 上方目標三角形亮邊標示圖形 (半透明 0.35 + 粗邊框 4.5，確保底層字母依然可讀)
        tri_ABC_high = m.Polygon(
            posA, posB, posC,
            fill_color=COLOR_TRI_MID_FILL,
            fill_opacity=0.35,
            stroke_color=COLOR_TRI_MID_STROKE,
            stroke_width=4.5,
        ).set_z_index(8)

        tri_BCD_high = m.Polygon(
            posB, posC, posD,
            fill_color=COLOR_TRI_LEFT_FILL,
            fill_opacity=0.35,
            stroke_color=COLOR_TRI_LEFT_STROKE,
            stroke_width=4.5,
        ).set_z_index(8)

        tri_ABD_high = m.Polygon(
            posA, posB, posD,
            fill_color=COLOR_TRI_RIGHT_FILL,
            fill_opacity=0.35,
            stroke_color=COLOR_TRI_RIGHT_STROKE,
            stroke_width=4.5,
        ).set_z_index(8)

        # =========================================================================
        # 5. 分鏡動畫演繹流程（採用 3 號幹練清晰配音全程同步）
        # =========================================================================

        # --- Beat 1A: 先畫圓 ---
        cap1_a = self.make_caption("考慮一個外接圓")
        self.say(
            "考慮一個外接圓。",
            m.FadeIn(header_group),
            m.FadeIn(cap1_a),
            m.Create(circ, run_time=1.2),
        )

        # --- Beat 1B: 再畫出內接四邊形 ---
        cap1_b = self.make_caption("圓內接四邊形：邊長順次記為", ("math", "a, b, c, d"))
        self.say(
            "建立圓內接四邊形，邊長依序記為 a、b、c、d。",
            m.FadeOut(cap1_a),
            m.FadeIn(cap1_b),
            m.Create(m.VGroup(line_AB, line_BC, line_CD, line_DA), run_time=1.4),
            m.FadeIn(dots),
            m.FadeIn(vertex_labels),
            m.FadeIn(edge_labels[:4]),
        )

        # --- Beat 2: 對角線 e 與 f ---
        cap2 = self.make_caption("對角線分別記為", ("math", "e"), "與", ("math", "f"))
        self.say(
            "兩條對角線長度分別記為 e 和 f。",
            m.FadeOut(cap1_b),
            m.FadeIn(cap2),
            m.Create(line_AC),
            m.Create(line_BD),
            m.FadeIn(lbl_e),
            m.FadeIn(lbl_f),
        )

        # --- Beat 3: 同弧圓周角相等 ---
        cap3 = self.make_caption("同弧所對圓周角相等，記為", ("math", r"\alpha, \beta, \gamma, \delta"))
        self.say(
            "由圓周角定理，同弧所對的圓周角相等，記為阿爾法、貝塔、伽瑪、德爾塔。",
            m.FadeOut(cap2),
            m.FadeIn(cap3),
            m.FadeIn(angles_group, lag_ratio=0.15),
        )

        # --- Beat 4: 圓內接四邊形對角互補 ---
        cap4 = self.make_caption("圓內接四邊形對角互補：四角總和為 180°")
        self.say(
            "圓內接四邊形對角互補，四個內角總和恰好為一百八十度。",
            m.FadeOut(cap3),
            m.FadeIn(cap4),
            m.FadeIn(angle_sum_badge, shift=m.UP * 0.1),
        )

        # =========================================================================
        # 【三角形放大移位】：一次處理一個，就位後角度與邊長標示再出現
        # =========================================================================

        # -------------------------------------------------------------------------
        # [Triangle 1/3] 中間三角形 △ABC
        # -------------------------------------------------------------------------
        cap5 = self.make_caption("將三角形", ("math", r"\triangle ABC"), "放大", ("math", "f"), "倍")
        self.say(
            "首先，將三角形 A B C 放大 f 倍並移至下方。",
            m.FadeOut(cap4),
            m.FadeIn(cap5),
            m.Create(tri_ABC_high, run_time=0.8),
            m.TransformFromCopy(tri_ABC_high, poly_mid, run_time=1.4),
            m.FadeOut(tri_ABC_high, run_time=0.4),
        )

        cap5_seated = self.make_caption("就位後邊長為", ("math", r"e \cdot f, a \cdot f, b \cdot f"))
        self.say(
            "就位後，底邊長度唯 e f，兩腰分別唯 a f 和 b f。",
            m.FadeOut(cap5),
            m.FadeIn(cap5_seated),
            m.FadeIn(lbl_ef),
            m.FadeIn(lbl_af),
            m.FadeIn(lbl_bf),
            m.FadeIn(ang_top_mid),
            m.FadeIn(ang_bl_beta),
            m.FadeIn(ang_br_alpha),
        )

        # -------------------------------------------------------------------------
        # [Triangle 2/3] 左側三角形 △BCD
        # -------------------------------------------------------------------------
        cap6 = self.make_caption("將三角形", ("math", r"\triangle BCD"), "放大", ("math", "a"), "倍")
        self.say(
            "接著，將三角形 B C D 放大 a 倍，移動拼接到左側。",
            m.FadeOut(cap5_seated),
            m.FadeIn(cap6),
            m.Create(tri_BCD_high, run_time=0.8),
            m.TransformFromCopy(tri_BCD_high, poly_left, run_time=1.4),
            m.FadeOut(tri_BCD_high, run_time=0.4),
        )

        cap6_seated = self.make_caption("公共邊", ("math", r"a \cdot f"), "吻合，邊長為", ("math", r"a \cdot c, a \cdot b"))
        self.say(
            "公共邊 a f 完美吻合，左上邊長唯 a c，外側腰長唯 a b。",
            m.FadeOut(cap6),
            m.FadeIn(cap6_seated),
            m.FadeIn(lbl_ac),
            m.FadeIn(lbl_ab_left),
            m.FadeIn(ang_top_beta),
            m.FadeIn(ang_bl_gamma),
            m.FadeIn(ang_tl_comb),
        )

        # -------------------------------------------------------------------------
        # [Triangle 3/3] 右側三角形 △ABD
        # -------------------------------------------------------------------------
        cap7 = self.make_caption("將三角形", ("math", r"\triangle ABD"), "放大", ("math", "b"), "倍")
        self.say(
            "最後，將三角形 A B D 放大 b 倍，移動拼接到右側。",
            m.FadeOut(cap6_seated),
            m.FadeIn(cap7),
            m.Create(tri_ABD_high, run_time=0.8),
            m.TransformFromCopy(tri_ABD_high, poly_right, run_time=1.4),
            m.FadeOut(tri_ABD_high, run_time=0.4),
        )

        cap7_seated = self.make_caption("公共邊", ("math", r"b \cdot f"), "吻合，邊長為", ("math", r"b \cdot d, a \cdot b"))
        self.say(
            "公共邊 b f 吻合，右上邊長唯 b d，外側腰長同樣唯 a b。",
            m.FadeOut(cap7),
            m.FadeIn(cap7_seated),
            m.FadeIn(lbl_bd),
            m.FadeIn(lbl_ab_right),
            m.FadeIn(ang_top_alpha),
            m.FadeIn(ang_br_delta),
            m.FadeIn(ang_tr_comb),
        )

        # =========================================================================
        # 6. 頂角共線與平行四邊形結論收尾
        # =========================================================================
        cap8 = self.make_caption("頂角總和", ("math", r"\beta + (\gamma + \delta) + \alpha = 180^\circ"), "，頂部共線成直線段")
        self.say(
            "觀察上方頂角，總和剛好是一百八十度，頂部完全共線成一條水平直線段。",
            m.FadeOut(cap7_seated),
            m.FadeIn(cap8),
            m.Create(top_full_line),
            m.FadeOut(lbl_ac),
            m.FadeOut(lbl_bd),
            m.FadeIn(lbl_top_sum),
        )

        cap9 = self.make_caption("左右邊長皆為", ("math", r"a \cdot b"), "且平行，構成平行四邊形！")
        self.say(
            "左右兩側對邊長度皆唯 a b 且彼此平行，這是一個完整的平行四邊形！",
            m.FadeOut(cap8),
            m.FadeIn(cap9),
            m.Create(bot_full_line),
        )

        cap10 = self.make_caption("上下對邊相等：", ("math", r"a \cdot c + b \cdot d = e \cdot f"), "（證畢）")
        highlight_box = m.SurroundingRectangle(
            target_formula_box,
            buff=0.10,
            color=COLOR_GOLD,
            stroke_width=3.6,
        )

        self.say(
            "因此上下對邊相等，a c 加 b d 等於 e f，托勒密定理得證！",
            m.FadeOut(cap9),
            m.FadeIn(cap10),
            m.Create(highlight_box),
            m.Indicate(target_formula, color=COLOR_GOLD, scale_factor=1.15),
        )
        self.wait(1.5)
