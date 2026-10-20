import asyncio
import edge_tts
import subprocess
import os

FFMPEG_PATH = "ffmpeg"
FFPROBE_PATH = "ffprobe"

PROJECT_DIR = r"d:\WebDesign\ManimCEAnimate"
SUM_OF_CUBES_DIR = os.path.join(PROJECT_DIR, "SumOfCubes")
AUDIO_OUTPUT = os.path.join(SUM_OF_CUBES_DIR, "master_narration.mp3")

# 採用台灣男聲: zh-TW-YunJheNeural（雲哲）
VOICE = "zh-TW-YunJheNeural"

# 注意破音字修正原則（依據 manim-math-animation 技能）：
# 「為」在「邊長為」、「體積為」、「截面為」、「面積為」等幾何情境中，教育部國語辭典標準讀音為二聲 wéi。
# edge-tts 若直接寫「為」易誤讀為去聲「位」（wèi），因此在 TTS 文本中一律替換為同音字「唯」，保證二聲 wéi。
SEGMENTS = [
    {
        "id": "seg_0",
        "start": 0.40,
        "text": "先考慮邊長唯 a 與 b 的兩個正方體。",
        "rate": "+15%",
        "comment": "0.0s~4.0s: 並列顯示 (為->唯)"
    },
    {
        "id": "seg_1",
        "start": 4.80,
        "text": "將兩個正方體靠著角落緊密貼合在一起。",
        "rate": "+15%",
        "comment": "4.0s~8.6s: 角落貼合"
    },
    {
        "id": "seg_2",
        "start": 9.20,
        "text": "直接切出一根截面唯 b 平方、長度唯 a 加 b 的長方角柱。",
        "rate": "+16%",
        "comment": "8.6s~15.6s: 切出 b^2*(a+b) 角柱 (為->唯)"
    },
    {
        "id": "seg_3",
        "start": 16.20,
        "text": "視角切換至平面圖，檢視剩下的 L 形截面。",
        "rate": "+16%",
        "comment": "15.6s~20.2s: 切換到平面圖"
    },
    {
        "id": "seg_4",
        "start": 20.60,
        "text": "回頭看剩下的 L 形：外圍邊長唯 a，被挖去邊長唯 b。",
        "rate": "+22%",
        "comment": "20.2s~25.0s: 顯示外圍邊長 a 和被挖去邊長 b (為->唯)"
    },
    {
        "id": "seg_5",
        "start": 25.40,
        "text": "將 L 形切成兩塊：一塊唯 a 減 b 乘 a，另一塊唯 b 乘 a 減 b。",
        "rate": "+22%",
        "comment": "25.0s~29.4s: 分割成兩塊長方形 (為->唯)"
    },
    {
        "id": "seg_6",
        "start": 31.00,
        "text": "藍色長方形直接往上移並旋轉，重組唯 a 加 b 乘上 a 減 b 的長方形。",
        "rate": "+18%",
        "comment": "29.4s~37.8s: 藍色向上旋轉重組 (為->唯)"
    },
    {
        "id": "seg_7a",
        "start": 38.60,
        "text": "回到立體視角，將兩大長方體旋轉對齊。",
        "rate": "+16%",
        "comment": "37.8s~44.5s: 回到 3D 視角並旋轉"
    },
    {
        "id": "seg_7b",
        "start": 45.20,
        "text": "兩者具有共同長度 a 加 b，隨後緊密貼合。",
        "rate": "+16%",
        "comment": "44.5s~51.0s: 標註共同長度 a+b 並貼合"
    },
    {
        "id": "seg_8",
        "start": 51.80,
        "text": "觀察對齊後的頂部截面，總截面積唯 a 乘上 a 減 b，加上 b 平方。",
        "rate": "+18%",
        "comment": "51.0s~58.0s: 頂部截面 a(a-b)+b^2 (為->唯)"
    },
    {
        "id": "seg_9",
        "start": 58.60,
        "text": "展開並化簡截面積，得到 a 平方減 a b 加 b 平方。",
        "rate": "+18%",
        "comment": "58.0s~63.1s: 化簡為 a^2-ab+b^2"
    },
    {
        "id": "seg_10",
        "start": 63.80,
        "text": "總體積等於底面積乘上高，由此證得立方核公式：a 三方加 b 三方，等於 a 加 b，乘上 a 平方減 a b 加 b 平方。",
        "rate": "+22%",
        "comment": "63.1s~77.2s: 得到立方和公式 (和->核，避免讀為 hàn)"
    }
]

async def generate_all_segments(voice=VOICE, total_duration=77.20):
    tts_dir = os.path.join(SUM_OF_CUBES_DIR, "audio", "tts")
    os.makedirs(tts_dir, exist_ok=True)

    seg_files = []
    print(f"=== Generating Narration Segments with Taiwan Male Voice ({voice}) ===")
    all_ok = True
    for i, seg in enumerate(SEGMENTS):
        out_path = os.path.join(tts_dir, f"{seg['id']}.mp3")
        c = edge_tts.Communicate(seg["text"], voice=voice, rate=seg["rate"])
        await c.save(out_path)

        res = subprocess.run(
            [FFPROBE_PATH, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_path],
            capture_output=True,
            text=True
        )
        dur = float(res.stdout.strip())
        next_start = SEGMENTS[i+1]["start"] if i+1 < len(SEGMENTS) else total_duration
        end_time = seg["start"] + dur
        status = "OK" if end_time <= next_start else "OVERLAP!"
        if status != "OK":
            all_ok = False
        margin = next_start - end_time
        print(f"[{status:8s}] {seg['id']:7s} (start={seg['start']:.2f}s, dur={dur:.2f}s, end={end_time:.2f}s | next={next_start:.2f}s, margin={margin:+.2f}s)")
        print(f"           Text: {seg['text']}")
        seg_files.append((out_path, seg["start"], dur))
    
    print(f"\nAll segments validation: {'PASSED' if all_ok else 'FAILED OVERLAP'}")
    return seg_files, all_ok

def mix_audio_and_mux_video(seg_files, video_input=None, video_output=None, total_duration=77.20):
    print("\n=== Mixing Master Audio with FFmpeg ===")
    filter_parts = []
    inputs = []

    for i, (path, start, dur) in enumerate(seg_files):
        inputs.extend(["-i", path])
        delay_ms = int(round(start * 1000))
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")

    mix_inputs = "".join(f"[a{i}]" for i in range(len(seg_files)))
    filter_parts.append(f"{mix_inputs}amix=inputs={len(seg_files)}:normalize=0:dropout_transition=0[aout]")

    filter_str = ";".join(filter_parts)

    mix_cmd = [
        FFMPEG_PATH, "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[aout]",
        "-t", f"{total_duration:.2f}",
        AUDIO_OUTPUT
    ]
    subprocess.run(mix_cmd, check=True)
    print(f"Master audio generated: {AUDIO_OUTPUT}")

    if video_input and video_output and os.path.exists(video_input):
        print(f"\n=== Muxing Audio and Video ({video_input}) ===")
        mux_cmd = [
            FFMPEG_PATH, "-y",
            "-i", video_input,
            "-i", AUDIO_OUTPUT,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            video_output
        ]
        subprocess.run(mux_cmd, check=True)
        print(f"Master Video successfully created: {video_output}")

async def main():
    video_in = os.path.join(SUM_OF_CUBES_DIR, "SumOfCubes.mp4")
    
    tot_dur = 77.20
    if os.path.exists(video_in):
        res = subprocess.run(
            [FFPROBE_PATH, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_in],
            capture_output=True,
            text=True
        )
        try:
            tot_dur = float(res.stdout.strip())
        except ValueError:
            pass

    seg_files, all_ok = await generate_all_segments(total_duration=tot_dur)
    if not all_ok:
        print("ERROR: Timeline has overlaps! Please adjust rates or start times.")
        return

    video_out = os.path.join(SUM_OF_CUBES_DIR, "SumOfCubes_with_voice.mp4")
    mix_audio_and_mux_video(seg_files, video_in, video_out, total_duration=tot_dur)

if __name__ == "__main__":
    asyncio.run(main())
