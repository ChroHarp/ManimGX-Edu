"""Generate Edge-TTS preview narration for ArcDegreeLandscapeLight."""
import asyncio
import hashlib
import json
import subprocess
import wave
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from manimgx_tw_helper import _synthesize_edge_tts_bytes, fix_tw_heteronyms

ROOT = Path(__file__).resolve().parent / "narration_edge_light"
LINES = [
    "以同一個圓心，向外展開三個不同半徑的同心圓。",
    "通過圓心畫出兩條垂直軸線，切出四分之一圓，也就是九十度。",
    "聚焦在第一象限的三段圓弧。半徑不同，長度也明顯不同。",
    "圖形平移向左，將三段圓弧平滑拉直為線段，起點對齊。",
    "可以清楚看見：半徑越長，拉直後的弧長就越長。",
    "接著將線段平滑捲回圓弧。弧長雖然不同，那麼圓弧的度數呢？",
    "圓弧的度數，本質上就是沿著弧線前進時，轉彎轉過的角度。",
    "在三段圓弧的起點標出點和切向箭頭，同時在右側記錄初始方向。",
    "箭頭前進的時候，會隨著路徑平滑轉彎。",
    "抵達九十度終點時，箭頭轉向左方。將終點方向與初始方向進行比較。",
    "可以看見：三段圓弧前進時，箭頭轉過的角度完全相同，都是九十度！",
    "這個轉彎的角度，正好等於所對的圓心角。因此，這三段圓弧的度數完全相同，都是九十度！",
    "不是九十度的時候，箭頭偏轉的角度依然等於圓心角，因此我們將圓弧的角度，定義為圓心角的度數！",
]


async def main():
    (ROOT / "final").mkdir(parents=True, exist_ok=True)
    (ROOT / "source").mkdir(exist_ok=True)
    records = []
    for i, text in enumerate(LINES, 1):
        key = f"light_{i:02d}"
        profile = {"text": text, "voice": "zh-TW-YunJheNeural", "rate": "+12%", "pitch": "+0Hz"}
        fingerprint = hashlib.sha256(json.dumps(profile, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        metadata = ROOT / "source" / f"{key}.json"
        final = ROOT / "final" / f"{key}.wav"
        mp3 = ROOT / "source" / f"{key}.mp3"

        cached = (
            metadata.exists()
            and final.exists()
            and json.loads(metadata.read_text(encoding="utf-8")).get("fingerprint") == fingerprint
        )
        if not cached:
            spoken_text = fix_tw_heteronyms(text)
            mp3_bytes = await _synthesize_edge_tts_bytes(spoken_text, profile["voice"], profile["rate"], profile["pitch"])
            mp3.write_bytes(mp3_bytes)

            subprocess.run([
                "ffmpeg", "-y", "-v", "error",
                "-i", str(mp3),
                "-af", "loudnorm=I=-18:TP=-2:LRA=9",
                "-ar", "48000",
                "-ac", "1",
                "-c:a", "pcm_s16le",
                str(final),
            ], check=True)
            metadata.write_text(json.dumps({"fingerprint": fingerprint, **profile}, ensure_ascii=False, indent=2), encoding="utf-8")

        with wave.open(str(final)) as wav:
            duration = wav.getnframes() / wav.getframerate()
        records.append({
            "key": key,
            "text": text,
            "duration": duration,
            "fingerprint": fingerprint,
            "audio_sha256": hashlib.sha256(final.read_bytes()).hexdigest(),
        })
        print(f"{key}: {duration:.2f}s - {text}", flush=True)

    (ROOT / "manifest.json").write_text(
        json.dumps({
            "source_voice": "zh-TW-YunJheNeural",
            "rate": "+12%",
            "pitch": "+0Hz",
            "stage": "Edge-TTS preview only",
            "clips": records,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("All narration clips generated successfully!", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
