"""Generate Taiwan Mandarin source clips, keeping display and spoken text separate."""
import asyncio
import hashlib
import json
import re
import subprocess
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "narration_f0"


async def main():
    records = []
    for layout in ("Landscape", "Vertical"):
        srt = (ROOT / f"ArcDegree{layout}.srt").read_text(encoding="utf-8-sig")
        for block in re.split(r"\n\s*\n", srt.strip()):
            lines = block.splitlines()
            text = "".join(lines[2:])
            key = f"{layout.lower()}_{int(lines[0]):02d}"
            spoken = text.replace("圓心 O 為", "圓心歐唯").replace("圓心 O", "圓心歐").replace("90度", "九十度")
            spoken = spoken.replace("拉直為", "拉直唯")
            dest = OUT / "source_rate12" / f"{key}.wav"
            dest.parent.mkdir(parents=True, exist_ok=True)
            mp3 = dest.with_suffix(".mp3")
            if not dest.exists():
                for attempt in range(8):
                    try:
                        await edge_tts.Communicate(spoken, voice="zh-TW-YunJheNeural", rate="+12%", pitch="+0Hz").save(str(mp3))
                        break
                    except Exception:
                        print(f"retry {key}: {attempt + 1}", flush=True)
                        if attempt == 7:
                            raise
                        await asyncio.sleep(2)
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-ar", "44100", "-ac", "1", str(dest)], check=True)
            records.append({"key": key, "text": text, "spoken_text": spoken, "source_sha256": hashlib.sha256(dest.read_bytes()).hexdigest()})
            print(key, flush=True)
    (OUT / "manifest.json").write_text(json.dumps({"source_voice": "zh-TW-YunJheNeural", "rate": "+12%", "pitch": "+0Hz", "clips": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    import zipfile
    with zipfile.ZipFile(OUT / "arc_sources.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in (OUT / "source_rate12").glob("*.wav"):
            z.write(f, "source/" + f.name)
        z.write(OUT / "manifest.json", "manifest.json")


if __name__ == "__main__":
    asyncio.run(main())
