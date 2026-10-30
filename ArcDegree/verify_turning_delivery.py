"""Check invariant endpoints, arc lengths, tangent directions and final media."""
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from ArcDegree.arc_degree_vertical_turning import COLORS, RADII, START, TURN, ORIGIN, point, tangent_arrow, unrolled_arc

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "narration_turning"


def geometry():
    for radius, color in zip(RADII, COLORS):
        for amount in np.linspace(0, 1, 21):
            curve = unrolled_arc(radius, float(amount), color)
            np.testing.assert_allclose(curve.get_start(), point(radius, START+TURN), atol=1e-9)
            vertices = curve.get_points()
            measured = float(np.linalg.norm(np.diff(vertices, axis=0), axis=1).sum())
            assert abs(measured-radius*TURN)/(radius*TURN) < 1e-4
            arrow = tangent_arrow(radius, float(amount), color)
            heading = arrow.get_end()-arrow.get_start()
            radial = arrow.get_start()-ORIGIN
            assert abs(float(np.dot(heading, radial))) < 1e-8
        np.testing.assert_allclose(unrolled_arc(radius, 0, color).get_end(), point(radius, START), atol=1e-9)
        np.testing.assert_allclose(unrolled_arc(radius, 1, color).get_end(), point(radius, START+TURN)+[radius*TURN,0,0], atol=1e-9)
    print("B endpoints, preserved lengths, tangent directions: passed")


def media():
    video = ROOT / "ArcDegreeVerticalTurning.mp4"
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)], text=True))
    streams = {s["codec_type"]:s for s in info["streams"]}
    assert streams["video"]["width"] == 1080 and streams["video"]["height"] == 1920
    assert streams["video"]["r_frame_rate"] == "60/1"
    assert streams["audio"]["codec_name"] == "aac"
    timeline = json.loads((REPORT / "vertical_timeline.json").read_text())
    assert len(timeline) == 10
    assert all(t["section_end"]+1e-6 >= t["audio_end"] for t in timeline)
    assert all(b["start"]+1e-6 >= a["audio_end"] for a,b in zip(timeline,timeline[1:]))
    assert float(info["format"]["duration"]) >= timeline[-1]["audio_end"]
    assert abs(float(streams["audio"]["duration"])-float(streams["video"]["duration"])) < 0.1
    assert video.with_suffix(".srt").read_text(encoding="utf-8-sig").count("-->") == 10
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=True)
    old = ROOT / "narration_f0/final/vertical_05.wav"
    new = REPORT / "final/vertical_05.wav"
    assert hashlib.sha256(old.read_bytes()).digest() == hashlib.sha256(new.read_bytes()).digest()
    manifest = json.loads((REPORT / "manifest.json").read_text(encoding="utf-8"))
    assert not any(word in c["text"] for c in manifest["clips"] for word in ("九十", "七十", "90", "70"))
    result = {"duration":float(info["format"]["duration"]), "geometry_invariants":"passed", "complete_decode":"passed", "audio_timeline":"passed", "subtitles":10, "length_comparison_original_audio":"identical", "no_specific_degrees_in_narration":True}
    (REPORT / "delivery_checks.json").write_text(json.dumps(result,indent=2))
    print(result)


if __name__ == "__main__":
    import sys
    geometry()
    if "--geometry-only" not in sys.argv:
        media()
