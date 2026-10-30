"""Derive narrated variants without overwriting the original silent scenes."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def build(layout, anchors):
    text = (ROOT / f"arc_degree_{layout}.py").read_text(encoding="utf-8-sig")
    original = ast.parse(text)
    text = text.replace("import numpy as np", "import numpy as np\nfrom ArcDegree.narration_scene import NarratedScene")
    title = layout.capitalize()
    text = text.replace(f"class ArcDegree{title}(m.Scene):", f"class ArcDegree{title}F0(NarratedScene):")
    text = text.replace(f"class ArcDegree{title}(TWScene):", f"class ArcDegree{title}F0(NarratedScene):")
    for number, anchor in enumerate(anchors, 1):
        assert text.count(anchor) == 1, (number, anchor, text.count(anchor))
        text = text.replace(anchor, f'        self.begin_narration("{layout}", {number})\n' + anchor)
    text += "\n        self.end_narration()\n        self.wait(0.35)\n"
    text = text.replace("無語音旁白", "F0 聲線旁白")
    def animation_calls(tree):
        return [ast.dump(node) for node in ast.walk(tree)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "self"
                and node.func.attr == "play"]
    assert animation_calls(original) == animation_calls(ast.parse(text)), "Animation timing changed"
    print(layout, len(animation_calls(original)), "animation calls unchanged")
    (ROOT / f"arc_degree_{layout}_f0.py").write_text(text, encoding="utf-8")


build("vertical", [
    "        self.play(m.FadeIn(title_box, shift=m.UP * 0.3), run_time=1.0)",
    "        cap1 = self.make_caption_lines(",
    "        cap2 = self.make_caption_lines(",
    "        cap3 = self.make_caption_lines(",
    "        cap4 = self.make_caption_lines(",
    "        cap5 = self.make_caption_lines(",
    "        cap6 = self.make_caption_lines(",
    "        cap7 = self.make_caption_lines(",
    "        cap8 = self.make_caption_lines(",
    "        cap9 = self.make_caption_lines(",
])
build("landscape", [
    "        self.play(m.FadeIn(center_dot, scale=1.5), run_time=0.6)",
    "        axis_len = 3.6",
    "        arc1 = m.Arc(radius=r1, start_angle=0, angle=np.pi / 2, arc_center=O_INIT, color=C_ARC1, stroke_width=6.0)",
    "        self.play(\n            left_assembly.animate.shift(SHIFT_VEC),",
    "        self.play(\n            m.FadeIn(align_baseline),",
    "        self.play(\n            m.Flash(end_dot1,",
    "        self.play(\n            m.FadeOut(end_dot1),",
    "        self.play(\n            m.Create(ray_x),",
    "        self.play(\n            m.Rotate(sweep_ray,",
    "        self.play(\n            m.FadeOut(sweep_ray),",
    "        self.play(\n            m.Create(rad_line_30),",
    "        self.play(\n            arc1.animate.set_stroke(width=9.0),",
])
