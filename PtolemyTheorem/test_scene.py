import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import manimgx as m
from manimgx_tw_helper import TWScene, YunJheVoice

m.config.pixel_width = 1080
m.config.pixel_height = 1920
m.config.frame_height = 16.0

class TestVertical(TWScene):
    def construct(self) -> None:
        title = m.Text("托勒密定理", font_size=40).move_to([0, 6.5, 0])
        circle = m.Circle(radius=1.65, color=m.WHITE).move_to([0, 2.7, 0])
        self.play(m.FadeIn(title), m.Create(circle))
        self.wait(0.5)
