"""圓弧度數的幾何性質 - 16:9 橫幅明亮主題解說 (Light Theme).

依據教師回饋影片 (arc_drgree_fix.mp4) 指示精確製作：
1. 三個同心圓由同一圓心向外展開。
2. 兩條垂直軸線切出第一象限 1/4 圓弧 (90°)。
3. 三段圓弧平滑拉直為平行線段，起點對齊，呈現半徑越大弧長越長 (L1 < L2 < L3)。
4. 線段捲回圓弧，探討「圓弧的度數」。
5. 教師核心教學法：「度數就是前進時轉彎轉過的度數」。
   - 三段圓弧起點標出點與切向箭頭 (向上)，右側同步記錄初始方向。
   - 原起點與初始箭頭保持留存。
   - 分身沿圓弧前進，切向箭頭隨路徑平滑偏轉。
   - 抵達終點 (向左)，比較初始與終點方向，三者皆轉過 90°！
   - 偏轉角 = 圓心角 = 90°，因此三段圓弧度數完全相同！
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import manimgx as m
import numpy as np
from ArcDegree.narration_scene import NarratedScene
from manimgx_tw_helper import CHINESE_FONT

# 16:9 橫幅標準解析度 (1920x1080)
m.config.pixel_width = 1920
m.config.pixel_height = 1080
m.config.frame_height = 8.0
m.config.background_color = "#F8FAFC"  # 明亮清爽底色 (Slate 50)


class ArcDegreeLandscapeLight(NarratedScene):
    narration_root = Path(__file__).resolve().parent / "narration_edge_light"
    timeline_root = narration_root

    def make_right_angle(
        self,
        corner: np.ndarray,
        p1: np.ndarray,
        p2: np.ndarray,
        size: float = 0.28,
        color: m.ParsableManimColor = "#2563EB",
        stroke_width: float = 2.4,
    ) -> m.VMobject:
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

    def show_caption(self, text: str) -> None:
        caption = m.Text(text, font=CHINESE_FONT, font_size=23, color="#0F172A")
        caption.to_edge(m.DOWN, buff=0.45)
        old = getattr(self, "_caption_text", None)
        if old is None:
            self.play(m.FadeIn(caption), run_time=0.3)
        else:
            self.play(m.ReplacementTransform(old, caption), run_time=0.3)
        self._caption_text = caption

    def construct(self) -> None:
        # =====================================================
        # 0. 明亮風格配色與參數
        # =====================================================
        C_CENTER = "#0F172A"         # 深深灰圓心
        C_AXIS = "#64748B"           # 軸線 Slate 500
        C_CIRC_STROKE = "#CBD5E1"    # 同心圓 Slate 300
        C_TEXT_MAIN = "#0F172A"      # 主文字 Slate 900
        C_TEXT_MUTED = "#475569"     # 次文字 Slate 600
        C_BLUE = "#2563EB"           # 強調藍

        # 三段圓弧專屬高對比配色 (綠、橘、紅)
        C_ARC1 = "#059669"           # 內弧：翠綠
        C_ARC2 = "#D97706"           # 中弧：琥珀暖橘
        C_ARC3 = "#DC2626"           # 外弧：珊瑚緋紅
        COLORS = [C_ARC1, C_ARC2, C_ARC3]

        r1, r2, r3 = 1.30, 2.15, 3.00
        RADII = [r1, r2, r3]
        O_INIT = np.array([0.0, 0.0, 0.0])

        # 頂部固定主題標題 (避開垂直軸線頂端 y=3.12)
        title_group = m.VGroup(
            m.Text("圓弧的長度與度數", font=CHINESE_FONT, font_size=26, weight=m.BOLD, color=C_TEXT_MAIN),
            m.Text("從切線轉彎的角度，看見圓弧的度數本質", font=CHINESE_FONT, font_size=18, color=C_TEXT_MUTED),
        ).arrange(m.RIGHT, buff=0.4).to_edge(m.UP, buff=0.25)
        self.play(m.FadeIn(title_group), run_time=0.6)

        # =====================================================
        # 1. 步驟一：圓心與三個同心圓展開
        # =====================================================
        self.begin_narration("light", 1)
        self.show_caption("以同一個圓心，向外展開三個不同半徑的同心圓。")

        center_dot = m.Dot(O_INIT, radius=0.08, color=C_CENTER)
        label_o = m.Text("O", font=CHINESE_FONT, font_size=20, weight=m.BOLD, color=C_TEXT_MAIN).next_to(center_dot, m.DL, buff=0.12)
        circle1 = m.Circle(radius=r1, color=C_CIRC_STROKE, stroke_width=2.2).move_to(O_INIT)
        circle2 = m.Circle(radius=r2, color=C_CIRC_STROKE, stroke_width=2.2).move_to(O_INIT)
        circle3 = m.Circle(radius=r3, color=C_CIRC_STROKE, stroke_width=2.2).move_to(O_INIT)

        self.play(m.FadeIn(center_dot, scale=1.3), m.FadeIn(label_o), run_time=0.5)
        self.play(
            m.Create(circle1, run_time=0.7),
            m.Create(circle2, run_time=0.8),
            m.Create(circle3, run_time=0.9),
        )
        self.wait(0.6)

        # =====================================================
        # 2. 步驟二：通過圓心畫兩條互相垂直的線，切出 90 度
        # =====================================================
        self.begin_narration("light", 2)
        self.show_caption("通過圓心畫出兩條垂直軸線，切出四分之一圓，也就是九十度。")

        # 軸線長度設定為 3.12，高於外圓半徑 3.0，但嚴格避開上方標題 (y=3.35) 與下方字幕 (y=-3.32)
        axis_len = 3.12
        line_h = m.Line(O_INIT + np.array([-axis_len, 0, 0]), O_INIT + np.array([axis_len, 0, 0]), stroke_color=C_AXIS, stroke_width=2.0)
        line_v = m.Line(O_INIT + np.array([0, -axis_len, 0]), O_INIT + np.array([0, axis_len, 0]), stroke_color=C_AXIS, stroke_width=2.0)

        ra_mark = self.make_right_angle(
            O_INIT,
            O_INIT + np.array([1, 0, 0]),
            O_INIT + np.array([0, 1, 0]),
            size=0.28,
            color=C_BLUE,
            stroke_width=2.4,
        )
        deg_90_text = m.Text("90°", font=CHINESE_FONT, font_size=18, weight=m.BOLD, color=C_BLUE).move_to(O_INIT + np.array([0.45, 0.45, 0]))

        self.play(
            m.Create(line_h, run_time=0.7),
            m.Create(line_v, run_time=0.7),
        )
        self.play(m.Create(ra_mark), m.FadeIn(deg_90_text), run_time=0.5)
        self.wait(0.8)

        # =====================================================
        # 3. 步驟三：聚焦第一象限的三段 1/4 圓弧
        # =====================================================
        self.begin_narration("light", 3)
        self.show_caption("聚焦在第一象限的三段圓弧。半徑不同，長度也明顯不同。")

        arc1 = m.Arc(radius=r1, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=C_ARC1, stroke_width=6.0)
        arc2 = m.Arc(radius=r2, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=C_ARC2, stroke_width=6.0)
        arc3 = m.Arc(radius=r3, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=C_ARC3, stroke_width=6.0)

        dots_start = m.VGroup(
            m.Dot(O_INIT + np.array([r1, 0, 0]), radius=0.075, color=C_ARC1),
            m.Dot(O_INIT + np.array([r2, 0, 0]), radius=0.075, color=C_ARC2),
            m.Dot(O_INIT + np.array([r3, 0, 0]), radius=0.075, color=C_ARC3),
        )
        dots_end = m.VGroup(
            m.Dot(O_INIT + np.array([0, r1, 0]), radius=0.075, color=C_ARC1),
            m.Dot(O_INIT + np.array([0, r2, 0]), radius=0.075, color=C_ARC2),
            m.Dot(O_INIT + np.array([0, r3, 0]), radius=0.075, color=C_ARC3),
        )

        labels_abc_start = m.VGroup(
            m.Text("A", font=CHINESE_FONT, font_size=18, weight=m.BOLD, color=C_ARC1).move_to(dots_start[0].get_center() + np.array([-0.18, -0.22, 0])),
            m.Text("B", font=CHINESE_FONT, font_size=18, weight=m.BOLD, color=C_ARC2).move_to(dots_start[1].get_center() + np.array([-0.18, -0.22, 0])),
            m.Text("C", font=CHINESE_FONT, font_size=18, weight=m.BOLD, color=C_ARC3).move_to(dots_start[2].get_center() + np.array([-0.18, -0.22, 0])),
        )

        self.play(
            circle1.animate.set_stroke(opacity=0.20),
            circle2.animate.set_stroke(opacity=0.20),
            circle3.animate.set_stroke(opacity=0.20),
            m.Create(arc1, run_time=0.6),
            m.Create(arc2, run_time=0.7),
            m.Create(arc3, run_time=0.8),
            m.FadeIn(dots_start),
            m.FadeIn(dots_end),
            m.FadeIn(labels_abc_start),
        )
        self.wait(1.0)

        # =====================================================
        # 4. 步驟四：圖形平移向左，三段圓弧向右平滑拉直
        # =====================================================
        SHIFT_VEC = np.array([-3.2, 0.0, 0.0])
        O_LEFT = O_INIT + SHIFT_VEC

        left_assembly = m.VGroup(
            center_dot, label_o, circle1, circle2, circle3,
            line_h, line_v, ra_mark, deg_90_text,
            arc1, arc2, arc3, dots_start, dots_end, labels_abc_start,
        )

        self.begin_narration("light", 4)
        self.show_caption("圖形平移向左，將三段圓弧平滑拉直為線段，起點對齊。")

        self.play(
            left_assembly.animate.shift(SHIFT_VEC),
            run_time=0.9,
        )
        self.wait(0.4)

        # 原地保留淡色幽靈弧
        ghost_arc1 = arc1.copy().set_stroke(opacity=0.25, width=3.0)
        ghost_arc2 = arc2.copy().set_stroke(opacity=0.25, width=3.0)
        ghost_arc3 = arc3.copy().set_stroke(opacity=0.25, width=3.0)
        self.add(ghost_arc1, ghost_arc2, ghost_arc3)

        # 右側直線段目標位置與長度 (L = r * pi / 2)
        X_START = 0.8
        L1 = r1 * np.pi / 2  # ~ 2.04
        L2 = r2 * np.pi / 2  # ~ 3.38
        L3 = r3 * np.pi / 2  # ~ 4.71

        Y_POS1 = -1.2
        Y_POS2 = 0.0
        Y_POS3 = 1.2

        line_seg1 = m.Line([X_START, Y_POS1, 0], [X_START + L1, Y_POS1, 0], stroke_color=C_ARC1, stroke_width=6.0)
        line_seg2 = m.Line([X_START, Y_POS2, 0], [X_START + L2, Y_POS2, 0], stroke_color=C_ARC2, stroke_width=6.0)
        line_seg3 = m.Line([X_START, Y_POS3, 0], [X_START + L3, Y_POS3, 0], stroke_color=C_ARC3, stroke_width=6.0)

        align_baseline = m.DashedLine([X_START, -2.0, 0], [X_START, 2.0, 0], stroke_color="#94A3B8", stroke_width=2.0, dash_length=0.12)
        align_label = m.Text("起點對齊", font=CHINESE_FONT, font_size=18, color=C_TEXT_MUTED).move_to([X_START, -2.35, 0])

        end_dot1 = m.Dot([X_START + L1, Y_POS1, 0], radius=0.075, color=C_ARC1)
        end_dot2 = m.Dot([X_START + L2, Y_POS2, 0], radius=0.075, color=C_ARC2)
        end_dot3 = m.Dot([X_START + L3, Y_POS3, 0], radius=0.075, color=C_ARC3)

        self.play(
            m.FadeIn(align_baseline),
            m.FadeIn(align_label),
            m.Transform(arc1, line_seg1),
            m.Transform(arc2, line_seg2),
            m.Transform(arc3, line_seg3),
            run_time=1.3,
        )
        self.play(
            m.FadeIn(end_dot1),
            m.FadeIn(end_dot2),
            m.FadeIn(end_dot3),
            run_time=0.4,
        )
        self.wait(0.8)

        # =====================================================
        # 5. 步驟五：半徑越大，弧長越長 (L1 < L2 < L3)
        # =====================================================
        self.begin_narration("light", 5)
        self.show_caption("可以清楚看見：半徑越長，拉直後的弧長就越長。")

        label_l1 = m.Text("弧長 L₁", font=CHINESE_FONT, font_size=18, color=C_ARC1).next_to(line_seg1, m.RIGHT, buff=0.2)
        label_l2 = m.Text("弧長 L₂", font=CHINESE_FONT, font_size=18, color=C_ARC2).next_to(line_seg2, m.RIGHT, buff=0.2)
        label_l3 = m.Text("弧長 L₃", font=CHINESE_FONT, font_size=18, color=C_ARC3).next_to(line_seg3, m.RIGHT, buff=0.2)

        length_inequality = m.Text("L₁ < L₂ < L₃  (半徑越長，弧長越長)", font=CHINESE_FONT, font_size=20, weight=m.BOLD, color=C_TEXT_MAIN).move_to([3.8, 2.4, 0])

        self.play(
            m.FadeIn(label_l1),
            m.FadeIn(label_l2),
            m.FadeIn(label_l3),
            m.FadeIn(length_inequality),
            run_time=0.6,
        )
        self.play(
            m.Flash(end_dot1, color=C_ARC1, flash_radius=0.25),
            m.Flash(end_dot2, color=C_ARC2, flash_radius=0.25),
            m.Flash(end_dot3, color=C_ARC3, flash_radius=0.25),
            run_time=0.8,
        )
        self.wait(1.0)

        # =====================================================
        # 6. 步驟六：捲回圓弧，提出核心問題：度數呢？
        # =====================================================
        self.begin_narration("light", 6)
        self.show_caption("接著將線段平滑捲回圓弧。弧長雖然不同，那麼圓弧的度數呢？")

        target_arc1 = m.Arc(radius=r1, start_angle=0, angle=np.pi / 2, arc_center=O_LEFT, color=C_ARC1, stroke_width=6.0)
        target_arc2 = m.Arc(radius=r2, start_angle=0, angle=np.pi / 2, arc_center=O_LEFT, color=C_ARC2, stroke_width=6.0)
        target_arc3 = m.Arc(radius=r3, start_angle=0, angle=np.pi / 2, arc_center=O_LEFT, color=C_ARC3, stroke_width=6.0)

        self.play(
            m.FadeOut(end_dot1), m.FadeOut(end_dot2), m.FadeOut(end_dot3),
            m.FadeOut(align_baseline), m.FadeOut(align_label),
            m.FadeOut(label_l1), m.FadeOut(label_l2), m.FadeOut(label_l3),
            m.FadeOut(length_inequality),
            m.Transform(arc1, target_arc1),
            m.Transform(arc2, target_arc2),
            m.Transform(arc3, target_arc3),
            run_time=1.3,
        )
        self.remove(ghost_arc1, ghost_arc2, ghost_arc3)
        self.wait(0.8)

        # =====================================================
        # 7. 步驟七：教師指示——度數本質是轉彎轉過的度數
        # =====================================================
        self.begin_narration("light", 7)
        self.show_caption("圓弧的度數，本質上就是沿著弧線前進時，轉彎轉過的角度。")

        CARD_X = 3.6
        panel_title = m.Text("方向轉彎角度比較 (切線偏轉角)", font=CHINESE_FONT, font_size=20, weight=m.BOLD, color=C_BLUE).move_to([CARD_X, 2.5, 0])
        self.play(m.FadeIn(panel_title), run_time=0.6)
        self.wait(0.8)

        # =====================================================
        # 8. 步驟八：起點出現 A, B, C 與切向箭頭 (向上)，右側同步出現
        # =====================================================
        self.begin_narration("light", 8)
        self.show_caption("在三段圓弧的起點標出點和切向箭頭，同時在右側記錄初始方向。")

        p_start_1 = O_LEFT + np.array([r1, 0, 0])
        p_start_2 = O_LEFT + np.array([r2, 0, 0])
        p_start_3 = O_LEFT + np.array([r3, 0, 0])
        P_STARTS = [p_start_1, p_start_2, p_start_3]

        arrow_len = 0.70
        circle_arrows_init = [
            m.Arrow(p, p + np.array([0, arrow_len, 0]), buff=0, stroke_width=3.5, color=c, max_tip_length_to_length_ratio=0.25)
            for p, c in zip(P_STARTS, COLORS)
        ]

        # 右側三個卡片的樞紐位置 (由上至下：C 外弧, B 中弧, A 內弧)
        PIVOTS = [
            np.array([CARD_X - 0.2, -1.3, 0.0]),  # A 內弧
            np.array([CARD_X - 0.2, 0.1, 0.0]),   # B 中弧
            np.array([CARD_X - 0.2, 1.5, 0.0]),   # C 外弧
        ]
        NAMES = ["A (內弧)", "B (中弧)", "C (外弧)"]

        card_labels = [
            m.Text(name, font=CHINESE_FONT, font_size=19, weight=m.BOLD, color=c).move_to(piv + np.array([-1.9, 0, 0]))
            for name, piv, c in zip(NAMES, PIVOTS, COLORS)
        ]
        card_arrows_init = [
            m.Arrow(piv, piv + np.array([0, arrow_len, 0]), buff=0, stroke_width=3.5, color="#94A3B8", max_tip_length_to_length_ratio=0.25)
            for piv in PIVOTS
        ]

        self.play(
            *[m.Create(arr) for arr in circle_arrows_init],
            *[m.FadeIn(lbl) for lbl in card_labels],
            *[m.Create(arr) for arr in card_arrows_init],
            run_time=1.0,
        )
        self.wait(1.0)

        # =====================================================
        # 9. 步驟九：原點保持在原地，分身同步前進，切線箭頭轉彎
        # =====================================================
        self.begin_narration("light", 9)
        self.show_caption("箭頭前進的時候，會隨著路徑平滑轉彎。")

        # 原起點與箭頭保留為淺色留底 (依教師指示：「這個點還是要在喔」)
        self.play(
            circle_arrows_init[0].animate.set_stroke(opacity=0.35),
            circle_arrows_init[1].animate.set_stroke(opacity=0.35),
            circle_arrows_init[2].animate.set_stroke(opacity=0.35),
            dots_start.animate.set_fill(opacity=0.4),
            run_time=0.4,
        )

        tracers = [m.Dot(p, radius=0.08, color=c) for p, c in zip(P_STARTS, COLORS)]
        running_circle_arrows = [
            m.Arrow(p, p + np.array([0, arrow_len, 0]), buff=0, stroke_width=4.0, color=c, max_tip_length_to_length_ratio=0.25)
            for p, c in zip(P_STARTS, COLORS)
        ]
        running_card_arrows = [
            m.Arrow(piv, piv + np.array([0, arrow_len, 0]), buff=0, stroke_width=4.0, color=c, max_tip_length_to_length_ratio=0.25)
            for piv, c in zip(PIVOTS, COLORS)
        ]
        card_turn_arcs = [
            m.Arc(radius=0.38, start_angle=np.pi / 2, angle=0.001, arc_center=piv, color=c, stroke_width=2.5)
            for piv, c in zip(PIVOTS, COLORS)
        ]

        self.add(*tracers, *running_circle_arrows, *running_card_arrows, *card_turn_arcs)

        def update_walker(i: int, alpha: float) -> None:
            r = RADII[i]
            c = COLORS[i]
            piv = PIVOTS[i]
            angle = alpha * (np.pi / 2)

            pos = O_LEFT + np.array([r * np.cos(angle), r * np.sin(angle), 0])
            tracers[i].move_to(pos)

            tangent = np.array([-np.sin(angle), np.cos(angle), 0])
            running_circle_arrows[i].become(
                m.Arrow(pos, pos + tangent * arrow_len, buff=0, stroke_width=4.0, color=c, max_tip_length_to_length_ratio=0.25)
            )
            running_card_arrows[i].become(
                m.Arrow(piv, piv + tangent * arrow_len, buff=0, stroke_width=4.0, color=c, max_tip_length_to_length_ratio=0.25)
            )
            card_turn_arcs[i].become(
                m.Arc(radius=0.38, start_angle=np.pi / 2, angle=max(0.001, angle), arc_center=piv, color=c, stroke_width=2.5)
            )

        self.play(
            m.UpdateFromAlphaFunc(tracers[0], lambda mob, u: update_walker(0, u)),
            m.UpdateFromAlphaFunc(tracers[1], lambda mob, u: update_walker(1, u)),
            m.UpdateFromAlphaFunc(tracers[2], lambda mob, u: update_walker(2, u)),
            run_time=2.4,
            rate_func=m.smooth,
        )
        self.wait(0.8)

        # =====================================================
        # 10. 步驟十：抵達終點 (向左)，比較初始與終點方向
        # =====================================================
        self.begin_narration("light", 10)
        self.show_caption("抵達九十度終點時，箭頭轉向左方。將終點方向與初始方向進行比較。")
        self.wait(1.5)

        # =====================================================
        # 11. 步驟十一：三段圓弧的箭頭偏轉角皆為 90 度
        # =====================================================
        self.begin_narration("light", 11)
        self.show_caption("可以看見：三段圓弧前進時，箭頭轉過的角度完全相同，都是九十度！")

        ra_marks_card = [
            self.make_right_angle(
                piv,
                piv + np.array([0, 1, 0]),
                piv + np.array([-1, 0, 0]),
                size=0.25,
                color=c,
                stroke_width=2.4,
            )
            for piv, c in zip(PIVOTS, COLORS)
        ]

        deg_labels_card = [
            m.Text("轉過 90°", font=CHINESE_FONT, font_size=19, weight=m.BOLD, color=c).move_to(piv + np.array([1.25, 0.45, 0]))
            for piv, c in zip(PIVOTS, COLORS)
        ]

        self.play(
            *[m.FadeOut(arc) for arc in card_turn_arcs],
            *[m.Create(ra) for ra in ra_marks_card],
            *[m.FadeIn(lbl) for lbl in deg_labels_card],
            run_time=0.8,
        )
        self.wait(1.2)

        # =====================================================
        # 12. 步驟十二：轉彎角度 ＝ 圓心角 ＝ 90°，圓弧度數相同
        # =====================================================
        self.begin_narration("light", 12)
        self.show_caption("這個轉彎的角度，正好等於所對的圓心角。因此，這三段圓弧的度數完全相同，都是九十度！")

        conclusion_text = m.Text("結論：偏轉角 ＝ 圓心角 ＝ 90°，圓弧度數皆相同！", font=CHINESE_FONT, font_size=20, weight=m.BOLD, color=C_BLUE).move_to([CARD_X, -2.4, 0])

        self.play(
            m.FadeIn(conclusion_text),
            ra_mark.animate.set_stroke(width=4.5),
            arc1.animate.set_stroke(width=8.0),
            arc2.animate.set_stroke(width=8.0),
            arc3.animate.set_stroke(width=8.0),
            run_time=1.0,
        )
        self.play(
            ra_mark.animate.set_stroke(width=2.4),
            arc1.animate.set_stroke(width=6.0),
            arc2.animate.set_stroke(width=6.0),
            arc3.animate.set_stroke(width=6.0),
            run_time=0.8,
        )
        self.wait(1.5)

        # =====================================================
        # 13. 步驟十三：非 90 度時，偏轉角依然等於圓心角（定義圓弧度數）
        # =====================================================
        self.begin_narration("light", 13)
        self.show_caption("不是九十度的時候，箭頭偏轉的角度依然等於圓心角，因此我們將圓弧的角度，定義為圓心角的度數！")

        THETA = np.pi / 3  # 60 度任意角
        v_theta = np.array([np.cos(THETA), np.sin(THETA), 0.0])
        tangent_theta = np.array([-np.sin(THETA), np.cos(THETA), 0.0])

        # 左側同心圓切出任意角 THETA (60°)
        ray_theta = m.Line(O_LEFT, O_LEFT + v_theta * axis_len, stroke_color=C_AXIS, stroke_width=2.0)
        central_arc_theta = m.Arc(radius=0.52, start_angle=0, angle=THETA, arc_center=O_LEFT, color=C_BLUE, stroke_width=2.5)
        central_label_theta = m.MathTex(r"\theta", font_size=30, color=C_BLUE).move_to(
            O_LEFT + np.array([0.78 * np.cos(THETA / 2), 0.78 * np.sin(THETA / 2), 0])
        )

        target_arc1_theta = m.Arc(radius=r1, start_angle=0, angle=THETA, arc_center=O_LEFT, color=C_ARC1, stroke_width=6.0)
        target_arc2_theta = m.Arc(radius=r2, start_angle=0, angle=THETA, arc_center=O_LEFT, color=C_ARC2, stroke_width=6.0)
        target_arc3_theta = m.Arc(radius=r3, start_angle=0, angle=THETA, arc_center=O_LEFT, color=C_ARC3, stroke_width=6.0)

        target_circle_arrows_theta = [
            m.Arrow(
                O_LEFT + r * v_theta,
                O_LEFT + r * v_theta + tangent_theta * arrow_len,
                buff=0, stroke_width=4.0, color=c, max_tip_length_to_length_ratio=0.25
            )
            for r, c in zip(RADII, COLORS)
        ]
        target_tracers_theta = [
            m.Dot(O_LEFT + r * v_theta, radius=0.08, color=c)
            for r, c in zip(RADII, COLORS)
        ]

        # 右側對比欄位：箭頭轉為 THETA 偏轉角
        target_card_arrows_theta = [
            m.Arrow(piv, piv + tangent_theta * arrow_len, buff=0, stroke_width=4.0, color=c, max_tip_length_to_length_ratio=0.25)
            for piv, c in zip(PIVOTS, COLORS)
        ]
        card_arcs_theta = [
            m.Arc(radius=0.38, start_angle=np.pi / 2, angle=THETA, arc_center=piv, color=c, stroke_width=2.5)
            for piv, c in zip(PIVOTS, COLORS)
        ]
        deg_labels_theta = [
            m.Text("偏轉角 ＝ θ", font=CHINESE_FONT, font_size=19, weight=m.BOLD, color=c).move_to(piv + np.array([1.35, 0.45, 0]))
            for piv, c in zip(PIVOTS, COLORS)
        ]

        conclusion_final = m.Text(
            "圓弧的度數 ≡ 所對圓心角的度數 (θ)",
            font=CHINESE_FONT,
            font_size=20,
            weight=m.BOLD,
            color=C_BLUE,
        ).move_to([CARD_X, -2.4, 0])

        self.play(
            m.FadeOut(dots_end),
            m.ReplacementTransform(line_v, ray_theta),
            m.ReplacementTransform(ra_mark, central_arc_theta),
            m.ReplacementTransform(deg_90_text, central_label_theta),
            m.Transform(arc1, target_arc1_theta),
            m.Transform(arc2, target_arc2_theta),
            m.Transform(arc3, target_arc3_theta),
            *[m.Transform(tr, ttr) for tr, ttr in zip(tracers, target_tracers_theta)],
            *[m.Transform(arr, tarr) for arr, tarr in zip(running_circle_arrows, target_circle_arrows_theta)],
            *[m.Transform(arr, tarr) for arr, tarr in zip(running_card_arrows, target_card_arrows_theta)],
            *[m.ReplacementTransform(ra, arc) for ra, arc in zip(ra_marks_card, card_arcs_theta)],
            *[m.ReplacementTransform(lbl, tlbl) for lbl, tlbl in zip(deg_labels_card, deg_labels_theta)],
            m.ReplacementTransform(conclusion_text, conclusion_final),
            run_time=1.8,
            rate_func=m.smooth,
        )
        self.wait(1.0)

        # 圓心角與三段圓弧呼應共振
        self.play(
            central_arc_theta.animate.set_stroke(width=4.5),
            arc1.animate.set_stroke(width=8.0),
            arc2.animate.set_stroke(width=8.0),
            arc3.animate.set_stroke(width=8.0),
            run_time=0.8,
        )
        self.play(
            central_arc_theta.animate.set_stroke(width=2.5),
            arc1.animate.set_stroke(width=6.0),
            arc2.animate.set_stroke(width=6.0),
            arc3.animate.set_stroke(width=6.0),
            run_time=0.8,
        )
        self.wait(2.2)

        self.end_narration()
        self.wait(0.5)
