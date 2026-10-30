"""任意扇形的同心弧：固定 B 展直、切向箭頭偏轉、圓心角定義。"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import manimgx as m
import numpy as np
from ArcDegree.narration_scene import NarratedScene
from manimgx_tw_helper import CHINESE_FONT

m.config.pixel_width = 1080
m.config.pixel_height = 1920
m.config.frame_height = 16.0

ORIGIN = np.array([-1.0, 1.0, 0.0])
TURN = 1.2  # Illustrative angle only; no particular degree value is displayed.
START = np.pi / 2 - TURN
RADII = (1.4, 2.35, 3.3)
COLORS = ("#34D399", "#FBBF24", "#F87171")


def direction(angle: float) -> np.ndarray:
    return np.array([np.cos(angle), np.sin(angle), 0.0])


def point(radius: float, angle: float) -> np.ndarray:
    return ORIGIN + radius * direction(angle)


def tangent_arrow(radius: float, progress: float, color: str) -> m.Arrow:
    angle = START + TURN * progress
    tail = point(radius, angle)
    return m.Arrow(tail, tail + 0.72 * direction(angle + np.pi / 2), buff=0,
                   color=color, stroke_width=4.5, max_tip_length_to_length_ratio=0.3)


def unrolled_arc(radius: float, amount: float, color: str) -> m.VMobject:
    """B stays exact; curvature decreases while r*theta remains constant."""
    b = point(radius, START + TURN)
    length = radius * TURN
    distance = np.linspace(0, length, 101)
    curvature = (1 - amount) / radius
    if curvature < 1e-7:
        points = b + np.column_stack((distance, np.zeros_like(distance), np.zeros_like(distance)))
    else:
        points = b + np.column_stack((np.sin(curvature * distance) / curvature,
                                      (np.cos(curvature * distance) - 1) / curvature,
                                      np.zeros_like(distance)))
    return m.VMobject().set_points_as_corners(points).set_stroke(color, width=6)


class ArcDegreeVerticalTurning(NarratedScene):
    timeline_root = Path(__file__).resolve().parent / "narration_turning"
    # Layout-only inspection can use previously measured narration durations.
    # Final rendering uses the revised recordings by default.
    narration_root = Path(__file__).resolve().parent / (
        "narration_f0" if os.environ.get("ARC_TURNING_LAYOUT_ONLY") == "1" else "narration_turning"
    )

    def caption(self, *lines: str) -> None:
        group = m.VGroup(*[m.Text(line, font=CHINESE_FONT, font_size=29) for line in lines])
        group.arrange(m.DOWN, buff=0.16).to_edge(m.DOWN, buff=0.92)
        self.set_caption(group)

    def construct(self) -> None:
        self.begin_narration("vertical", 1)
        title = m.VGroup(
            m.Text("圓弧的度數與性質", font=CHINESE_FONT, font_size=46, weight=m.BOLD, color=m.YELLOW),
            m.Text("從箭頭的轉彎，看見圓弧的角度", font=CHINESE_FONT, font_size=29, color="#94A3B8"),
        ).arrange(m.DOWN, buff=0.35).move_to([0, 1.4, 0])
        self.play(m.FadeIn(title), run_time=0.8)
        self.wait(1.8)
        self.play(m.FadeOut(title), run_time=0.5)
        hud = m.Text("圓弧度數的幾何定義", font=CHINESE_FONT, font_size=34, weight=m.BOLD, color=m.YELLOW).move_to([0, 6.8, 0])
        self.play(m.FadeIn(hud), m.Create(m.Line([-3.8, 6.35, 0], [3.8, 6.35, 0], color="#475569")), run_time=0.5)

        self.begin_narration("vertical", 2)
        self.caption("以同一個圓心 O 為基準", "畫出三個不同半徑的同心圓")
        dot = m.Dot(ORIGIN, radius=0.08)
        label_o = m.MathTex("O", font_size=40).next_to(dot, m.DL, buff=0.15)
        circles = [m.Circle(radius=r, color="#475569", stroke_width=2).move_to(ORIGIN) for r in RADII]
        self.play(m.FadeIn(dot), m.FadeIn(label_o), run_time=0.5)
        self.play(*[m.Create(c) for c in circles], run_time=0.9)

        self.begin_narration("vertical", 3)
        self.caption("從同一個圓心切出扇形", "觀察其中的三段同心圓弧")
        sector = m.Sector(radius=RADII[-1], start_angle=START, angle=TURN,
                          arc_center=ORIGIN, fill_color="#38BDF8", fill_opacity=0.10, stroke_width=0)
        ray_a = m.Line(ORIGIN, point(3.7, START), color="#64748B", stroke_width=2)
        ray_b = m.Line(ORIGIN, point(3.7, START + TURN), color="#64748B", stroke_width=2)
        self.play(m.FadeIn(sector), m.Create(ray_a), m.Create(ray_b), run_time=0.8)

        self.begin_narration("vertical", 4)
        self.caption("留下三段同心圓弧", "它們對應同一個扇形")
        arcs = [unrolled_arc(r, 0, c) for r, c in zip(RADII, COLORS)]
        a_dots = [m.Dot(point(r, START), radius=0.075, color=c) for r, c in zip(RADII, COLORS)]
        b_dots = [m.Dot(point(r, START + TURN), radius=0.075, color=c) for r, c in zip(RADII, COLORS)]
        a_labels = [m.MathTex(f"A_{i}", font_size=36, color=c).move_to(point(r, START) + [0.05, -0.4, 0]) for i, (r, c) in enumerate(zip(RADII, COLORS), 1)]
        b_labels = [m.MathTex(f"B_{i}", font_size=36, color=c).move_to(d.get_center() + [0.35, 0.5, 0]) for i, (d, c) in enumerate(zip(b_dots, COLORS), 1)]
        self.play(*[m.FadeOut(c) for c in circles], *[m.Create(a) for a in arcs],
                  *[m.FadeIn(obj) for obj in a_dots + b_dots + a_labels + b_labels], run_time=0.9)

        self.begin_narration("vertical", 5)
        self.caption("因為三個圓的半徑不同", "這三段圓弧的「長度」明顯各不相同")
        card = m.RoundedRectangle(width=8.1, height=3.25, corner_radius=0.25,
                                  fill_color="#0F172A", fill_opacity=0.96,
                                  stroke_color="#334155", stroke_width=1.5).move_to([0, -3.65, 0])
        comparison = m.VGroup(
            m.Text("弧長比較", font=CHINESE_FONT, font_size=30, color=m.YELLOW),
            m.MathTex(r"L_1 < L_2 < L_3", font_size=46),
            m.Text("固定 B₁、B₂、B₃，長度保持不變", font=CHINESE_FONT, font_size=26, color="#94A3B8"),
        ).arrange(m.DOWN, buff=0.25).move_to(card)
        self.play(m.FadeIn(card), m.FadeIn(comparison), m.FadeOut(sector),
                  *[m.FadeOut(x) for x in a_dots + a_labels], run_time=0.35)
        self.play(*[m.UpdateFromAlphaFunc(a, lambda mob, u, r=r, c=c: mob.become(unrolled_arc(r, u, c))) for a, r, c in zip(arcs, RADII, COLORS)], run_time=1.1)
        ends = [m.Dot(point(r, START + TURN) + [r * TURN, 0, 0], radius=0.075, color=c) for r, c in zip(RADII, COLORS)]
        self.play(*[m.FadeIn(e) for e in ends], run_time=0.2)
        self.wait(0.6)
        self.play(*[m.FadeOut(e) for e in ends], run_time=0.2)
        self.play(*[m.UpdateFromAlphaFunc(a, lambda mob, u, r=r, c=c: mob.become(unrolled_arc(r, 1-u, c))) for a, r, c in zip(arcs, RADII, COLORS)], run_time=1.1)
        self.play(*[m.FadeIn(x) for x in a_dots + a_labels], run_time=0.25)

        self.begin_narration("vertical", 6)
        self.caption("箭頭沿圓弧移動", "前進方向始終與圓弧相切")
        inset_centers = [np.array([x, -3.55, 0.0]) for x in (-2.65, 0, 2.65)]
        inset_title = m.Text("比較起點與終點的方向", font=CHINESE_FONT, font_size=28, color=m.YELLOW).move_to([0, -2.3, 0])
        references = [m.Arrow(p, p + 0.88 * direction(START + np.pi/2), buff=0, color="#64748B", stroke_width=2.5) for p in inset_centers]
        moving = [m.Arrow(p, p + 0.88 * direction(START + np.pi/2), buff=0, color=c, stroke_width=3) for p, c in zip(inset_centers, COLORS)]
        marks = [m.Arc(radius=0.48, start_angle=START+np.pi/2, angle=0.001, arc_center=p, color=c, stroke_width=3) for p, c in zip(inset_centers, COLORS)]
        results = [m.MathTex(rf"\delta_{i}", font_size=40, color=c).move_to(p + [0, -0.85, 0]) for i, (p, c) in enumerate(zip(inset_centers, COLORS), 1)]
        walkers = [tangent_arrow(r, 0, c) for r, c in zip(RADII, COLORS)]
        self.play(m.FadeOut(comparison), m.FadeIn(inset_title), m.FadeIn(references[0]),
                  m.FadeIn(moving[0]), m.FadeIn(walkers[0]), run_time=0.4)

        def walk(indices: tuple[int, ...]) -> None:
            animations: list[m.Animation] = []
            for i in indices:
                r, color, pivot = RADII[i], COLORS[i], inset_centers[i]
                animations.extend([
                    m.UpdateFromAlphaFunc(walkers[i], lambda obj, u, r=r, c=color: obj.become(tangent_arrow(r, u, c))),
                    m.UpdateFromAlphaFunc(moving[i], lambda obj, u, p=pivot, c=color: obj.become(m.Arrow(p, p+0.88*direction(START+np.pi/2+TURN*u), buff=0, color=c, stroke_width=3))),
                    m.UpdateFromAlphaFunc(marks[i], lambda obj, u, p=pivot, c=color: obj.become(m.Arc(radius=0.48, start_angle=START+np.pi/2, angle=max(0.001, TURN*u), arc_center=p, color=c, stroke_width=3))),
                ])
            self.play(*animations, run_time=1.5, rate_func=m.smooth)
            self.play(*[m.FadeIn(results[i]) for i in indices], run_time=0.25)

        walk((0,))
        self.begin_narration("vertical", 7)
        self.caption("換成另外兩段圓弧", "箭頭偏轉的角度完全相同！")
        self.play(*[m.FadeIn(obj) for i in (1, 2) for obj in (references[i], moving[i], walkers[i])], run_time=0.3)
        walk((1, 2))

        self.begin_narration("vertical", 8)
        self.caption("比較箭頭起點與終點的方向", "它們之間的夾角，就是偏轉角")
        equality = m.MathTex(r"\delta_1=\delta_2=\delta_3", font_size=40, color=m.YELLOW).move_to([0, -1.5, 0])
        self.play(m.FadeIn(equality), run_time=0.5)
        self.wait(0.6)

        self.begin_narration("vertical", 9)
        self.caption("箭頭的偏轉角 ＝ 圓心角", "用相同的角度，定義圓弧的度數")
        central = m.Arc(radius=0.58, start_angle=START, angle=TURN, arc_center=ORIGIN, color=m.YELLOW, stroke_width=3)
        theta = m.MathTex(r"\theta", font_size=48, color=m.YELLOW).move_to(ORIGIN + 0.98*direction(START+TURN/2))
        old_insets = m.VGroup(inset_title, *references, *moving, *marks, *results)
        pivot = np.array([-2.0, -3.6, 0.0])
        pair = m.VGroup(
            m.Arrow(pivot, pivot+1.0*direction(START+np.pi/2), buff=0, color="#64748B", stroke_width=3),
            m.Arrow(pivot, pivot+1.0*direction(START+TURN+np.pi/2), buff=0, color=COLORS[0], stroke_width=3),
            m.Arc(radius=0.55, start_angle=START+np.pi/2, angle=TURN, arc_center=pivot, color=m.YELLOW, stroke_width=3),
        )
        inset_caption = m.Text("兩方向一起轉，夾角保持不變", font=CHINESE_FONT, font_size=25, color="#94A3B8").move_to([0, -2.3, 0])
        relation = m.MathTex(r"\delta=\theta", font_size=44, color=m.YELLOW).move_to([1.35, -3.6, 0])
        self.play(m.FadeOut(old_insets), m.FadeIn(pair), m.FadeIn(inset_caption), m.Create(central), m.FadeIn(theta), run_time=0.5)
        self.play(m.Rotate(pair, angle=-np.pi/2, about_point=pivot), run_time=0.8)
        self.play(m.FadeIn(relation), run_time=0.4)

        self.begin_narration("vertical", 10)
        self.caption("總結：弧長因半徑而異", "圓弧度數由所對的圓心角決定！")
        summary = m.VGroup(
            m.Text("圓弧的度數", font=CHINESE_FONT, font_size=32, weight=m.BOLD, color=m.YELLOW),
            m.Text("＝ 箭頭的偏轉角 ＝ 所對圓心角", font=CHINESE_FONT, font_size=29),
            m.MathTex(r"\overgroup{A_1B_1}=\overgroup{A_2B_2}=\overgroup{A_3B_3}=\theta", font_size=34, color="#38BDF8"),
        ).arrange(m.DOWN, buff=0.25).move_to(card)
        self.play(m.FadeOut(pair), m.FadeOut(inset_caption), m.FadeOut(relation), m.FadeIn(summary), card.animate.set_stroke(m.YELLOW, width=2.5), run_time=0.7)
        self.end_narration()
        self.wait(0.35)
