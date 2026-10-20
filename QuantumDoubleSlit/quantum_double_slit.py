"""量子雙狹縫實驗與波粒二象性（曉臻知性配音自動同步版）

配音設定：
- 語音角色：台灣女聲 曉臻 (zh-TW-HsiaoChenNeural)
- 沉穩知性款：pitch: -15Hz, rate: +5%
- 聽感：降調後保留咬字溫和度，散發沉著內斂的講課質感，聽感極為舒適耐聽。
- 整合 self.say() 自動同步，完全淘汰手動硬編碼秒數與外掛音軌。
"""

from __future__ import annotations

import os
import sys

# 確保可匯入專案根目錄之 manimgx_tw_helper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import manimgx as m
import numpy as np
from manimgx_tw_helper import HsiaoChenVoice

CHINESE_FONT = "GenSekiGothic TW"
CYAN_COLOR = "#00E5FF"


class QuantumDoubleSlitScene(m.Scene):
    """量子雙狹縫實驗：波粒二象性與觀測者效應精緻視覺解析（曉臻知性配音版）。"""

    voice = HsiaoChenVoice()

    def construct(self) -> None:
        np.random.seed(42)

        # =====================================================================
        # 0. 序幕：標題與歷史導引
        # =====================================================================
        title = m.Text("量子雙狹縫實驗", font=CHINESE_FONT, font_size=38, color=m.YELLOW)
        subtitle = m.Text(
            "波粒二象性與觀測者效應之謎", font=CHINESE_FONT, font_size=24, color=m.BLUE_B
        )
        title_group = m.VGroup(title, subtitle).arrange(m.DOWN, buff=0.25).move_to(m.UP * 0.5)

        self.play(m.FadeIn(title_group, shift=m.UP * 0.3), run_time=1.0)
        self.wait(0.4)

        quote_feynman = m.VGroup(
            m.Text("「它包含了量子力學的心臟。」", font=CHINESE_FONT, font_size=22, color=m.WHITE),
            m.Text(
                "「在真實世界中，它包含了唯一的奧秘。」",
                font=CHINESE_FONT,
                font_size=22,
                color=m.WHITE,
            ),
            m.Text(
                "— 理查·費曼 (Richard Feynman), 1965",
                font=CHINESE_FONT,
                font_size=18,
                color=m.YELLOW_B,
            ),
        ).arrange(m.DOWN, buff=0.15).next_to(title_group, m.DOWN, buff=0.5)

        quote_box = m.SurroundingRectangle(
            quote_feynman,
            buff=0.25,
            color=m.GREY_C,
            stroke_width=1.5,
            fill_color=m.BLACK,
            fill_opacity=0.6,
        )

        self.say(
            "如果量子力學有一個心臟，那一定是雙狹縫實驗。正如費曼所說，這裡包含了微觀世界唯一的奧秘。",
            m.FadeIn(quote_box),
            m.FadeIn(quote_feynman),
        )
        self.wait(0.6)

        self.play(
            m.FadeOut(title_group, shift=m.UP * 0.4),
            m.FadeOut(quote_box),
            m.FadeOut(quote_feynman, shift=m.UP * 0.2),
            run_time=0.7,
        )

        # =====================================================================
        # 1. 搭建實驗環境
        # =====================================================================
        # 頂部狀態列 HUD
        hud_bar = m.Rectangle(
            width=13.0,
            height=0.65,
            fill_color=m.DARK_GREY,
            fill_opacity=0.8,
            stroke_color=m.GREY_E,
            stroke_width=1.0,
        ).to_edge(m.UP, buff=0.25)

        hud_title = m.Text(
            "雙狹縫實驗裝置", font=CHINESE_FONT, font_size=20, color=m.YELLOW
        ).move_to(hud_bar.get_left() + np.array([1.5, 0, 0]))

        hud_status = m.Text(
            "階段一：經典粒子彈幕對比", font=CHINESE_FONT, font_size=18, color=m.GREEN_B
        ).move_to(hud_bar.get_right() - np.array([2.3, 0, 0]))

        hud_group = m.VGroup(hud_bar, hud_title, hud_status)

        # 發射源（左側 x = -5.0）
        gun_x = -5.0
        gun_body = m.Rectangle(
            width=0.9, height=0.9, fill_color=m.GREY_D, fill_opacity=0.95, stroke_color=m.WHITE, stroke_width=1.5
        ).move_to(np.array([gun_x, 0, 0]))
        gun_barrel = m.Rectangle(
            width=0.45, height=0.35, fill_color=m.GREY_C, fill_opacity=0.95, stroke_color=m.WHITE, stroke_width=1.5
        ).next_to(gun_body, m.RIGHT, buff=0.0)
        gun_label = m.Text("彈珠發射器", font=CHINESE_FONT, font_size=15, color=m.WHITE).next_to(
            gun_body, m.DOWN, buff=0.2
        )
        gun_group = m.VGroup(gun_body, gun_barrel, gun_label)

        # 雙狹縫屏障（x = -0.6）
        barrier_x = -0.6
        slit_y = 0.75
        slit_w = 0.45

        top_barrier = m.Rectangle(
            width=0.22, height=1.5, fill_color=m.GREY_B, fill_opacity=0.95, stroke_color=m.WHITE, stroke_width=1.5
        ).move_to(np.array([barrier_x, slit_y + slit_w / 2 + 0.75, 0]))

        mid_barrier = m.Rectangle(
            width=0.22, height=1.05, fill_color=m.GREY_B, fill_opacity=0.95, stroke_color=m.WHITE, stroke_width=1.5
        ).move_to(np.array([barrier_x, 0, 0]))

        bot_barrier = m.Rectangle(
            width=0.22, height=1.5, fill_color=m.GREY_B, fill_opacity=0.95, stroke_color=m.WHITE, stroke_width=1.5
        ).move_to(np.array([barrier_x, -slit_y - slit_w / 2 - 0.75, 0]))

        slit_a_label = m.Text("狹縫 A", font=CHINESE_FONT, font_size=13, color=m.YELLOW).next_to(
            np.array([barrier_x, slit_y, 0]), m.LEFT, buff=0.25
        )
        slit_b_label = m.Text("狹縫 B", font=CHINESE_FONT, font_size=13, color=m.YELLOW).next_to(
            np.array([barrier_x, -slit_y, 0]), m.LEFT, buff=0.25
        )
        barrier_walls = m.VGroup(top_barrier, mid_barrier, bot_barrier)
        slit_labels = m.VGroup(slit_a_label, slit_b_label)
        barrier_group = m.VGroup(barrier_walls, slit_labels)

        # 接收螢幕（x = 2.7）
        screen_x = 2.7
        screen_plate = m.Rectangle(
            width=0.2, height=4.4, fill_color=m.GREY_B, fill_opacity=0.85, stroke_color=m.WHITE, stroke_width=1.5
        ).move_to(np.array([screen_x, 0, 0]))
        screen_label = m.Text("感光接收屏", font=CHINESE_FONT, font_size=15, color=m.WHITE).move_to(
            np.array([screen_x + 1.0, 2.55, 0])
        )
        screen_group = m.VGroup(screen_plate, screen_label)

        # 底部字幕框 HUD
        caption_box = m.Rectangle(
            width=13.0,
            height=0.9,
            fill_color=m.BLACK,
            fill_opacity=0.85,
            stroke_color=m.GREY_D,
            stroke_width=1.0,
        ).to_edge(m.DOWN, buff=0.25)

        cap_text1 = m.Text(
            "【經典彈幕】宏觀彈珠均勻掃射，穿過狹縫的粒子在接收屏形成兩條清晰的直線！",
            font=CHINESE_FONT,
            font_size=18,
            color=m.WHITE,
        ).move_to(caption_box.get_center())

        self.say(
            "我們先從宏觀經典世界看起。當彈珠均勻掃射時，只有穿過兩道狹縫的彈珠能抵達屏幕，留下經典的雙線條紋。",
            m.FadeIn(hud_group),
            m.FadeIn(gun_group),
            m.FadeIn(barrier_group),
            m.FadeIn(screen_group),
            m.FadeIn(caption_box),
            m.FadeIn(cap_text1),
        )

        # =====================================================================
        # 1.1 經典粒子均勻掃射彈幕 (Evenly swept barrage with wall bounces)
        # =====================================================================
        screen_hits_classical = m.VGroup()
        fire_anims = []

        num_balls = 42
        sweep_targets_y = np.linspace(-2.1, 2.1, num_balls)
        np.random.seed(42)
        perm = np.random.permutation(num_balls)

        for idx in perm:
            target_y = float(sweep_targets_y[idx])
            ball = m.Dot(point=[gun_x + 0.7, 0, 0], radius=0.065, color=m.YELLOW)

            passed_slit_a = abs(target_y - slit_y) <= (slit_w / 2)
            passed_slit_b = abs(target_y - (-slit_y)) <= (slit_w / 2)

            if passed_slit_a or passed_slit_b:
                s_y = slit_y if passed_slit_a else -slit_y
                end_y = float(np.clip(s_y + np.random.normal(0, 0.18), -2.0, 2.0))
                p_slit = np.array([barrier_x, target_y, 0])
                p_screen = np.array([screen_x - 0.12, end_y, 0])

                hit = m.Dot(point=p_screen, radius=0.05, color=m.YELLOW_B)
                screen_hits_classical.add(hit)

                anim = m.Succession(
                    m.FadeIn(ball, run_time=0.04),
                    ball.animate(run_time=0.28, rate_func=m.linear).move_to(p_slit),
                    ball.animate(run_time=0.30, rate_func=m.linear).move_to(p_screen),
                    m.FadeOut(ball, run_time=0.04),
                )
            else:
                p_wall = np.array([barrier_x - 0.11, target_y, 0])
                p_bounce = np.array([barrier_x - 0.75, target_y * 1.15, 0])

                anim = m.Succession(
                    m.FadeIn(ball, run_time=0.04),
                    ball.animate(run_time=0.28, rate_func=m.linear).move_to(p_wall),
                    ball.animate(run_time=0.18, rate_func=m.linear).move_to(p_bounce).set_opacity(0.0),
                    m.FadeOut(ball, run_time=0.04),
                )
            fire_anims.append(anim)

        self.play(
            m.AnimationGroup(*fire_anims, lag_ratio=0.045),
            m.FadeIn(screen_hits_classical, lag_ratio=0.06),
            run_time=2.8,
        )

        # 雙峰經典強度曲線
        curve_two_stripes = m.VMobject(stroke_color=m.YELLOW, stroke_width=2.5)
        ys = np.linspace(-2.1, 2.1, 100)
        c_pts = []
        for y in ys:
            intensity = 0.8 * (
                np.exp(-((y - slit_y) ** 2) / 0.15)
                + np.exp(-((y + slit_y) ** 2) / 0.15)
            )
            c_pts.append(np.array([screen_x + 0.2 + intensity * 1.3, y, 0]))
        curve_two_stripes.set_points_smoothly(c_pts)

        two_peak_label = m.Text(
            "經典雙峰分佈", font=CHINESE_FONT, font_size=14, color=m.YELLOW
        ).next_to(curve_two_stripes, m.RIGHT, buff=0.10)

        self.say(
            "沒對準狹縫的彈珠撞牆反彈，對準的穿過狹縫，在後方統計出直觀的雙峰分佈。",
            m.Create(curve_two_stripes),
            m.FadeIn(two_peak_label),
        )
        self.wait(0.5)

        self.play(
            m.FadeOut(screen_hits_classical),
            m.FadeOut(curve_two_stripes),
            m.FadeOut(two_peak_label),
            m.FadeOut(slit_labels),
            run_time=0.6,
        )

        # =====================================================================
        # 2. 0:16 托馬斯·楊光波干涉（半圓形同心波前擴散，鮮明相長相消干涉）
        # =====================================================================
        new_hud_status1 = m.Text(
            "歷史：1801 托馬斯·楊 光波干涉",
            font=CHINESE_FONT,
            font_size=18,
            color=m.BLUE_B,
        ).move_to(hud_bar.get_right() - np.array([2.2, 0, 0]))

        cap_text2 = m.Text(
            "【1801 年｜光波干涉】光源發射同心波前，經雙狹縫分開後產生大面積半圓干涉！",
            font=CHINESE_FONT,
            font_size=17,
            color=m.WHITE,
        ).move_to(caption_box.get_center())

        laser_tube = m.Rectangle(
            width=1.1, height=0.6, fill_color=m.TEAL_E, fill_opacity=0.95, stroke_color=CYAN_COLOR, stroke_width=2.0
        ).move_to(np.array([gun_x, 0, 0]))
        laser_lens = m.Arc(
            radius=0.3, start_angle=-m.PI / 2, angle=m.PI, stroke_color=CYAN_COLOR, stroke_width=2.5
        ).move_to(laser_tube.get_right())
        laser_label = m.Text("同調光源", font=CHINESE_FONT, font_size=15, color=CYAN_COLOR).next_to(
            laser_tube, m.DOWN, buff=0.2
        )
        laser_source_group = m.VGroup(laser_tube, laser_lens, laser_label)

        self.say(
            "然而在一八零一年，托馬斯·楊用光波進行了相同的實驗，結果卻完全不同。",
            m.Transform(hud_status, new_hud_status1),
            m.ReplacementTransform(cap_text1, cap_text2),
            m.ReplacementTransform(gun_group, laser_source_group),
        )

        # 發射源向狹縫傳播的同心圓波前
        pre_semicircles = m.VGroup()
        for r_pre in np.linspace(0.6, 3.8, 6):
            semi_pre = m.Arc(
                radius=r_pre,
                start_angle=-m.PI / 3.8,
                angle=2 * m.PI / 3.8,
                arc_center=[gun_x + 0.55, 0, 0],
                stroke_color=CYAN_COLOR,
                stroke_width=2.4,
                stroke_opacity=max(0.25, 0.9 - r_pre / 4.6),
            )
            pre_semicircles.add(semi_pre)

        self.play(
            m.FadeIn(pre_semicircles, lag_ratio=0.15, rate_func=m.linear),
            run_time=1.4,
        )

        # 狹縫後方：產生兩列完整的「大面積半圓次級波」
        post_semicircles_a = m.VGroup()
        post_semicircles_b = m.VGroup()
        semi_radii = np.linspace(0.35, 2.3, 7)
        for r in semi_radii:
            arc_a = m.Arc(
                radius=r,
                start_angle=-m.PI / 2.1,
                angle=2 * m.PI / 2.1,
                arc_center=[barrier_x, slit_y, 0],
                stroke_color=CYAN_COLOR,
                stroke_width=2.5,
                stroke_opacity=max(0.35, 1.0 - r / 2.8),
            )
            arc_b = m.Arc(
                radius=r,
                start_angle=-m.PI / 2.1,
                angle=2 * m.PI / 2.1,
                arc_center=[barrier_x, -slit_y, 0],
                stroke_color=CYAN_COLOR,
                stroke_width=2.5,
                stroke_opacity=max(0.35, 1.0 - r / 2.8),
            )
            post_semicircles_a.add(arc_a)
            post_semicircles_b.add(arc_b)

        cap_text2b = m.Text(
            "雙狹縫分開為兩個次級波源，兩組同心半圓波互相重疊，產生清晰的明暗干涉！",
            font=CHINESE_FONT,
            font_size=17,
            color=m.YELLOW,
        ).move_to(caption_box.get_center())

        self.say(
            "雙狹縫化身為兩個次級波源，向外擴散的半圓波相互交疊，波峰與波谷相長相消，形成了明暗相間的干涉條紋。",
            m.ReplacementTransform(cap_text2, cap_text2b),
            m.FadeIn(post_semicircles_a, lag_ratio=0.12),
            m.FadeIn(post_semicircles_b, lag_ratio=0.12),
        )

        # 接收屏上的波動干涉曲線
        curve_interference = m.VMobject(stroke_color=CYAN_COLOR, stroke_width=2.8)
        ys_inf = np.linspace(-2.1, 2.1, 160)
        inf_pts = []
        for y in ys_inf:
            intensity = (np.cos(3.8 * y) ** 2) * np.exp(-(y**2) / 2.2)
            inf_pts.append(np.array([screen_x + 0.2 + intensity * 1.3, y, 0]))
        curve_interference.set_points_smoothly(inf_pts)

        inf_label = m.Text(
            "明暗相間干涉圖樣", font=CHINESE_FONT, font_size=14, color=CYAN_COLOR
        ).next_to(curve_interference, m.RIGHT, buff=0.10)

        self.play(
            m.Create(curve_interference),
            m.FadeIn(inf_label),
            run_time=1.0,
        )
        self.wait(1.0)

        self.play(
            m.FadeOut(pre_semicircles),
            m.FadeOut(post_semicircles_a),
            m.FadeOut(post_semicircles_b),
            m.FadeOut(curve_interference),
            m.FadeOut(inf_label),
            run_time=0.8,
        )

        # =====================================================================
        # 3. 0:25 電子束：均勻分佈發射，到狹縫前淡化消失，感光屏顯現干涉圖樣
        # =====================================================================
        electron_gun_body = m.Rectangle(
            width=0.9, height=0.7, fill_color=m.BLUE_E, fill_opacity=0.95, stroke_color=m.TEAL_B, stroke_width=1.5
        ).move_to(np.array([gun_x, 0, 0]))
        electron_gun_nozzle = m.Polygon(
            [gun_x + 0.45, 0.18, 0],
            [gun_x + 0.75, 0.08, 0],
            [gun_x + 0.75, -0.08, 0],
            [gun_x + 0.45, -0.18, 0],
            fill_color=m.BLUE_D,
            fill_opacity=0.95,
            stroke_color=m.TEAL_B,
            stroke_width=1.5,
        )
        electron_gun_label = m.Text("電子槍", font=CHINESE_FONT, font_size=15, color=m.TEAL_A).next_to(
            electron_gun_body, m.DOWN, buff=0.2
        )
        electron_gun_group = m.VGroup(electron_gun_body, electron_gun_nozzle, electron_gun_label)

        new_hud_status2a = m.Text(
            "實驗：發射大量電子束",
            font=CHINESE_FONT,
            font_size=18,
            color=m.TEAL_A,
        ).move_to(hud_bar.get_right() - np.array([2.1, 0, 0]))

        cap_text3a = m.Text(
            "【步驟一：發射電子束】電子束呈均勻分佈射向雙狹縫，到狹縫前淡化消失，感光屏竟出現干涉圖樣！",
            font=CHINESE_FONT,
            font_size=16,
            color=m.WHITE,
        ).move_to(caption_box.get_center())

        self.say(
            "那麼，如果我們換成具有質量的實體粒子，例如電子，又會發生什麼呢？",
            m.Transform(hud_status, new_hud_status2a),
            m.ReplacementTransform(cap_text2b, cap_text3a),
            m.ReplacementTransform(laser_source_group, electron_gun_group),
        )

        expected_curve = curve_two_stripes.copy().set_stroke(color=m.GREY_A, width=1.8)

        legend_expected = m.VGroup(
            m.Line([0, 0, 0], [0.35, 0, 0], stroke_color=m.GREY_A, stroke_width=2.2),
            m.Text("預期：雙峰條紋", font=CHINESE_FONT, font_size=13, color=m.GREY_A),
        ).arrange(m.RIGHT, buff=0.10)

        legend_actual = m.VGroup(
            m.Line([0, 0, 0], [0.35, 0, 0], stroke_color=m.TEAL_A, stroke_width=2.5),
            m.Text("實際：干涉圖樣", font=CHINESE_FONT, font_size=13, color=m.TEAL_A),
        ).arrange(m.RIGHT, buff=0.10)

        curve_legend = m.VGroup(legend_expected, legend_actual).arrange(
            m.DOWN, buff=0.22, aligned_edge=m.LEFT
        ).move_to(np.array([screen_x + 2.6, 0.0, 0]))

        self.play(m.FadeIn(expected_curve), m.FadeIn(legend_expected), run_time=0.6)

        # 動態展示：電子束與 0:06 一樣全角度均勻角向掃射，但所有電子在狹縫前淡化消失
        beam_fire_anims = []
        beam_screen_hits = m.VGroup()
        num_beam_electrons = 42
        sweep_beam_targets_y = np.linspace(-2.1, 2.1, num_beam_electrons)
        np.random.seed(101)
        perm_beam = np.random.permutation(num_beam_electrons)

        for idx in perm_beam:
            target_y = float(sweep_beam_targets_y[idx])
            e_dot = m.Dot(point=[gun_x + 0.75, 0, 0], radius=0.06, color=m.TEAL_A)
            p_fade = np.array([barrier_x - 0.45, target_y * 0.75, 0])

            while True:
                cand_y = float(np.random.uniform(-2.0, 2.0))
                prob = float((np.cos(3.8 * cand_y) ** 2) * np.exp(-(cand_y**2) / 2.2))
                if np.random.rand() < prob:
                    end_y = cand_y
                    break
            p_screen = np.array([screen_x - 0.12, end_y, 0])
            hit_d = m.Dot(point=p_screen, radius=0.045, color=m.TEAL_A)
            beam_screen_hits.add(hit_d)

            anim = m.Succession(
                m.FadeIn(e_dot, run_time=0.04),
                e_dot.animate(run_time=0.35, rate_func=m.linear).move_to(p_fade).set_opacity(0.0),
                m.FadeOut(e_dot, run_time=0.02),
            )
            beam_fire_anims.append(anim)

        curve_interference_beam = m.VMobject(stroke_color=m.TEAL_A, stroke_width=2.5)
        curve_interference_beam.set_points_smoothly(inf_pts)

        self.say(
            "直覺上，我們預期電子會像彈珠一樣留下雙線。但令人震驚的是，感光屏上竟然浮現出了波動干涉紋！",
            m.AnimationGroup(*beam_fire_anims, lag_ratio=0.045),
            m.FadeIn(beam_screen_hits, lag_ratio=0.045),
            m.Create(curve_interference_beam),
            m.FadeIn(legend_actual),
        )
        self.wait(0.8)

        self.play(
            m.FadeOut(expected_curve),
            m.FadeOut(legend_expected),
            m.FadeOut(beam_screen_hits),
            m.FadeOut(curve_interference_beam),
            m.FadeOut(legend_actual),
            run_time=0.6,
        )

        # =====================================================================
        # 3.1 0:28 - 0:37 單電子自我干涉三階段
        # =====================================================================

        # -------------------------------------------------------------
        # 1. 為了排除電子間的干涉，我們一次發射一個電子
        # -------------------------------------------------------------
        new_hud_status2b1 = m.Text(
            "關鍵一：一次只發射一顆電子",
            font=CHINESE_FONT,
            font_size=18,
            color=m.YELLOW,
        ).move_to(hud_bar.get_right() - np.array([2.3, 0, 0]))

        cap_step1 = m.Text(
            "【排除干涉】為了排除電子彼此之間的碰撞干涉，我們每次只發射一顆電子。",
            font=CHINESE_FONT,
            font_size=17,
            color=m.WHITE,
        ).move_to(caption_box.get_center())

        self.say(
            "會不會是大量電子在飛行中相互推擠干擾？為了排除這個可能，我們將發射速率降到極低，一次只發射一顆電子。",
            m.Transform(hud_status, new_hud_status2b1),
            m.ReplacementTransform(cap_text3a, cap_step1),
        )

        # 發射第 1 顆電子：飛向狹縫前淡化消失 -> 感光屏亮點 1
        e_single1 = m.Dot(point=[gun_x + 0.75, 0, 0], radius=0.075, color=m.TEAL_A)
        hit_pt1 = np.array([screen_x - 0.12, 0.0, 0])
        hit_dot1 = m.Dot(point=hit_pt1, radius=0.065, color=m.YELLOW)

        self.play(
            m.FadeIn(e_single1),
            e_single1.animate(run_time=0.55, rate_func=m.linear).move_to(np.array([barrier_x - 0.45, 0.25, 0])).set_opacity(0.0),
        )
        self.play(
            m.FadeOut(e_single1),
            m.FadeIn(hit_dot1),
            m.Flash(hit_dot1, color=m.YELLOW, line_length=0.15, flash_radius=0.3),
            run_time=0.35,
        )

        # 發射第 2 顆電子
        e_single2 = m.Dot(point=[gun_x + 0.75, 0, 0], radius=0.075, color=m.TEAL_A)
        hit_pt2 = np.array([screen_x - 0.12, 0.82, 0])
        hit_dot2 = m.Dot(point=hit_pt2, radius=0.065, color=m.YELLOW)

        self.play(
            m.FadeIn(e_single2),
            e_single2.animate(run_time=0.55, rate_func=m.linear).move_to(np.array([barrier_x - 0.45, -0.3, 0])).set_opacity(0.0),
        )
        self.play(
            m.FadeOut(e_single2),
            m.FadeIn(hit_dot2),
            m.Flash(hit_dot2, color=m.YELLOW, line_length=0.15, flash_radius=0.3),
            run_time=0.35,
        )

        # 發射第 3 顆電子
        e_single3 = m.Dot(point=[gun_x + 0.75, 0, 0], radius=0.075, color=m.TEAL_A)
        hit_pt3 = np.array([screen_x - 0.12, -0.82, 0])
        hit_dot3 = m.Dot(point=hit_pt3, radius=0.065, color=m.YELLOW)

        self.play(
            m.FadeIn(e_single3),
            e_single3.animate(run_time=0.55, rate_func=m.linear).move_to(np.array([barrier_x - 0.45, 0.1, 0])).set_opacity(0.0),
        )
        self.play(
            m.FadeOut(e_single3),
            m.FadeIn(hit_dot3),
            m.Flash(hit_dot3, color=m.YELLOW, line_length=0.15, flash_radius=0.3),
            run_time=0.35,
        )
        self.wait(0.3)

        # -------------------------------------------------------------
        # 2. 排除干擾後，干涉紋依然出現
        # -------------------------------------------------------------
        new_hud_status2b2 = m.Text(
            "排除干擾後，干涉紋依然出現",
            font=CHINESE_FONT,
            font_size=18,
            color=m.YELLOW,
        ).move_to(hud_bar.get_right() - np.array([2.3, 0, 0]))

        cap_step2 = m.Text(
            "【加速發射】連續發射成千上萬顆單電子：感光屏上竟然依然浮現出干涉紋！",
            font=CHINESE_FONT,
            font_size=17,
            color=m.YELLOW,
        ).move_to(caption_box.get_center())

        self.say(
            "屏幕上一個個光斑孤立出現。當成千上萬顆單電子累積之後，干涉紋依然清晰浮現！",
            m.Transform(hud_status, new_hud_status2b2),
            m.ReplacementTransform(cap_step1, cap_step2),
        )

        accel_dots = m.VGroup()
        for _ in range(160):
            cand_y = float(np.random.uniform(-2.0, 2.0))
            prob = float((np.cos(3.8 * cand_y) ** 2) * np.exp(-(cand_y**2) / 2.2))
            if np.random.rand() < prob:
                d = m.Dot(point=[screen_x - 0.12, cand_y, 0], radius=0.045, color=m.TEAL_A)
                accel_dots.add(d)

        curve_self_interference = m.VMobject(stroke_color=m.TEAL_A, stroke_width=2.5)
        curve_self_interference.set_points_smoothly(inf_pts)
        self_inf_label = m.Text(
            "干涉紋依然出現", font=CHINESE_FONT, font_size=14, color=m.TEAL_A
        ).next_to(curve_self_interference, m.RIGHT, buff=0.10)

        self.play(
            m.FadeIn(accel_dots, lag_ratio=0.015),
            m.Create(curve_self_interference),
            m.FadeIn(self_inf_label),
            run_time=2.2,
        )
        self.wait(1.0)

        self.play(
            m.FadeOut(hit_dot1),
            m.FadeOut(hit_dot2),
            m.FadeOut(hit_dot3),
            m.FadeOut(accel_dots),
            m.FadeOut(curve_self_interference),
            m.FadeOut(self_inf_label),
            run_time=0.6,
        )

        # -------------------------------------------------------------
        # 3. 揭露本質：發射的電子變成了波，並在通過狹縫時與自己產生了干涉
        # -------------------------------------------------------------
        new_hud_status2b3 = m.Text(
            "奧秘：電子化為波，與自己干涉",
            font=CHINESE_FONT,
            font_size=18,
            color=m.TEAL_A,
        ).move_to(hud_bar.get_right() - np.array([2.3, 0, 0]))

        cap_step3 = m.Text(
            "【揭露奧秘】電子以物質波形態傳播，同時穿過雙狹縫，自己與自己產生了干涉！",
            font=CHINESE_FONT,
            font_size=17,
            color=m.YELLOW,
        ).move_to(caption_box.get_center())

        self.say(
            "這指向了唯一的物理真相：這顆孤獨的電子並非選擇走左縫或右縫，而是以物質波的形態同時通過了兩道狹縫，自己與自己發生了干涉！",
            m.Transform(hud_status, new_hud_status2b3),
            m.ReplacementTransform(cap_step2, cap_step3),
        )

        # 慢速顯現電子化為波的動態演化
        p_start = np.array([gun_x + 0.75, 0, 0])
        p_slit_target = np.array([barrier_x - 0.05, 0, 0])

        evo_particle = m.Dot(point=p_start, radius=0.09, color=m.YELLOW)
        w1_start = m.Arc(
            radius=0.35,
            start_angle=-m.PI / 2.5,
            angle=2 * m.PI / 2.5,
            arc_center=p_start,
            stroke_color=CYAN_COLOR,
            stroke_width=2.2,
            stroke_opacity=0.8,
        )
        w2_start = m.Arc(
            radius=0.7,
            start_angle=-m.PI / 2.5,
            angle=2 * m.PI / 2.5,
            arc_center=p_start,
            stroke_color=CYAN_COLOR,
            stroke_width=2.5,
            stroke_opacity=0.6,
        )
        evo_wave_group = m.VGroup(w1_start, w2_start)

        self.play(m.FadeIn(evo_particle), m.FadeIn(evo_wave_group), run_time=0.3)

        w1_end = m.Arc(
            radius=1.1,
            start_angle=-m.PI / 2.2,
            angle=2 * m.PI / 2.2,
            arc_center=p_slit_target,
            stroke_color=CYAN_COLOR,
            stroke_width=2.5,
            stroke_opacity=0.9,
        )
        w2_end = m.Arc(
            radius=1.5,
            start_angle=-m.PI / 2.2,
            angle=2 * m.PI / 2.2,
            arc_center=p_slit_target,
            stroke_color=CYAN_COLOR,
            stroke_width=2.2,
            stroke_opacity=0.75,
        )
        slit_impact_waves = m.VGroup(w1_end, w2_end)

        self.play(
            evo_particle.animate(run_time=1.2, rate_func=m.linear).move_to(p_slit_target).set_opacity(0.0),
            m.ReplacementTransform(evo_wave_group, slit_impact_waves, run_time=1.2, rate_func=m.linear),
        )

        sub_waves_a = m.VGroup()
        sub_waves_b = m.VGroup()
        evo_radii = np.linspace(0.45, 2.05, 5)
        for r_evo in evo_radii:
            arc_a = m.Arc(
                radius=r_evo,
                start_angle=-m.PI / 2.2,
                angle=2 * m.PI / 2.2,
                arc_center=[barrier_x, slit_y, 0],
                stroke_color=CYAN_COLOR,
                stroke_width=2.4,
                stroke_opacity=max(0.35, 1.0 - r_evo / 2.6),
            )
            arc_b = m.Arc(
                radius=r_evo,
                start_angle=-m.PI / 2.2,
                angle=2 * m.PI / 2.2,
                arc_center=[barrier_x, -slit_y, 0],
                stroke_color=CYAN_COLOR,
                stroke_width=2.4,
                stroke_opacity=max(0.35, 1.0 - r_evo / 2.6),
            )
            sub_waves_a.add(arc_a)
            sub_waves_b.add(arc_b)

        self.play(
            m.FadeOut(evo_particle),
            m.FadeOut(slit_impact_waves),
            m.FadeIn(sub_waves_a, lag_ratio=0.15),
            m.FadeIn(sub_waves_b, lag_ratio=0.15),
            run_time=1.5,
        )

        hit_wave_dot = m.Dot(point=[screen_x - 0.12, 0.0, 0], radius=0.07, color=m.YELLOW)

        self.say(
            "波函數在空間決定了機率分佈，而在撞擊屏幕的測量瞬間，波函數瞬間塌縮，留下一顆實體光斑。",
            m.FadeIn(hit_wave_dot),
            m.Flash(hit_wave_dot, color=m.YELLOW, line_length=0.20, flash_radius=0.35),
        )
        self.wait(0.6)

        self.play(
            m.FadeOut(sub_waves_a),
            m.FadeOut(sub_waves_b),
            m.FadeOut(hit_wave_dot),
            run_time=0.6,
        )

        # =====================================================================
        # 4. 0:38 觀測者塌縮：路徑測量導致干涉消失
        # =====================================================================
        new_hud_status3 = m.Text(
            "狀態：探測器路徑測量 (Which-Way)",
            font=CHINESE_FONT,
            font_size=18,
            color=m.RED_B,
        ).move_to(hud_bar.get_right() - np.array([2.2, 0, 0]))

        cap_text5a = m.Text(
            "【觀測者介入】只要探測器偵測到電子的具體路徑，感光屏就出現對應落點！",
            font=CHINESE_FONT,
            font_size=17,
            color=m.WHITE,
        ).move_to(caption_box.get_center())

        self.say(
            "如果我們想親眼看看到底發生了什麼，在狹縫旁安裝探測器，測量電子究竟通過哪道狹縫呢？",
            m.Transform(hud_status, new_hud_status3),
            m.ReplacementTransform(cap_step3, cap_text5a),
        )

        det_dot_a = m.Circle(
            radius=0.14, fill_color=m.RED, fill_opacity=0.9, stroke_color=m.WHITE, stroke_width=1.5
        )
        det_txt_a = m.Text("探測器 A", font=CHINESE_FONT, font_size=12, color=m.RED_A)
        detector_a = m.VGroup(det_dot_a, det_txt_a).arrange(m.RIGHT, buff=0.10)
        detector_a.move_to(np.array([barrier_x + 0.85, slit_y, 0]))

        det_dot_b = m.Circle(
            radius=0.14, fill_color=m.RED, fill_opacity=0.9, stroke_color=m.WHITE, stroke_width=1.5
        )
        det_txt_b = m.Text("探測器 B", font=CHINESE_FONT, font_size=12, color=m.RED_A)
        detector_b = m.VGroup(det_dot_b, det_txt_b).arrange(m.RIGHT, buff=0.10)
        detector_b.move_to(np.array([barrier_x + 0.85, -slit_y, 0]))

        self.play(
            m.FadeIn(detector_a),
            m.FadeIn(detector_b),
            run_time=0.7,
        )

        cap_text5b = m.Text(
            "探測器 A 閃光偵測！感光屏 A 縫後方立刻亮起，確定電子只通過狹縫 A！",
            font=CHINESE_FONT,
            font_size=17,
            color=m.RED_A,
        ).move_to(caption_box.get_center())

        hit_point_a1 = np.array([screen_x - 0.12, slit_y + 0.08, 0])
        hit_dot_a1 = m.Dot(point=hit_point_a1, radius=0.065, color=m.YELLOW)

        self.say(
            "當探測器 A 閃爍，我們確定電子穿過了狹縫 A，屏幕 A 縫後方隨之亮起。",
            m.ReplacementTransform(cap_text5a, cap_text5b),
            m.Flash(det_dot_a, color=m.RED, line_length=0.25, flash_radius=0.45),
            m.FadeIn(hit_dot_a1),
            m.Flash(hit_dot_a1, color=m.YELLOW, line_length=0.15, flash_radius=0.3),
        )

        cap_text5c = m.Text(
            "探測器 B 閃光偵測！感光屏 B 縫後方立刻亮起，確定電子只通過狹縫 B！",
            font=CHINESE_FONT,
            font_size=17,
            color=m.RED_A,
        ).move_to(caption_box.get_center())

        hit_point_b1 = np.array([screen_x - 0.12, -slit_y - 0.08, 0])
        hit_dot_b1 = m.Dot(point=hit_point_b1, radius=0.065, color=m.YELLOW)

        self.say(
            "當探測器 B 閃爍，電子則被確定穿過狹縫 B。",
            m.ReplacementTransform(cap_text5b, cap_text5c),
            m.Flash(det_dot_b, color=m.RED, line_length=0.25, flash_radius=0.45),
            m.FadeIn(hit_dot_b1),
            m.Flash(hit_dot_b1, color=m.YELLOW, line_length=0.15, flash_radius=0.3),
        )

        cap_text5d = m.Text(
            "密集觀測：感測器高頻交替觸發，波函數頻繁塌縮，干涉圖樣消失還原為經典雙峰！",
            font=CHINESE_FONT,
            font_size=17,
            color=m.YELLOW,
        ).move_to(caption_box.get_center())

        rapid_hits = m.VGroup()
        for _ in range(160):
            choose_a = np.random.rand() > 0.5
            target_y = slit_y if choose_a else -slit_y
            sample_y = float(np.clip(target_y + np.random.normal(0, 0.28), -2.0, 2.0))
            dot = m.Dot(
                point=[screen_x - 0.12, sample_y, 0],
                radius=0.045,
                color=m.YELLOW_B,
            )
            rapid_hits.add(dot)

        alternating_flashes = []
        for i in range(20):
            target_det = det_dot_a if (i % 2 == 0) else det_dot_b
            alternating_flashes.append(
                m.Flash(target_det, color=m.RED, line_length=0.22, flash_radius=0.4, run_time=0.10)
            )

        curve_observed = m.VMobject(stroke_color=m.YELLOW, stroke_width=2.5)
        curve_observed.set_points_smoothly(c_pts)

        obs_label = m.Text(
            "干涉消失：經典雙條紋", font=CHINESE_FONT, font_size=14, color=m.YELLOW
        ).next_to(curve_observed, m.RIGHT, buff=0.10)

        self.say(
            "不可思議的事情發生了：只要我們實施了觀測，干涉條紋便瞬間瓦解，徹底退化回經典的雙線分佈！",
            m.ReplacementTransform(cap_text5c, cap_text5d),
            m.Succession(*alternating_flashes),
            m.FadeIn(rapid_hits, lag_ratio=0.015),
            m.Create(curve_observed),
            m.FadeIn(obs_label),
        )
        self.wait(1.0)

        # =====================================================================
        # 5. 波耳互補原理與數學本質昇華 (Bohr & Quantum Mathematics)
        # =====================================================================
        self.play(
            m.FadeOut(hud_group),
            m.FadeOut(electron_gun_group),
            m.FadeOut(barrier_walls),
            m.FadeOut(screen_group),
            m.FadeOut(caption_box),
            m.FadeOut(cap_text5d),
            m.FadeOut(detector_a),
            m.FadeOut(detector_b),
            m.FadeOut(hit_dot_a1),
            m.FadeOut(hit_dot_b1),
            m.FadeOut(rapid_hits),
            m.FadeOut(curve_observed),
            m.FadeOut(obs_label),
            run_time=1.0,
        )

        bohr_title = m.Text(
            "波耳互補原理 (Complementarity)", font=CHINESE_FONT, font_size=24, color=m.YELLOW
        ).to_edge(m.UP, buff=0.55)

        bohr_quote = m.VGroup(
            m.Text("「物質的波性與粒子性是互補的。」", font=CHINESE_FONT, font_size=20, color=m.WHITE),
            m.Text(
                "「設計用來證實其一的實驗，必然會摧毀展現另一面的可能。」",
                font=CHINESE_FONT,
                font_size=20,
                color=m.WHITE,
            ),
            m.Text("— 尼爾斯·波耳 (Niels Bohr), 1927", font=CHINESE_FONT, font_size=16, color=m.YELLOW_B),
        ).arrange(m.DOWN, buff=0.15).next_to(bohr_title, m.DOWN, buff=0.3)

        self.say(
            "正如波耳提出的互補原理：波動性與粒子性互為補充，任何試圖確定粒子路徑的實驗，都必然摧毀其波動干涉的能力。",
            m.FadeIn(bohr_title, shift=m.UP * 0.2),
            m.FadeIn(bohr_quote),
        )

        # 中央數學公式對比卡片
        math_card_bg = m.Rectangle(
            width=12.2,
            height=2.8,
            fill_color=m.DARK_GREY,
            fill_opacity=0.75,
            stroke_color=m.GREY_D,
            stroke_width=1.5,
        ).move_to(m.DOWN * 1.0)

        # 公式 1：無觀測（疊加態）
        tex_unobserved_label = m.Text(
            "① 無觀測（自由疊加態）：", font=CHINESE_FONT, font_size=17, color=m.TEAL_A
        )
        tex_unobserved = m.MathTex(
            r"P = |\psi_1 + \psi_2|^2 = |\psi_1|^2 + |\psi_2|^2 + 2\mathrm{Re}(\psi_1^* \psi_2)",
            font_size=25,
            color=m.WHITE,
        )
        tex_interference_note = m.Text(
            "← 關鍵干涉交叉項（形成明暗條紋）",
            font=CHINESE_FONT,
            font_size=15,
            color=m.TEAL_B,
        )
        row1 = m.VGroup(tex_unobserved_label, tex_unobserved, tex_interference_note).arrange(
            m.RIGHT, buff=0.20
        )

        # 公式 2：有觀測（波函數塌縮）
        tex_observed_label = m.Text(
            "② 有觀測（波函數塌縮）：", font=CHINESE_FONT, font_size=17, color=m.YELLOW
        )
        tex_observed = m.MathTex(
            r"P = |\psi_1|^2 + |\psi_2|^2",
            font_size=25,
            color=m.WHITE,
        )
        tex_collapse_note = m.Text(
            "← 交叉項歸零，退化為經典機率相加",
            font=CHINESE_FONT,
            font_size=15,
            color=m.YELLOW_B,
        )
        row2 = m.VGroup(tex_observed_label, tex_observed, tex_collapse_note).arrange(
            m.RIGHT, buff=0.20
        )

        math_rows = m.VGroup(row1, row2).arrange(m.DOWN, buff=0.45, aligned_edge=m.LEFT).move_to(math_card_bg.get_center())

        self.say(
            "從數學上看，未受干擾時，兩條路徑的機率振幅相加，產生了關鍵的干涉交叉項；一旦施加觀測，波函數塌縮，交叉項歸零，只剩下經典的機率相加。",
            m.FadeIn(math_card_bg),
            m.FadeIn(math_rows),
        )

        conclusion_box = m.SurroundingRectangle(
            math_card_bg, buff=0.1, color=m.YELLOW, stroke_width=2.5
        )
        final_summary = m.Text(
            "「在微觀量子世界中，觀測不是被動的旁觀，而是參與定義了物理現實。」",
            font=CHINESE_FONT,
            font_size=20,
            color=m.YELLOW,
        ).next_to(math_card_bg, m.DOWN, buff=0.35)

        self.say(
            "在微觀量子世界中，觀測不是被動的旁觀，而是參與定義了物理現實。",
            m.Create(conclusion_box),
            m.FadeIn(final_summary, shift=m.UP * 0.15),
        )
        self.wait(1.5)

        # 結尾淡出
        self.play(*[m.FadeOut(mob) for mob in list(self.mobjects)], run_time=1.2)
        self.wait(0.5)
