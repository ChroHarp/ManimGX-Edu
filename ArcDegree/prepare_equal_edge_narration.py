"""Generate only Edge-TTS preview narration; no Colab or voice conversion."""
import asyncio
import hashlib
import json
import subprocess
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent / "narration_edge_equal"
LINES = (
    "取三條一樣長的線段，分別叫做 a、b、c。",
    "把它們彎成不同半徑的圓弧。雖然長度相同，形狀卻不一樣。",
    "就算把起點和前進方向對齊，三段圓弧還是無法完全疊合。",
    "讓箭頭從 a 的一端出發，沿圓弧前進，記錄方向總共偏轉的角度。",
    "接著畫出圓心和兩條半徑。箭頭偏轉的角度，就是這段圓弧所對的圓心角。",
    "在 b、c 上也做同樣的觀察。雖然弧長相同，但它們的偏轉角和圓心角都不同。",
    "因此，一個圓弧除了長度以外，還可以測量角度。這個角度，就是它所對的圓心角。",
    "現在把三段圓弧移到同一個圓心，各自的半徑保持不變。",
    "再把三段弧的張角調成相同。注意，半徑不變時，調整張角也會改變弧長。",
    "所以，同心圓中，對應同一個圓心角的圓弧，角度相同，但弧長可以不同。",
)


async def main():
    (ROOT / "final").mkdir(parents=True, exist_ok=True)
    (ROOT / "source").mkdir(exist_ok=True)
    records = []
    missing = []
    for i, text in enumerate(LINES, 1):
        key = f"equal_{i:02d}"
        profile = {"text":text, "voice":"zh-TW-YunJheNeural", "rate":"+12%", "pitch":"+0Hz"}
        fingerprint = hashlib.sha256(json.dumps(profile, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        metadata = ROOT / "source" / f"{key}.json"
        final = ROOT / "final" / f"{key}.wav"
        cached = metadata.exists() and final.exists() and json.loads(metadata.read_text(encoding="utf-8")).get("fingerprint") == fingerprint
        if not cached:
            mp3 = ROOT / "source" / f"{key}.mp3"
            for attempt in range(3):
                try:
                    await edge_tts.Communicate(text, voice=profile["voice"], rate=profile["rate"], pitch=profile["pitch"]).save(str(mp3))
                    break
                except Exception:
                    print("Retry", key, attempt+1, flush=True)
                    if attempt == 2:
                        missing.append(key)
                        break
                    await asyncio.sleep(2)
            if key in missing:
                continue
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-af", "loudnorm=I=-18:TP=-2:LRA=9", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(final)], check=True)
            metadata.write_text(json.dumps({"fingerprint":fingerprint, **profile}, ensure_ascii=False, indent=2), encoding="utf-8")
        import wave
        with wave.open(str(final)) as wav:
            duration = wav.getnframes()/wav.getframerate()
        records.append({"key":key, "text":text, "duration":duration, "fingerprint":fingerprint, "audio_sha256":hashlib.sha256(final.read_bytes()).hexdigest()})
        print(key, duration, flush=True)
    if missing:
        raise RuntimeError(f"No audio returned for {missing}; successful clips are cached for retry.")
    (ROOT / "manifest.json").write_text(json.dumps({"source_voice":"zh-TW-YunJheNeural", "rate":"+12%", "pitch":"+0Hz", "stage":"Edge-TTS preview only", "clips":records}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())
