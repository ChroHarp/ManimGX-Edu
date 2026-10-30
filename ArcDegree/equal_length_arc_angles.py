"""Bright vertical Edge-TTS lesson: equal lengths, curvature and central angles."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import manimgx as m
import numpy as np
from manimgx_tw_helper import CHINESE_FONT
from ArcDegree.narration_scene import NarratedScene

m.config.pixel_width = 1080
m.config.pixel_height = 1920
m.config.frame_height = 16.0
m.config.background_color = "#F7F9FC"
DARK = "#172B4D"
BLUE = "#1D4ED8"

LENGTH = 2.7
RADII = (1.15, 1.85, 2.45)
SWEEPS = tuple(LENGTH / radius for radius in RADII)
ROWS = (4.0, 0.7, -2.6)
STARTS = tuple(np.array([-1.4, y-1.1, 0.0]) for y in ROWS)
CENTERS = tuple(a + [0, r, 0] for a, r in zip(STARTS, RADII))
COLORS = ("#087F5B", "#A46300", "#C4374E")
NAMES = ("a", "b", "c")


def vector(angle: float) -> np.ndarray:
    return np.array([np.cos(angle), np.sin(angle), 0.0])


def curve(center: np.ndarray, radius: float, start: float, sweep: float, color: str) -> m.VMobject:
    angles = np.linspace(start, start+sweep, 121)
    points = center + radius*np.column_stack((np.cos(angles), np.sin(angles), np.zeros_like(angles)))
    return m.VMobject().set_points_as_corners(points).set_stroke(color, width=6)


def bend(start: np.ndarray, radius: float, amount: float, color: str) -> m.VMobject:
    s = np.linspace(0, LENGTH, 121)
    k = amount / radius
    if k < 1e-8:
        points = start + np.column_stack((s, np.zeros_like(s), np.zeros_like(s)))
    else:
        points = start + np.column_stack((np.sin(k*s)/k, (1-np.cos(k*s))/k, np.zeros_like(s)))
    return m.VMobject().set_points_as_corners(points).set_stroke(color, width=6)


def walker(index: int, progress: float) -> m.Arrow:
    angle = SWEEPS[index]*progress
    tail = CENTERS[index] + RADII[index]*vector(-np.pi/2+angle)
    return m.Arrow(tail, tail+0.62*vector(angle), color=COLORS[index], buff=0,
                   stroke_width=4, max_tip_length_to_length_ratio=0.3)


class EqualLengthArcAngles(NarratedScene):
    voice = None
    narration_root = Path(__file__).resolve().parent / "narration_edge_equal"
    timeline_root = narration_root

    def caption(self, *lines: str) -> None:
        caption = m.VGroup(*[m.Text(line, font=CHINESE_FONT, font_size=30, color=DARK) for line in lines])
        # Raise the whole caption by about three quarters of a text em.
        caption.arrange(m.DOWN, buff=0.15).to_edge(m.DOWN, buff=1.23)
        old = getattr(self, "_caption", None)
        if old is None:
            self.play(m.FadeIn(caption), run_time=0.3)
        else:
            self.play(m.FadeOut(old), m.FadeIn(caption), run_time=0.3)
        self._caption = caption

    def construct(self) -> None:
        title = m.Text("弧長相同，圓弧就相同嗎？", font=CHINESE_FONT, font_size=35,
                       weight=m.BOLD, color=DARK).move_to([0, 6.8, 0])
        rule = m.Line([-3.8, 6.35, 0], [3.8, 6.35, 0], color="#475569", stroke_width=1.5)
        self.play(m.FadeIn(title), m.Create(rule), run_time=0.5)
        panels = [m.RoundedRectangle(width=7.8, height=3.05, corner_radius=0.2,
                                      fill_color="#FFFFFF", fill_opacity=1.0,
                                      stroke_color="#D6DFEA", stroke_width=1.5).move_to([0, y, 0]) for y in ROWS]
        names = [m.MathTex(name, font_size=72, color=color).move_to([-3.2, y+0.55, 0]) for name, color, y in zip(NAMES, COLORS, ROWS)]
        arcs = [bend(a, r, 0, c).set_z_index(1) for a, r, c in zip(STARTS, RADII, COLORS)]
        equal = m.MathTex("L_a=L_b=L_c", font_size=42, color=DARK).move_to([0, -4.85, 0])

        # 1. Identical lengths and endpoint alignment establish the invariant.
        self.begin_narration("equal", 1)
        self.caption("取三條一樣長的線段 a、b、c")
        self.play(*[m.FadeIn(p) for p in panels], *[m.FadeIn(n) for n in names],
                  *[m.Create(a) for a in arcs], m.FadeIn(equal), run_time=0.9)
        self.wait(1.6)

        # 2. Bend without stretching, then rigidly align starts and tangent directions.
        self.begin_narration("equal", 2)
        self.caption("彎成不同半徑的圓弧", "長度仍然相同，形狀卻不同")
        self.play(*[m.UpdateFromAlphaFunc(a, lambda obj, u, p=p, r=r, c=c: obj.become(bend(p, r, u, c))) for a, p, r, c in zip(arcs, STARTS, RADII, COLORS)], run_time=1.3)
        self.wait(1.5)
        self.begin_narration("equal", 3)
        self.caption("把起點與前進方向對齊", "三條圓弧仍無法完全疊合")
        ghosts = [a.copy().set_stroke(opacity=0.25) for a in arcs]
        self.add(*ghosts)
        common_start = np.array([-1.6, 0.2, 0.0])
        self.play(*[a.animate.shift(common_start-p) for a, p in zip(arcs, STARTS)],
                  *[m.FadeOut(p) for p in panels], *[m.FadeOut(n) for n in names], run_time=0.8)
        self.wait(2.0)
        self.play(*[a.animate.shift(p-common_start) for a, p in zip(arcs, STARTS)],
                  *[m.FadeIn(p) for p in panels], *[m.FadeIn(n) for n in names], run_time=0.8)
        self.remove(*ghosts)

        # Each tangent-direction inset has a fixed starting direction and turning arc.
        pivots = [np.array([2.6, y-0.15, 0.0]) for y in ROWS]
        refs = [m.Arrow(p, p+[0.65, 0, 0], buff=0, color="#64748B", stroke_width=2.5) for p in pivots]
        directions = [m.Arrow(p, p+[0.65, 0, 0], buff=0, color=c, stroke_width=3) for p, c in zip(pivots, COLORS)]
        turns = [m.Arc(radius=0.4, start_angle=0, angle=0.001, arc_center=p, color=c, stroke_width=3) for p, c in zip(pivots, COLORS)]
        labels = [m.MathTex(rf"\delta_{name}", font_size=40, color=c).move_to(p+[0, 1.0, 0]) for p, name, c in zip(pivots, NAMES, COLORS)]
        arrows = [walker(i, 0) for i in range(3)]

        def travel(indices: tuple[int, ...]) -> list[m.Animation]:
            animations: list[m.Animation] = []
            for i in indices:
                pivot, sweep, color = pivots[i], SWEEPS[i], COLORS[i]
                animations.extend([
                    m.UpdateFromAlphaFunc(arrows[i], lambda obj, u, i=i: obj.become(walker(i, u))),
                    m.UpdateFromAlphaFunc(directions[i], lambda obj, u, p=pivot, t=sweep, c=color: obj.become(m.Arrow(p, p+0.65*vector(t*u), buff=0, color=c, stroke_width=3))),
                    m.UpdateFromAlphaFunc(turns[i], lambda obj, u, p=pivot, t=sweep, c=color: obj.become(m.Arc(radius=0.4, start_angle=0, angle=max(0.001, t*u), arc_center=p, color=c, stroke_width=3))),
                ])
            return animations

        # 3. First track the a arc alone, preserving its tangent at every frame.
        self.begin_narration("equal", 4)
        self.caption("箭頭從 a 的一端沿弧前進", "記錄方向總共偏轉的角度")
        self.play(m.FadeIn(arrows[0]), m.FadeIn(refs[0]), m.FadeIn(directions[0]), run_time=0.3)
        self.play(*travel((0,)), run_time=1.7, rate_func=m.smooth)
        self.play(m.FadeIn(labels[0]), run_time=0.3)
        self.wait(1.4)

        # 4. Rotating BOTH tangent directions by the same right angle preserves their angle.
        centers = [m.Dot(o, radius=0.06, color=DARK) for o in CENTERS]
        center_labels = [m.MathTex(rf"O_{name}", font_size=34, color=DARK).next_to(dot, m.LEFT, buff=0.16).shift(0.25*m.DOWN) for name, dot in zip(NAMES, centers)]
        radii = [m.VGroup(m.Line(o, p, color="#64748B", stroke_width=2),
                         m.Line(o, o+r*vector(-np.pi/2+t), color="#64748B", stroke_width=2)) for o, p, r, t in zip(CENTERS, STARTS, RADII, SWEEPS)]
        central_arcs = [m.Arc(radius=0.44, start_angle=-np.pi/2, angle=t, arc_center=o, color=c, stroke_width=3) for o, t, c in zip(CENTERS, SWEEPS, COLORS)]
        theta_labels = [m.MathTex(rf"\theta_{name}", font_size=38, color=c).move_to(o+0.76*vector(-np.pi/2+t/2)) for name, o, t, c in zip(NAMES, CENTERS, SWEEPS, COLORS)]
        relations = [m.MathTex(rf"\delta_{name}=\theta_{name}", font_size=34, color=c).move_to(p+[0, 1.0, 0]) for name, p, c in zip(NAMES, pivots, COLORS)]
        self.begin_narration("equal", 5)
        self.caption("畫出圓心與兩條半徑", "箭頭的偏轉角，就是圓心角")
        self.play(m.FadeIn(centers[0]), m.FadeIn(center_labels[0]), m.Create(radii[0]), m.Create(central_arcs[0]), m.FadeIn(theta_labels[0]), run_time=0.8)
        tangent_pair = m.VGroup(refs[0], directions[0], turns[0])
        self.play(m.Rotate(tangent_pair, angle=-np.pi/2, about_point=pivots[0]), run_time=0.7)
        self.play(m.ReplacementTransform(labels[0], relations[0]), run_time=0.35)
        self.wait(1.7)

        # 5. Repeat b and c simultaneously; equal lengths yield different turning angles.
        self.begin_narration("equal", 6)
        self.caption("在 b、c 上做相同的觀察", "弧長相同，偏轉角與圓心角卻不同")
        self.play(*[m.FadeIn(obj) for i in (1, 2) for obj in (arrows[i], refs[i], directions[i])], run_time=0.3)
        self.play(*travel((1, 2)), *[m.FadeIn(obj) for i in (1, 2) for obj in (centers[i], center_labels[i], radii[i], central_arcs[i], theta_labels[i])], run_time=1.7, rate_func=m.smooth)
        self.play(*[m.FadeIn(relations[i]) for i in (1, 2)], run_time=0.3)
        self.wait(2.1)

        # Independent conclusion after the three-arc comparison.
        self.end_narration()
        objects = panels + names + centers + center_labels + radii + central_arcs + theta_labels + arrows + refs + directions + turns + relations
        assert self._caption is not None
        self.play(*[m.FadeOut(obj) for obj in objects], *[m.FadeOut(a) for a in arcs], m.FadeOut(equal), m.FadeOut(self._caption), run_time=0.45)
        self._caption = None
        conclusion_card = m.RoundedRectangle(width=8.0, height=4.9, corner_radius=0.3,
                                              fill_color="#FFFFFF", fill_opacity=1,
                                              stroke_color=BLUE, stroke_width=2.5).move_to([0, -3.3, 0])
        conclusion_text = m.VGroup(
            m.Text("結論", font=CHINESE_FONT, font_size=44, weight=m.BOLD, color=BLUE),
            m.Text("一個圓弧除了長度以外", font=CHINESE_FONT, font_size=35, color=DARK),
            m.Text("還可以測量角度", font=CHINESE_FONT, font_size=35, color=DARK),
            m.Text("其角度就是所對的圓心角", font=CHINESE_FONT, font_size=35, color=DARK),
        ).arrange(m.DOWN, buff=0.38).move_to(conclusion_card)
        # One arc only: identical theta marks connect arc measure to its central angle.
        diagram_center = np.array([-1.2, 1.6, 0.0])
        diagram_radius, diagram_start, diagram_angle = 2.6, 0.15, 1.6
        diagram_a = diagram_center + diagram_radius*vector(diagram_start)
        diagram_b = diagram_center + diagram_radius*vector(diagram_start+diagram_angle)
        arc_theta = m.MathTex(r"\theta", font_size=48, color=COLORS[0]).move_to(
            diagram_center+(diagram_radius+0.55)*vector(diagram_start+diagram_angle/2))
        arc_label = m.Text("圓弧角度", font=CHINESE_FONT, font_size=28, color=COLORS[0]).next_to(arc_theta, m.RIGHT, buff=0.15)
        center_dot = m.Dot(diagram_center, radius=0.075, color=DARK)
        conclusion_diagram = m.VGroup(
            m.Line(diagram_center, diagram_a, color="#64748B", stroke_width=2.5),
            m.Line(diagram_center, diagram_b, color="#64748B", stroke_width=2.5),
            curve(diagram_center, diagram_radius, diagram_start, diagram_angle, COLORS[0]),
            m.Dot(diagram_a, radius=0.06, color=COLORS[0]),
            m.Dot(diagram_b, radius=0.06, color=COLORS[0]),
            center_dot,
            m.MathTex("O", font_size=42, color=DARK).next_to(center_dot, m.DL, buff=0.16),
            m.Arc(radius=0.55, start_angle=diagram_start, angle=diagram_angle, arc_center=diagram_center, color=BLUE, stroke_width=3),
            m.MathTex(r"\theta", font_size=48, color=BLUE).move_to(diagram_center+0.9*vector(diagram_start+diagram_angle/2)),
            arc_theta, arc_label,
            m.Text("圓弧角度 ＝ 圓心角", font=CHINESE_FONT, font_size=32, color=DARK).move_to([0, 0.35, 0]),
        )
        self.begin_narration("equal", 7)
        self.play(m.FadeIn(conclusion_card), m.FadeIn(conclusion_text), m.FadeIn(conclusion_diagram), run_time=0.5)
        self.wait(3.6)
        self.end_narration()
        self.play(m.FadeOut(conclusion_card), m.FadeOut(conclusion_text), m.FadeOut(conclusion_diagram), run_time=0.4)

        # 6. Move circle centers together without changing radii; only then change sweeps.
        self.begin_narration("equal", 8)
        self.caption("將三弧移到同一圓心", "各自的半徑保持不變")
        self.play(*[m.FadeIn(a) for a in arcs], run_time=0.35)
        final_center = np.array([-0.8, 1.6, 0.0])
        final_start = 0.15
        self.play(*[m.UpdateFromAlphaFunc(a, lambda obj, u, o=o, r=r, t=t, c=c: obj.become(curve((1-u)*o+u*final_center, r, (1-u)*(-np.pi/2)+u*final_start, t, c))) for a, o, r, t, c in zip(arcs, CENTERS, RADII, SWEEPS, COLORS)], run_time=1.2)
        outlines = [m.Circle(radius=r, color="#C8D2DF", stroke_width=1.5).move_to(final_center) for r in RADII]
        origin_dot = m.Dot(final_center, radius=0.075, color=DARK)
        origin_label = m.MathTex("O", font_size=40, color=DARK).next_to(origin_dot, m.DL, buff=0.16)
        initial_ray = m.Line(final_center, final_center+2.8*vector(final_start), color=BLUE, stroke_width=3)
        ending_rays = [m.Line(final_center, final_center+2.8*vector(final_start+t), color=c, stroke_width=2) for t, c in zip(SWEEPS, COLORS)]
        self.play(*[m.FadeIn(c) for c in outlines], m.FadeIn(origin_dot), m.FadeIn(origin_label), m.Create(initial_ray), *[m.Create(ray) for ray in ending_rays], run_time=0.6)
        self.wait(0.8)
        self.begin_narration("equal", 9)
        self.caption("再把張角調整成相同", "半徑不變，弧長也會跟著改變")
        target = 1.7
        self.play(*[m.UpdateFromAlphaFunc(a, lambda obj, u, r=r, t=t, c=c: obj.become(curve(final_center, r, final_start, (1-u)*t+u*target, c))) for a, r, t, c in zip(arcs, RADII, SWEEPS, COLORS)],
                  *[m.UpdateFromAlphaFunc(ray, lambda obj, u, t=t, c=c: obj.become(m.Line(final_center, final_center+2.8*vector(final_start+(1-u)*t+u*target), color=c, stroke_width=2))) for ray, t, c in zip(ending_rays, SWEEPS, COLORS)], run_time=1.4)
        final_ray = m.Line(final_center, final_center+2.8*vector(final_start+target), color=BLUE, stroke_width=3)
        angle_mark = m.Arc(radius=0.5, start_angle=final_start, angle=target, arc_center=final_center, color=BLUE, stroke_width=3)
        theta = m.MathTex(r"\theta", font_size=48, color=BLUE).move_to(final_center+0.82*vector(final_start+target/2))
        self.play(*[m.FadeOut(ray) for ray in ending_rays], m.Create(final_ray), m.Create(angle_mark), m.FadeIn(theta), run_time=0.5)
        card = m.RoundedRectangle(width=8.0, height=3.2, corner_radius=0.25, fill_color="#FFFFFF", fill_opacity=1, stroke_color=BLUE, stroke_width=2).move_to([0, -3.0, 0])
        summary = m.VGroup(
            m.Text("同一圓心角，對應相同的弧度數", font=CHINESE_FONT, font_size=28, color=BLUE),
            m.VGroup(*[m.MathTex(name, font_size=66, color=c) for name, c in zip(NAMES, COLORS)]).arrange(m.RIGHT, buff=1.1),
            m.MathTex(r"\theta_a=\theta_b=\theta_c=\theta", font_size=40, color=DARK),
            m.Text("角度相同，弧長可以不同", font=CHINESE_FONT, font_size=29, color="#526780"),
        ).arrange(m.DOWN, buff=0.27).move_to(card)
        self.begin_narration("equal", 10)
        self.caption("同心圓中，對應同一圓心角的圓弧", "角度相同，弧長隨半徑而異")
        self.play(m.FadeIn(card), m.FadeIn(summary), run_time=0.6)
        self.wait(3.0)
        self.end_narration()
        self.wait(0.3)
