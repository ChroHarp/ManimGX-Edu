"""Reuse four accepted clips and synthesize six revised storyboard lines."""
import argparse
import asyncio
import hashlib
import json
import shutil
import subprocess
import wave
import zipfile
from pathlib import Path

import edge_tts

BASE = Path(__file__).resolve().parent
ROOT = BASE / "narration_turning"
CHANGES = {
    3: "從圓心切出一個扇形，觀察其中的三段同心圓弧。",
    4: "沿著扇形，留下三段半徑不同的同心圓弧。",
    6: "箭頭沿內弧從 A 一走到 B 一，方向跟著轉彎。",
    7: "換成另外兩段圓弧，箭頭偏轉的角度也完全相同。",
    8: "把起點與終點的方向放在一起，量出箭頭偏轉的角度。",
    9: "這個偏轉角等於圓心角，就用它來定義圓弧的度數。",
}


async def prepare():
    for folder in ("final", "source"):
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    old = json.loads((BASE / "narration_f0/manifest.json").read_text(encoding="utf-8"))
    clips = []
    for record in old["clips"]:
        if not record["key"].startswith("vertical_"):
            continue
        record = dict(record)
        key = record["key"]
        number = int(key.split("_")[1])
        if number in CHANGES:
            record["text"] = record["spoken_text"] = CHANGES[number]
            mp3 = ROOT / "source" / f"{key}.mp3"
            wav = mp3.with_suffix(".wav")
            if not wav.exists():
                for attempt in range(8):
                    try:
                        await edge_tts.Communicate(record["spoken_text"], voice="zh-TW-YunJheNeural", rate="+12%", pitch="+0Hz").save(str(mp3))
                        break
                    except Exception:
                        print("Retry", key, attempt+1, flush=True)
                        if attempt == 7:
                            raise
                        await asyncio.sleep(2)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-ar", "44100", "-ac", "1", str(wav)], check=True)
            record["source_sha256"] = hashlib.sha256(wav.read_bytes()).hexdigest()
            record.pop("duration", None)
        else:
            shutil.copy2(BASE / "narration_f0/final" / f"{key}.wav", ROOT / "final" / f"{key}.wav")
            record["reused_unchanged"] = True
        clips.append(record)
        print(key, flush=True)
    manifest = {"source_voice": "zh-TW-YunJheNeural", "rate": "+12%", "pitch": "+0Hz", "clips": clips}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    with zipfile.ZipFile(ROOT / "arc_sources.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in (ROOT / "source").glob("*.wav"):
            z.write(f, "source/" + f.name)
        z.write(ROOT / "manifest.json", "manifest.json")


def finish():
    converted = ROOT / "converted"
    converted.mkdir(exist_ok=True)
    with zipfile.ZipFile(ROOT / "arc_converted.zip") as z:
        z.extractall(converted)
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    for record in manifest["clips"]:
        key = record["key"]
        final = ROOT / "final" / f"{key}.wav"
        if not record.get("reused_unchanged"):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(converted / f"{key}_vc.wav"), "-af", "loudnorm=I=-18:TP=-2:LRA=9", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(final)], check=True)
        with wave.open(str(final)) as f:
            record["duration"] = f.getnframes()/f.getframerate()
        print(key, record["duration"])
    (ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--finish", action="store_true")
    args = parser.parse_args()
    if args.finish:
        finish()
    else:
        asyncio.run(prepare())
