"""Check the geometric invariants and silent delivery streams."""
import json
import subprocess
from pathlib import Path

import numpy as np
from ArcDegree.equal_length_arc_angles import LENGTH, RADII, SWEEPS, STARTS, CENTERS, COLORS, bend, walker, vector

ROOT = Path(__file__).resolve().parent


def geometry():
    for i, (p, r, c) in enumerate(zip(STARTS, RADII, COLORS)):
        for amount in np.linspace(0, 1, 21):
            line = bend(p, r, float(amount), c)
            np.testing.assert_allclose(line.get_start(), p, atol=1e-9)
            points = line.get_points()
            length = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
            assert abs(length-LENGTH)/LENGTH < 1e-4
            arrow = walker(i, float(amount))
            radial = arrow.get_start()-CENTERS[i]
            heading = arrow.get_end()-arrow.get_start()
            assert abs(float(np.dot(radial, heading))) < 1e-8
            np.testing.assert_allclose(np.linalg.norm(radial), r, atol=1e-9)
        assert abs(r*SWEEPS[i]-LENGTH) < 1e-9
    assert len(set(SWEEPS)) == 3
    print("Equal lengths while bending; radius and tangent directions: passed")


def delivery(silent: bool = False):
    video = ROOT / ("EqualLengthArcAngles.mp4" if silent else "EqualLengthArcAnglesLight.mp4")
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)], text=True))
    streams = {s["codec_type"]:s for s in info["streams"]}
    assert ("audio" not in streams) if silent else ("audio" in streams)
    stream = streams["video"]
    assert stream["codec_type"] == "video"
    assert stream["width"] == 1080 and stream["height"] == 1920
    assert stream["r_frame_rate"] == "60/1"
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=True)
    if not silent:
        timeline = json.loads((ROOT / "narration_edge_equal/equal_timeline.json").read_text())
        assert len(timeline) == 10
        assert all(t["section_end"]+1e-6 >= t["audio_end"] for t in timeline)
        assert all(b["start"]+1e-6 >= a["audio_end"] for a,b in zip(timeline,timeline[1:]))
        assert float(info["format"]["duration"]) >= timeline[-1]["audio_end"]
        assert abs(float(streams["audio"]["duration"])-float(stream["duration"])) < 0.1
        assert video.with_suffix(".srt").read_text(encoding="utf-8-sig").count("-->") == 10
    print({"duration":info["format"]["duration"], "silent_no_audio_stream":silent, "full_decode":"passed"})


if __name__ == "__main__":
    import sys
    geometry()
    if "--geometry-only" not in sys.argv:
        delivery(silent="--silent" in sys.argv)
