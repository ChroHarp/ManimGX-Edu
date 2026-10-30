"""Verify complete decode, output streams and non-overlapping narration timelines."""
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "narration_f0"
report = {}
for layout, count in [("Landscape", 12), ("Vertical", 10)]:
    video = ROOT / f"ArcDegree{layout}F0.mp4"
    info = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)
    ], text=True))
    streams = {s["codec_type"]: s for s in info["streams"]}
    assert {"video", "audio"} <= streams.keys()
    assert streams["video"]["codec_name"] == "h264"
    assert streams["audio"]["codec_name"] == "aac"
    assert streams["video"]["r_frame_rate"] == "60/1"
    timeline = json.loads((AUDIO / f"{layout.lower()}_timeline.json").read_text())
    assert len(timeline) == count
    assert all(t["section_end"] + 1e-6 >= t["audio_end"] for t in timeline)
    assert all(b["start"] + 1e-6 >= a["audio_end"] for a, b in zip(timeline, timeline[1:]))
    duration = float(info["format"]["duration"])
    assert duration >= timeline[-1]["audio_end"]
    assert abs(float(streams["video"]["duration"]) - float(streams["audio"]["duration"])) < 0.1
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=True)
    srt = video.with_suffix(".srt").read_text(encoding="utf-8-sig")
    assert srt.count("-->") == count
    peak = 0.0
    for t in timeline:
        with wave.open(str(AUDIO / "final" / (t["key"] + ".wav"))) as f:
            samples = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(float) / 32768
            assert np.max(np.abs(samples)) < 1.0
            peak = max(peak, float(np.max(np.abs(samples))))
    report[layout] = {"duration": duration, "width": streams["video"]["width"],
                      "height": streams["video"]["height"], "fps": 60,
                      "narration_clips": count, "full_decode": "passed",
                      "subtitles": "passed", "no_audio_overlap_or_cutoff": "passed",
                      "peak_dbfs": 20 * float(np.log10(peak))}
    print(layout, report[layout])
(AUDIO / "delivery_checks.json").write_text(json.dumps(report, indent=2))
