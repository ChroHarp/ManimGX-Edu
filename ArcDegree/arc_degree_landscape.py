"""圓弧度數的幾何性質 - 16:9 橫幅純圖形視覺解說 (No Text, Pure Geometry).

視覺流程：
1. 三個同心圓由圓心向外展開
2. 通過圓心畫出兩條互相垂直的軸線，標示直角符號
3. 聚焦第一象限的三段 1/4 圓弧（薄荷綠、琥珀黃、珊瑚紅）
4. 圖形往左移，三段圓弧向右平滑拉直為三條平行線段（起點對齊），純視覺呈現長度明顯不同 (L1 < L2 < L3)
5. 三條線段平滑捲回為圓弧，圖形移回中央
6. 射線旋轉掃掠與同速亮點，展示三段圓弧具有完全相同張角 (90°)，扇形與同心射線彰顯角度的一致性
7. 純幾何語言，零文字說明，優雅流暢
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import manimgx as m
import numpy as np

# 16:9 橫幅標準解析度 (1920x1080)
m.config.pixel_width = 1920
m.config.pixel_height = 1080
m.config.frame_height = 8.0


class ArcDegreeLandscape(m.Scene):
    def make_right_angle(
        self,
        corner: np.ndarray,
        p1: np.ndarray,
        p2: np.ndarray,
        size: float = 0.35,
        color: m.ParsableManimColor = m.YELLOW,
        stroke_width: float = 2.5,
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

    def construct(self) -> None:
        # =====================================================
        # 0. 配色與幾何核心參數
        # =====================================================
        C_CENTER = m.WHITE
        C_AXIS = "#475569"          # 柔和灰藍垂直軸線
        C_RAY = "#38BDF8"           # 亮天藍夾角射線
        C_CIRC_STROKE = "#334155"   # 同心圓線條
        
        # 三段 1/4 圓弧專屬配色
        C_ARC1 = "#34D399"          # 內弧：薄荷綠
        C_ARC2 = "#FBBF24"          # 中弧：琥珀黃
        C_ARC3 = "#F87171"          # 外弧：珊瑚紅

        r1, r2, r3 = 1.30, 2.20, 3.10
        O_INIT = np.array([0.0, 0.0, 0.0])

        # =====================================================
        # 1. 步驟一：圓心與三個同心圓展開
        # =====================================================
        center_dot = m.Dot(O_INIT, radius=0.08, color=C_CENTER)
        circle1 = m.Circle(radius=r1, color=C_CIRC_STROKE, stroke_width=2.2).move_to(O_INIT)
        circle2 = m.Circle(radius=r2, color=C_CIRC_STROKE, stroke_width=2.2).move_to(O_INIT)
        circle3 = m.Circle(radius=r3, color=C_CIRC_STROKE, stroke_width=2.2).move_to(O_INIT)

        self.play(m.FadeIn(center_dot, scale=1.5), run_time=0.6)
        self.play(
            m.Create(circle1, run_time=0.7),
            m.Create(circle2, run_time=0.8),
            m.Create(circle3, run_time=0.9),
        )
        self.wait(0.8)

        # =====================================================
        # 2. 步驟二：通過圓心畫兩條互相垂直的線
        # =====================================================
        axis_len = 3.6
        line_h = m.Line(O_INIT + np.array([-axis_len, 0, 0]), O_INIT + np.array([axis_len, 0, 0]), stroke_color=C_AXIS, stroke_width=2.0)
        line_v = m.Line(O_INIT + np.array([0, -axis_len, 0]), O_INIT + np.array([0, axis_len, 0]), stroke_color=C_AXIS, stroke_width=2.0)

        ra_mark = self.make_right_angle(
            O_INIT,
            O_INIT + np.array([1, 0, 0]),
            O_INIT + np.array([0, 1, 0]),
            size=0.32,
            color=m.YELLOW,
            stroke_width=2.4,
        )

        self.play(
            m.Create(line_h, run_time=0.8),
            m.Create(line_v, run_time=0.8),
        )
        self.play(m.Create(ra_mark), run_time=0.5)
        self.wait(1.0)

        # =====================================================
        # 3. 步驟三：聚焦第一象限的三段 1/4 圓弧
        # =====================================================
        arc1 = m.Arc(radius=r1, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=C_ARC1, stroke_width=6.0)
        arc2 = m.Arc(radius=r2, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=C_ARC2, stroke_width=6.0)
        arc3 = m.Arc(radius=r3, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=C_ARC3, stroke_width=6.0)

        # 端點亮點
        dots_x = m.VGroup(
            m.Dot(O_INIT + np.array([r1, 0, 0]), radius=0.07, color=C_ARC1),
            m.Dot(O_INIT + np.array([r2, 0, 0]), radius=0.07, color=C_ARC2),
            m.Dot(O_INIT + np.array([r3, 0, 0]), radius=0.07, color=C_ARC3),
        )
        dots_y = m.VGroup(
            m.Dot(O_INIT + np.array([0, r1, 0]), radius=0.07, color=C_ARC1),
            m.Dot(O_INIT + np.array([0, r2, 0]), radius=0.07, color=C_ARC2),
            m.Dot(O_INIT + np.array([0, r3, 0]), radius=0.07, color=C_ARC3),
        )

        # 淡化其餘非弧部分，突顯三段圓弧
        self.play(
            circle1.animate.set_stroke(opacity=0.15),
            circle2.animate.set_stroke(opacity=0.15),
            circle3.animate.set_stroke(opacity=0.15),
            m.Create(arc1, run_time=0.7),
            m.Create(arc2, run_time=0.8),
            m.Create(arc3, run_time=0.9),
            m.FadeIn(dots_x),
            m.FadeIn(dots_y),
        )
        self.wait(1.0)

        # =====================================================
        # 4. 步驟四：圖形平移向左，三段圓弧向右拉直為線段比較長度
        # =====================================================
        SHIFT_VEC = np.array([-2.7, 0.0, 0.0])
        O_LEFT = O_INIT + SHIFT_VEC

        left_assembly = m.VGroup(
            center_dot, circle1, circle2, circle3,
            line_h, line_v, ra_mark,
            arc1, arc2, arc3, dots_x, dots_y,
        )

        self.play(
            left_assembly.animate.shift(SHIFT_VEC),
            run_time=1.0,
        )
        self.wait(0.5)

        # 原地保留淡色幽靈弧（Ghost Arcs），方便對比拉直過程
        ghost_arc1 = arc1.copy().set_stroke(opacity=0.25, width=3.0)
        ghost_arc2 = arc2.copy().set_stroke(opacity=0.25, width=3.0)
        ghost_arc3 = arc3.copy().set_stroke(opacity=0.25, width=3.0)
        self.add(ghost_arc1, ghost_arc2, ghost_arc3)

        # 右側直線段目標位置與長度 (L = r * pi / 2)
        X_START = 1.0
        L1 = r1 * np.pi / 2  # ~ 2.04
        L2 = r2 * np.pi / 2  # ~ 3.46
        L3 = r3 * np.pi / 2  # ~ 4.87

        Y_POS1 = -1.3
        Y_POS2 = 0.0
        Y_POS3 = 1.3

        line_seg1 = m.Line([X_START, Y_POS1, 0], [X_START + L1, Y_POS1, 0], stroke_color=C_ARC1, stroke_width=6.0)
        line_seg2 = m.Line([X_START, Y_POS2, 0], [X_START + L2, Y_POS2, 0], stroke_color=C_ARC2, stroke_width=6.0)
        line_seg3 = m.Line([X_START, Y_POS3, 0], [X_START + L3, Y_POS3, 0], stroke_color=C_ARC3, stroke_width=6.0)

        # 左側起點對齊虛線
        align_baseline = m.DashedLine([X_START, -2.1, 0], [X_START, 2.1, 0], stroke_color="#64748B", stroke_width=1.8, dash_length=0.12)
        
        # 右側三線段末端指示虛線
        end_dot1 = m.Dot([X_START + L1, Y_POS1, 0], radius=0.07, color=C_ARC1)
        end_dot2 = m.Dot([X_START + L2, Y_POS2, 0], radius=0.07, color=C_ARC2)
        end_dot3 = m.Dot([X_START + L3, Y_POS3, 0], radius=0.07, color=C_ARC3)

        # 平滑拉直動畫：弧變直線！
        self.play(
            m.FadeIn(align_baseline),
            m.Transform(arc1, line_seg1),
            m.Transform(arc2, line_seg2),
            m.Transform(arc3, line_seg3),
            run_time=1.5,
        )
        self.play(
            m.FadeIn(end_dot1),
            m.FadeIn(end_dot2),
            m.FadeIn(end_dot3),
            run_time=0.4,
        )
        self.wait(1.5)

        # 純圖形長度對比提示：三個端點依次亮起
        self.play(
            m.Flash(end_dot1, color=C_ARC1, flash_radius=0.3, num_lines=8),
            m.Flash(end_dot2, color=C_ARC2, flash_radius=0.3, num_lines=8),
            m.Flash(end_dot3, color=C_ARC3, flash_radius=0.3, num_lines=8),
            run_time=0.8,
        )
        self.wait(1.2)

        # 線段平滑捲回為同心圓上的圓弧！
        target_arc1 = m.Arc(radius=r1, start_angle=0, angle=np.pi / 2, arc_center=O_LEFT, color=C_ARC1, stroke_width=6.0)
        target_arc2 = m.Arc(radius=r2, start_angle=0, angle=np.pi / 2, arc_center=O_LEFT, color=C_ARC2, stroke_width=6.0)
        target_arc3 = m.Arc(radius=r3, start_angle=0, angle=np.pi / 2, arc_center=O_LEFT, color=C_ARC3, stroke_width=6.0)

        self.play(
            m.FadeOut(end_dot1), m.FadeOut(end_dot2), m.FadeOut(end_dot3),
            m.FadeOut(align_baseline),
            m.Transform(arc1, target_arc1),
            m.Transform(arc2, target_arc2),
            m.Transform(arc3, target_arc3),
            run_time=1.5,
        )
        self.remove(ghost_arc1, ghost_arc2, ghost_arc3)
        self.wait(0.6)

        # =====================================================
        # 5. 步驟五：移回中央，聚焦「開口角度完全一致」
        # =====================================================
        self.play(
            left_assembly.animate.shift(-SHIFT_VEC),
            run_time=1.0,
        )
        self.wait(0.5)

        # 兩條第一象限的夾角射線高亮
        ray_x = m.Arrow(O_INIT, O_INIT + np.array([axis_len + 0.3, 0, 0]), buff=0, stroke_width=3.5, color=C_RAY, max_tip_length_to_length_ratio=0.08)
        ray_y = m.Arrow(O_INIT, O_INIT + np.array([0, axis_len + 0.3, 0]), buff=0, stroke_width=3.5, color=C_RAY, max_tip_length_to_length_ratio=0.08)

        # 圓心角弧符號 (半徑 0.55)
        central_angle_arc = m.Arc(radius=0.55, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=m.YELLOW, stroke_width=3.5)

        self.play(
            m.Create(ray_x),
            m.Create(ray_y),
            m.Create(central_angle_arc),
            run_time=0.8,
        )
        self.wait(0.8)

        # 旋轉掃掠射線與三個同速亮點：展現角度同步
        sweep_ray = m.Line(O_INIT, O_INIT + np.array([axis_len + 0.2, 0, 0]), stroke_color=m.YELLOW, stroke_width=3.0)
        tracer1 = m.Dot(O_INIT + np.array([r1, 0, 0]), radius=0.09, color=m.WHITE)
        tracer2 = m.Dot(O_INIT + np.array([r2, 0, 0]), radius=0.09, color=m.WHITE)
        tracer3 = m.Dot(O_INIT + np.array([r3, 0, 0]), radius=0.09, color=m.WHITE)

        sweep_sector = m.Sector(radius=r3, angle=0.001, start_angle=0, arc_center=O_INIT, fill_color=C_RAY, fill_opacity=0.12, stroke_width=0)

        self.play(
            m.FadeIn(sweep_ray),
            m.FadeIn(tracer1), m.FadeIn(tracer2), m.FadeIn(tracer3),
            run_time=0.4,
        )

        # 旋轉 90 度：同角度掃描
        # 建立滿版 90 度扇形並平滑填充
        full_sector = m.Sector(radius=r3, angle=np.pi / 2, start_angle=0, arc_center=O_INIT, fill_color=C_RAY, fill_opacity=0.15, stroke_width=0)

        self.play(
            m.Rotate(sweep_ray, angle=np.pi / 2, about_point=O_INIT),
            m.Rotate(tracer1, angle=np.pi / 2, about_point=O_INIT),
            m.Rotate(tracer2, angle=np.pi / 2, about_point=O_INIT),
            m.Rotate(tracer3, angle=np.pi / 2, about_point=O_INIT),
            m.Create(full_sector),
            run_time=2.0,
            rate_func=m.smooth,
        )
        self.play(
            m.FadeOut(sweep_ray),
            m.FadeOut(tracer1), m.FadeOut(tracer2), m.FadeOut(tracer3),
            run_time=0.4,
        )
        self.wait(0.8)

        # =====================================================
        # 6. 步驟六：圓心角波紋輻射向外，連結圓心角與圓弧度數
        # =====================================================
        # 從圓心角弧複製擴散至各弧
        ripple1 = m.Arc(radius=r1, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=m.YELLOW, stroke_width=3.5)
        ripple2 = m.Arc(radius=r2, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=m.YELLOW, stroke_width=3.5)
        ripple3 = m.Arc(radius=r3, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=m.YELLOW, stroke_width=3.5)

        # 放射線段輔助視覺 (例如 30 度、60 度分角線)
        rad_line_30 = m.DashedLine(O_INIT, O_INIT + np.array([axis_len * np.cos(np.pi / 6), axis_len * np.sin(np.pi / 6), 0]), stroke_color="#94A3B8", stroke_width=1.5, dash_length=0.1)
        rad_line_60 = m.DashedLine(O_INIT, O_INIT + np.array([axis_len * np.cos(np.pi / 3), axis_len * np.sin(np.pi / 3), 0]), stroke_color="#94A3B8", stroke_width=1.5, dash_length=0.1)

        self.play(
            m.Create(rad_line_30),
            m.Create(rad_line_60),
            run_time=0.8,
        )
        self.wait(0.5)

        # 圓心角黃金光芒向外波動抵達三段圓弧
        self.play(
            m.TransformFromCopy(central_angle_arc, ripple1),
            run_time=0.6,
        )
        self.play(
            m.TransformFromCopy(ripple1, ripple2),
            run_time=0.6,
        )
        self.play(
            m.TransformFromCopy(ripple2, ripple3),
            run_time=0.6,
        )
        self.wait(1.0)

        # 最終三段圓弧高亮呼吸燈效果收尾
        self.play(
            arc1.animate.set_stroke(width=9.0),
            arc2.animate.set_stroke(width=9.0),
            arc3.animate.set_stroke(width=9.0),
            ra_mark.animate.set_stroke(width=4.0),
            run_time=0.8,
        )
        self.play(
            arc1.animate.set_stroke(width=6.0),
            arc2.animate.set_stroke(width=6.0),
            arc3.animate.set_stroke(width=6.0),
            ra_mark.animate.set_stroke(width=2.4),
            m.FadeOut(ripple1), m.FadeOut(ripple2), m.FadeOut(ripple3),
            run_time=0.8,
        )
        self.wait(2.5)
