"""圓弧度數的性質解說 - 9:16 直幅幾何教學動畫.

主題流程：
1. 顯示三個不同半徑的同心圓
2. 通過圓心畫兩條互相垂直的直線
3. 比較第一象限的三個 1/4 圓弧，發現弧長皆不相同，但張開的角度完全一樣
4. 標出圓心角，說明用圓心角的度數來定義圓弧的度數
5. 直幅比例 (9:16)，無語音旁白，文字排版清晰、標籤防碰撞、字體大且易讀
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import manimgx as m
import numpy as np
from manimgx_tw_helper import CHINESE_FONT, CaptionItem, TWScene

# 9:16 短影音直幅設定 (1080x1920)
m.config.pixel_width = 1080
m.config.pixel_height = 1920
m.config.frame_height = 16.0  # 對應 frame_width = 9.0


class ArcDegreeVertical(TWScene):
    def make_caption_lines(
        self,
        *lines: list[CaptionItem] | tuple[CaptionItem, ...] | CaptionItem,
        font_size: float = 30,
        math_font_size: float = 40,
        buff: float = 0.12,
        line_buff: float = 0.18,
        edge_buff: float = 0.95,
    ) -> m.VGroup:
        """建立支援多行、自動安全居中、防止超出螢幕邊界的直幅底部字幕。"""
        line_groups: list[m.VGroup] = []
        for line in lines:
            if isinstance(line, (list, tuple)):
                items = list(line)
            else:
                items = [line]
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
            grp = m.VGroup(*parts).arrange(m.RIGHT, buff=buff)
            line_groups.append(grp)
        group = m.VGroup(*line_groups).arrange(m.DOWN, buff=line_buff, aligned_edge=m.ORIGIN)
        group.to_edge(m.DOWN, buff=edge_buff)
        return group

    def construct(self) -> None:
        # =====================================================
        # 0. 配色與幾何核心參數
        # =====================================================
        C_CENTER = m.WHITE
        C_AXIS = "#64748B"          # 柔和垂直軸線
        C_RAY = "#38BDF8"           # 夾角射線亮天藍
        C_CIRC_STROKE = "#475569"   # 同心圓線條
        
        # 三個 1/4 圓弧專屬配色
        C_ARC1 = "#34D399"          # 內弧：薄荷綠
        C_ARC2 = "#FBBF24"          # 中弧：琥珀黃
        C_ARC3 = "#F87171"          # 外弧：珊瑚紅

        # 圓心與三個半徑
        O_POS = np.array([0.0, 1.4, 0.0])
        r1, r2, r3 = 1.40, 2.35, 3.30

        # =====================================================
        # 1. 片頭標題 (Opening Title)
        # =====================================================
        main_title = m.Text("圓弧的度數與性質", font=CHINESE_FONT, font_size=46, weight=m.BOLD, color=m.YELLOW)
        sub_title = m.Text("為什麼除了「長度」，還需要定義「角度」？", font=CHINESE_FONT, font_size=26, color="#94A3B8")
        title_box = m.VGroup(main_title, sub_title).arrange(m.DOWN, buff=0.35).move_to([0.0, 1.4, 0.0])

        self.play(m.FadeIn(title_box, shift=m.UP * 0.3), run_time=1.0)
        self.wait(1.8)
        self.play(m.FadeOut(title_box, shift=m.UP * 0.4), run_time=0.6)

        # 頂部固定 HUD 標題與分隔線
        hud_title = m.Text("圓弧度數的幾何定義", font=CHINESE_FONT, font_size=34, weight=m.BOLD, color=m.YELLOW)
        hud_title.move_to([0.0, 6.8, 0.0])
        hud_line = m.Line([-3.8, 6.35, 0.0], [3.8, 6.35, 0.0], stroke_color="#475569", stroke_width=1.5)
        self.play(m.FadeIn(hud_title), m.Create(hud_line), run_time=0.5)

        # =====================================================
        # 2. 步驟一：顯示三個同心圓
        # =====================================================
        cap1 = self.make_caption_lines(
            ["以同一個圓心 ", ("math", "O"), " 為基準"],
            ["畫出三個不同半徑的同心圓"]
        )
        self.set_caption(cap1)

        center_dot = m.Dot(O_POS, radius=0.09, color=C_CENTER)
        label_O = m.MathTex("O", font_size=42, color=C_CENTER).next_to(center_dot, m.DL, buff=0.18)

        circle1 = m.Circle(radius=r1, color=C_CIRC_STROKE, stroke_width=2.5).move_to(O_POS)
        circle2 = m.Circle(radius=r2, color=C_CIRC_STROKE, stroke_width=2.5).move_to(O_POS)
        circle3 = m.Circle(radius=r3, color=C_CIRC_STROKE, stroke_width=2.5).move_to(O_POS)

        self.play(m.FadeIn(center_dot), m.FadeIn(label_O), run_time=0.5)
        self.play(
            m.Create(circle1, run_time=0.8),
            m.Create(circle2, run_time=0.9),
            m.Create(circle3, run_time=1.0),
        )
        self.wait(1.5)

        # =====================================================
        # 3. 步驟二：通過圓心畫兩條垂直線
        # =====================================================
        cap2 = self.make_caption_lines(
            ["通過圓心 ", ("math", "O"), "，畫出兩條互相垂直的直線"]
        )
        self.set_caption(cap2)

        line_h = m.Line(O_POS + np.array([-3.7, 0, 0]), O_POS + np.array([3.7, 0, 0]), stroke_color=C_AXIS, stroke_width=2.0)
        line_v = m.Line(O_POS + np.array([0, -3.7, 0]), O_POS + np.array([0, 3.7, 0]), stroke_color=C_AXIS, stroke_width=2.0)

        # 直角符號 (第一象限原點處)
        ra_mark = self.make_right_angle(
            O_POS,
            O_POS + np.array([1, 0, 0]),
            O_POS + np.array([0, 1, 0]),
            size=0.32,
            color=m.YELLOW,
            stroke_width=2.2,
        )

        self.play(
            m.Create(line_h, run_time=0.8),
            m.Create(line_v, run_time=0.8),
        )
        self.play(m.Create(ra_mark), run_time=0.5)
        self.wait(1.6)

        # =====================================================
        # 4. 步驟三：比較第一象限的三個 1/4 圓弧
        # =====================================================
        cap3 = self.make_caption_lines(
            ["聚焦第一象限：兩垂直線截出三個 ", ("math", r"\frac{1}{4}"), " 圓弧"]
        )
        self.set_caption(cap3)

        # 建立三個 1/4 弧 (0 到 90 度)
        arc1 = m.Arc(radius=r1, start_angle=0, angle=np.pi / 2, arc_center=O_POS, color=C_ARC1, stroke_width=6.0)
        arc2 = m.Arc(radius=r2, start_angle=0, angle=np.pi / 2, arc_center=O_POS, color=C_ARC2, stroke_width=6.0)
        arc3 = m.Arc(radius=r3, start_angle=0, angle=np.pi / 2, arc_center=O_POS, color=C_ARC3, stroke_width=6.0)

        # 弧的端點
        p1_x = O_POS + np.array([r1, 0, 0])
        p1_y = O_POS + np.array([0, r1, 0])
        p2_x = O_POS + np.array([r2, 0, 0])
        p2_y = O_POS + np.array([0, r2, 0])
        p3_x = O_POS + np.array([r3, 0, 0])
        p3_y = O_POS + np.array([0, r3, 0])

        dot_p1 = m.Dot(p1_x, radius=0.08, color=C_ARC1)
        dot_p2 = m.Dot(p2_x, radius=0.08, color=C_ARC2)
        dot_p3 = m.Dot(p3_x, radius=0.08, color=C_ARC3)

        dot_q1 = m.Dot(p1_y, radius=0.08, color=C_ARC1)
        dot_q2 = m.Dot(p2_y, radius=0.08, color=C_ARC2)
        dot_q3 = m.Dot(p3_y, radius=0.08, color=C_ARC3)

        # 標籤 A1, A2, A3 (放置於 x 軸下方安全無交叉處，加大字體)
        lbl_A1 = m.MathTex("A_1", font_size=38, color=C_ARC1).move_to(p1_x + np.array([0.0, -0.45, 0.0]))
        lbl_A2 = m.MathTex("A_2", font_size=38, color=C_ARC2).move_to(p2_x + np.array([0.0, -0.45, 0.0]))
        lbl_A3 = m.MathTex("A_3", font_size=38, color=C_ARC3).move_to(p3_x + np.array([0.0, -0.45, 0.0]))

        # 標籤 B1, B2, B3 (放置於 y 軸左側安全無交叉處，加大字體)
        lbl_B1 = m.MathTex("B_1", font_size=38, color=C_ARC1).move_to(p1_y + np.array([-0.48, 0.0, 0.0]))
        lbl_B2 = m.MathTex("B_2", font_size=38, color=C_ARC2).move_to(p2_y + np.array([-0.48, 0.0, 0.0]))
        lbl_B3 = m.MathTex("B_3", font_size=38, color=C_ARC3).move_to(p3_y + np.array([-0.48, 0.0, 0.0]))

        # 將圓其餘非弧部分淡出收淨，視野最專注且無任何線條壓字
        self.play(
            m.FadeOut(circle1),
            m.FadeOut(circle2),
            m.FadeOut(circle3),
            m.Create(arc1, run_time=0.7),
            m.Create(arc2, run_time=0.8),
            m.Create(arc3, run_time=0.9),
            m.FadeIn(dot_p1), m.FadeIn(dot_p2), m.FadeIn(dot_p3),
            m.FadeIn(dot_q1), m.FadeIn(dot_q2), m.FadeIn(dot_q3),
            m.FadeIn(lbl_A1), m.FadeIn(lbl_A2), m.FadeIn(lbl_A3),
            m.FadeIn(lbl_B1), m.FadeIn(lbl_B2), m.FadeIn(lbl_B3),
        )
        self.wait(1.5)

        # =====================================================
        # 步驟三 (續)：比較弧長——長度皆不相同
        # =====================================================
        cap4 = self.make_caption_lines(
            ["因為三個圓的半徑不同"],
            ["這三段圓弧的「長度」明顯各不相同"]
        )
        self.set_caption(cap4)

        # 下方呈現弧長比較卡片 (y = -3.8)
        card_bg = m.RoundedRectangle(
            corner_radius=0.25, width=8.2, height=3.0,
            fill_color="#0F172A", fill_opacity=0.95,
            stroke_color="#334155", stroke_width=1.5
        ).move_to([0.0, -3.8, 0.0])

        s1_text = m.MathTex(r"\text{內弧 } \overgroup{A_1 B_1} \text{ 長度} = \frac{1}{4} \times 2\pi r_1", font_size=29, color=C_ARC1)
        s2_text = m.MathTex(r"\text{中弧 } \overgroup{A_2 B_2} \text{ 長度} = \frac{1}{4} \times 2\pi r_2", font_size=29, color=C_ARC2)
        s3_text = m.MathTex(r"\text{外弧 } \overgroup{A_3 B_3} \text{ 長度} = \frac{1}{4} \times 2\pi r_3", font_size=29, color=C_ARC3)
        ineq_text = m.MathTex(r"\text{長度比較：} \quad \overgroup{A_1 B_1} < \overgroup{A_2 B_2} < \overgroup{A_3 B_3}", font_size=30, color=m.WHITE)

        comp_group = m.VGroup(s1_text, s2_text, s3_text, ineq_text).arrange(m.DOWN, buff=0.18, aligned_edge=m.LEFT).move_to(card_bg.get_center())

        self.play(
            m.FadeIn(card_bg),
            m.FadeIn(comp_group),
            run_time=0.8
        )
        self.wait(2.5)

        # =====================================================
        # 步驟三 (核心觀察)：角度相同，需定義度數
        # =====================================================
        cap5 = self.make_caption_lines(
            ["但是從圓心觀察"],
            ["它們張開的「角度」完全一樣！"]
        )
        self.set_caption(cap5)

        # 兩條第一象限的夾角射線高亮
        ray_x = m.Arrow(O_POS, O_POS + np.array([4.0, 0, 0]), buff=0, stroke_width=3.5, color=C_RAY, max_tip_length_to_length_ratio=0.08)
        ray_y = m.Arrow(O_POS, O_POS + np.array([0, 4.0, 0]), buff=0, stroke_width=3.5, color=C_RAY, max_tip_length_to_length_ratio=0.08)

        # 扇形半透明微光，彰顯開口角度的一致性
        sector_hl = m.Sector(radius=r3, angle=np.pi / 2, start_angle=0, arc_center=O_POS, fill_color=C_RAY, fill_opacity=0.08, stroke_width=0)

        self.play(
            m.FadeIn(sector_hl),
            m.Create(ray_x),
            m.Create(ray_y),
            run_time=0.8
        )
        self.wait(2.0)

        cap6 = self.make_caption_lines(
            ["只用「長度」無法描述相同開口"],
            ["因此圓弧除了長度，我們還需要定義「角度」"]
        )
        self.set_caption(cap6)
        self.wait(2.5)

        # =====================================================
        # 5. 步驟四：標出圓心角，用圓心角定義圓弧的度數
        # =====================================================
        cap7 = self.make_caption_lines(
            ["標出圓心角：兩條半徑射線在圓心所夾的角度"]
        )
        self.set_caption(cap7)

        # 圓心角弧（半徑 0.40）與醒目標記（放置於半徑 0.85 處，位於內圓 r1=1.40 內部安全區）
        angle_arc = m.Arc(radius=0.40, start_angle=0, angle=np.pi / 2, arc_center=O_POS, color=m.YELLOW, stroke_width=3.5)
        lbl_center_deg = m.MathTex("90^\\circ", font_size=46, color=m.YELLOW).move_to(O_POS + np.array([0.62, 0.62, 0.0]))

        self.play(
            m.Create(angle_arc),
            m.FadeIn(lbl_center_deg),
            run_time=0.8
        )
        self.wait(2.0)

        # 替換卡片為度數定義
        cap8 = self.make_caption_lines(
            ["數學上定義：圓弧的「度數」"],
            ["等於它所對「圓心角的度數」"]
        )
        self.set_caption(cap8)

        def_title = m.Text("圓弧度數的定義", font=CHINESE_FONT, font_size=30, weight=m.BOLD, color=m.YELLOW)
        def_eq = m.MathTex(r"\text{圓弧的度數} \equiv \text{所對圓心角的度數}", font_size=32, color=m.WHITE)
        deg_res = m.MathTex(
            r"\overgroup{A_1 B_1} = \overgroup{A_2 B_2} = \overgroup{A_3 B_3} = 90^\circ",
            font_size=32,
            color="#38BDF8",
        )
        def_sub = m.Text("（雖然弧長不同，但三段弧的度數都是 90°）", font=CHINESE_FONT, font_size=24, color="#94A3B8")
        def_card_content = m.VGroup(def_title, def_eq, deg_res, def_sub).arrange(m.DOWN, buff=0.20, aligned_edge=m.ORIGIN).move_to(card_bg.get_center())

        self.play(
            m.FadeOut(comp_group, shift=m.DOWN * 0.1),
            m.FadeIn(def_card_content, shift=m.UP * 0.1),
            run_time=0.8
        )
        self.wait(2.5)

        # =====================================================
        # 6. 步驟五：統整總結卡片 (Summary Conclusion)
        # =====================================================
        cap9 = self.make_caption_lines(
            ["總結：弧長因半徑而異"],
            ["但圓弧度數完全由所對的圓心角決定！"]
        )
        self.set_caption(cap9)

        summary_box = m.RoundedRectangle(
            corner_radius=0.25, width=8.2, height=3.2,
            fill_color="#0F172A", fill_opacity=0.96,
            stroke_color=m.YELLOW, stroke_width=2.5,
        ).move_to([0.0, -3.8, 0.0])

        sum_title = m.Text("圓弧兩大性質總結", font=CHINESE_FONT, font_size=30, weight=m.BOLD, color=m.YELLOW)
        sum_p1 = m.VGroup(
            m.Text("1. 弧長（長度）：", font=CHINESE_FONT, font_size=26, weight=m.BOLD, color="#94A3B8"),
            m.Text("隨半徑增大而增長", font=CHINESE_FONT, font_size=26, color=m.WHITE),
        ).arrange(m.RIGHT, buff=0.12)

        sum_p2 = m.VGroup(
            m.Text("2. 度數（角度）：", font=CHINESE_FONT, font_size=26, weight=m.BOLD, color="#38BDF8"),
            m.Text("永遠等於所對圓心角", font=CHINESE_FONT, font_size=26, color=m.WHITE),
            m.MathTex(r"(90^\circ)", font_size=34, color=m.YELLOW),
        ).arrange(m.RIGHT, buff=0.12)

        sum_content = m.VGroup(sum_title, sum_p1, sum_p2).arrange(m.DOWN, buff=0.24, aligned_edge=m.LEFT).move_to(summary_box.get_center())

        self.play(
            m.ReplacementTransform(card_bg, summary_box),
            m.ReplacementTransform(def_card_content, sum_content),
            run_time=0.9
        )
        self.wait(3.5)
