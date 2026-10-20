import asyncio
import edge_tts
import subprocess
import os

FFMPEG_PATH = "ffmpeg"
FFPROBE_PATH = "ffprobe"

PROJECT_DIR = r"d:\WebDesign\ManimCEAnimate"
LAW_OF_COSINES_DIR = os.path.join(PROJECT_DIR, "LawOfCosines")
TTS_DIR = os.path.join(LAW_OF_COSINES_DIR, "tts")
AUDIO_OUTPUT = os.path.join(LAW_OF_COSINES_DIR, "master_narration.mp3")

VIDEO_INPUT_480 = os.path.join(LAW_OF_COSINES_DIR, "media", "videos", "law_of_cosines", "480p15", "LawOfCosines.mp4")
VIDEO_INPUT_1080 = os.path.join(LAW_OF_COSINES_DIR, "media", "videos", "law_of_cosines", "1080p60", "LawOfCosines.mp4")
VIDEO_OUTPUT = os.path.join(LAW_OF_COSINES_DIR, "LawOfCosines_with_voice.mp4")

os.makedirs(TTS_DIR, exist_ok=True)

# 台灣男聲: zh-TW-YunJheNeural（雲哲）
VOICE = "zh-TW-YunJheNeural"

# 注意破音字修正原則（依據 manim-math-animation 技能）：
# 「為」在「邊長為」、「夾角為」、「放大為」、「化簡為」等幾何情境中，一律換成同音字「唯」（二聲 wéi）。
# 「總和」換成同音字「總核」（二聲 hé）。
SEGMENTS = [
    {
        "id": "seg_01",
        "start": 1.0,
        "text": "先考慮任意三角形，三邊長唯 a、b、c，夾角唯 A。",
        "rate": "+15%",
        "comment": "Part 1: 原始三角形 (為->唯)"
    },
    {
        "id": "seg_02",
        "start": 6.8,
        "text": "複製第一份三角形，將邊長放大 b 倍，得到 b 平方、a b 與 b c，並就定位於左側。",
        "rate": "+16%",
        "comment": "Part 2: 乘 b (為->唯)"
    },
    {
        "id": "seg_03",
        "start": 13.8,
        "text": "接著複製第二份，邊長放大 a 倍。此時特別高亮長度唯 a b 的這條邊，與左側三角形完美貼合。",
        "rate": "+16%",
        "comment": "Part 3: 乘 a，高亮 ab 邊 (為->唯)"
    },
    {
        "id": "seg_04",
        "start": 22.8,
        "text": "第三份三角形放大 c 倍。高亮彼此對應的 a c 邊，旋轉後緊密接在右側。",
        "rate": "+16%",
        "comment": "Part 4: 乘 c，高亮 ac 邊"
    },
    {
        "id": "seg_05",
        "start": 30.5,
        "text": "三塊三角形完全拼合。頂部三個內角總核唯 180 度，形成平整上邊，長度唯 b 平方加 c 平方；下邊中央唯 a 平方。",
        "rate": "+18%",
        "comment": "Part 5: 外框平整上邊與下邊 (為->唯, 總和->總核)"
    },
    {
        "id": "seg_06",
        "start": 40.5,
        "text": "觀察左側邊長 b c，其與水平線夾角唯 A。作垂直線向下投影，得到水平底邊長度唯 b c 乘 cosine A。",
        "rate": "+16%",
        "comment": "Part 6: 左側投影 (為->唯)"
    },
    {
        "id": "seg_07",
        "start": 49.5,
        "text": "右側邊長同唯 b c，作垂直投影，亦得到水平底邊長度唯 b c 乘 cosine A。",
        "rate": "+16%",
        "comment": "Part 7: 右側投影 (為->唯)"
    },
    {
        "id": "seg_08",
        "start": 57.5,
        "text": "外框唯一個矩形，上邊長等於下邊長：b 平方加 c 平方等於 a 平方加兩倍 b c cosine A。移項整理，即證得餘弦定理！",
        "rate": "+16%",
        "comment": "Part 8: 矩形上下邊比較與結論 (為->唯)"
    },
    {
        "id": "seg_09",
        "start": 68.0,
        "text": "最後延伸一個重要特例：當夾角 A 唯 90 度直角時，圖形變形唯三個直角三角形，兩側投影項歸零，外框完美密合成一個長方形。式子化簡唯 a 平方等於 b 平方加 c 平方，這正是著名的畢氏定理！",
        "rate": "+20%",
        "comment": "Part 9: 特例延伸－直角時變形密合成矩形，化簡為畢氏定理 (為->唯)"
    }
]

async def generate_and_mux():
    print("=== Step 1: Generating Edge-TTS Audio Chunks ===")
    seg_files = []
    for i, seg in enumerate(SEGMENTS):
        out_p = os.path.join(TTS_DIR, f"{seg['id']}.mp3")
        dur = 0.0
        for attempt in range(3):
            c = edge_tts.Communicate(seg["text"], voice=VOICE, rate=seg["rate"])
            await c.save(out_p)
            res = subprocess.run(
                [FFPROBE_PATH, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_p],
                capture_output=True, text=True
            )
            try:
                dur = float(res.stdout.strip())
            except Exception:
                dur = 0.0
            if dur >= 1.0 or len(seg["text"]) < 5:
                break
            await asyncio.sleep(1)
        
        next_s = SEGMENTS[i+1]["start"] if i+1 < len(SEGMENTS) else 999.0
        gap = next_s - (seg['start'] + dur)
        print(f"[{seg['id']}] start={seg['start']:.2f}s, dur={dur:.2f}s, end={seg['start']+dur:.2f}s, next={next_s:.2f}s, gap={gap:.2f}s")
        assert seg["start"] + dur <= next_s, f"Segment {seg['id']} overlaps by {-(gap):.2f}s!"
        seg_files.append((out_p, seg["start"]))

    print("\n=== Step 2: Mixing Master Narration with FFmpeg ===")
    filter_parts = []
    inputs = []
    for i, (p, st) in enumerate(seg_files):
        inputs.extend(["-i", p])
        ms = int(round(st * 1000))
        filter_parts.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    mix_ins = "".join(f"[a{i}]" for i in range(len(seg_files)))
    filter_parts.append(f"{mix_ins}amix=inputs={len(seg_files)}:normalize=0:dropout_transition=0[aout]")
    
    cmd_audio = [FFMPEG_PATH, "-y", *inputs, "-filter_complex", ";".join(filter_parts), "-map", "[aout]", AUDIO_OUTPUT]
    subprocess.run(cmd_audio, check=True)
    print(f"Saved master audio to {AUDIO_OUTPUT}")

    print("\n=== Step 3: Multiplexing Video and Audio ===")
    video_to_use = VIDEO_INPUT_1080 if os.path.exists(VIDEO_INPUT_1080) else VIDEO_INPUT_480

    cmd_mux = [
        FFMPEG_PATH, "-y",
        "-i", video_to_use,
        "-i", AUDIO_OUTPUT,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        VIDEO_OUTPUT
    ]
    subprocess.run(cmd_mux, check=True)
    print(f"\nSUCCESS! Master video generated at: {VIDEO_OUTPUT}")

if __name__ == "__main__":
    asyncio.run(generate_and_mux())
