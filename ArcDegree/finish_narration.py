"""Prepare final clips and record measurable delivery checks after conversion."""
import json
import subprocess
import wave
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "narration_f0"


def main():
    converted = ROOT / "converted"
    converted.mkdir(exist_ok=True)
    with zipfile.ZipFile(ROOT / "arc_converted.zip") as z:
        z.extractall(converted)
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    final = ROOT / "final"
    final.mkdir(exist_ok=True)
    for clip in manifest["clips"]:
        key = clip["key"]
        source = converted / f"{key}_vc.wav"
        if not source.exists():
            raise FileNotFoundError(f"Conversion incomplete: {source}")
        dest = final / f"{key}.wav"
        # Normalization only; no pitch shifting, time stretch or noise reduction.
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(source), "-af", "loudnorm=I=-18:TP=-2:LRA=9", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(dest)], check=True)
        with wave.open(str(dest)) as audio:
            clip["duration"] = audio.getnframes() / audio.getframerate()
        print(key, clip["duration"])
    manifest["timing_policy"] = "Original animation run_time preserved; wait for remaining speech only at section boundaries."
    (ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
