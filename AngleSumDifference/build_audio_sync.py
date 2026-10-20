import asyncio
import edge_tts
import subprocess
import os

VOICE = "zh-TW-YunJheNeural"

# 破音字校正原則：
# 1. 「和」一律發「禾」（hé）：禾角公式
# 2. 「差」一律發「插」（chā）：插角公式
# 3. 「為」一律發「唯」（wéi）：斜邊唯 1、長度唯 1、唯骨架
# 片頭切勿加「歡迎來到」等贅詞，直接朗讀標題「禾角與插角公式的幾何圖解」
SEGMENTS = [
    {
        "id": "seg_0",
        "start": 0.4,
        "text": "禾角與插角公式的幾何圖解。",
        "rate": "+10%"
    },
    {
        "id": "seg_1",
        "start": 4.2,
        "text": "首先，準備兩個斜邊唯 1 的單位直角三角形。",
        "rate": "+15%"
    },
    {
        "id": "seg_2",
        "start": 8.4,
        "text": "以貝塔三角形唯骨架，旋轉阿爾法角放在中央。",
        "rate": "+15%"
    },
    {
        "id": "seg_3",
        "start": 12.8,
        "text": "將阿爾法形縮放寇賽因貝塔倍，貼於底部。",
        "rate": "+18%"
    },
    {
        "id": "seg_4",
        "start": 17.2,
        "text": "再縮放賽因貝塔倍，旋轉貼在右上角。",
        "rate": "+15%"
    },
    {
        "id": "seg_5",
        "start": 21.6,
        "text": "補齊外框矩形，斜邊 A F 唯 1。",
        "rate": "+18%"
    },
    {
        "id": "seg_6",
        "start": 25.5,
        "text": "由平行內錯角，角 D F A 也是阿爾法加貝塔。",
        "rate": "+18%"
    },
    {
        "id": "seg_7",
        "start": 30.0,
        "text": "觀察垂直高度：線段 A D 等於 B E 加 E C，得到正弦禾角公式。",
        "rate": "+15%"
    },
    {
        "id": "seg_8",
        "start": 36.0,
        "text": "觀察水平寬度：線段 D F 等於 A B 減 F C，扣除粉色邊，得到餘弦禾角公式。",
        "rate": "+16%"
    },
    {
        "id": "seg_9",
        "start": 43.5,
        "text": "接著推導插角公式：將貝塔結構沿著 A E 鏡像翻轉至下方。",
        "rate": "+15%"
    },
    {
        "id": "seg_10",
        "start": 50.5,
        "text": "垂直高度：線段 F prime D prime 等於 B E 減 E C prime，導出正弦插角公式。",
        "rate": "+16%"
    },
    {
        "id": "seg_11",
        "start": 57.5,
        "text": "水平寬度：線段 A D prime 等於 A B 加上 B D prime，導出餘弦插角公式。",
        "rate": "+16%"
    },
    {
        "id": "seg_12",
        "start": 64.5,
        "text": "記住口訣：正弦同號，餘弦異號。幾何投影讓公式一目了然！",
        "rate": "+12%"
    }
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TTS_DIR = os.path.join(SCRIPT_DIR, "scratch", "tts")
os.makedirs(TTS_DIR, exist_ok=True)

async def generate_segment(seg, out_p, max_retries=3):
    if os.path.exists(out_p) and os.path.getsize(out_p) > 1000:
        return
    for attempt in range(1, max_retries + 1):
        try:
            c = edge_tts.Communicate(seg["text"], voice=VOICE, rate=seg["rate"])
            await asyncio.wait_for(c.save(out_p), timeout=12.0)
            return
        except Exception as e:
            print(f"[{seg['id']}] Attempt {attempt} failed: {e}", flush=True)
            if os.path.exists(out_p):
                try: os.remove(out_p)
                except: pass
            if attempt < max_retries:
                await asyncio.sleep(1.0)
            else:
                raise

async def generate_and_check():
    print("=== Checking & Generating TTS Segments ===", flush=True)
    seg_files = []
    has_overlap = False
    for i, seg in enumerate(SEGMENTS):
        out_p = os.path.join(TTS_DIR, f"{seg['id']}.mp3")
        await generate_segment(seg, out_p)
        
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_p],
            capture_output=True, text=True, check=True
        )
        dur = float(res.stdout.strip())
        next_s = SEGMENTS[i+1]["start"] if i+1 < len(SEGMENTS) else 73.0
        end_s = seg["start"] + dur
        gap = next_s - end_s
        print(f"[{seg['id']}] start={seg['start']:.2f}s, dur={dur:.2f}s, end={end_s:.2f}s, next={next_s:.2f}s, gap={gap:.2f}s", flush=True)
        if gap < 0:
            print(f"  >>> OVERLAP WARNING: exceeds next start by {-gap:.2f}s!", flush=True)
            has_overlap = True
        seg_files.append((out_p, seg["start"]))

    if has_overlap:
        print("ERROR: One or more segments overlap!", flush=True)
        return None
    
    print("All segments validated with positive breathing gaps!", flush=True)
    return seg_files

def mix_audio(seg_files, output_audio):
    print("=== Mixing Narration Audio Track ===", flush=True)
    filter_parts = []
    inputs = []
    for i, (p, st) in enumerate(seg_files):
        inputs.extend(["-i", p])
        ms = int(round(st * 1000))
        filter_parts.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    mix_ins = "".join(f"[a{i}]" for i in range(len(seg_files)))
    filter_parts.append(f"{mix_ins}amix=inputs={len(seg_files)}:normalize=0:dropout_transition=0[aout]")
    
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filter_parts), "-map", "[aout]", output_audio]
    subprocess.run(cmd, check=True)
    print(f"Master narration audio created at: {output_audio}", flush=True)

if __name__ == "__main__":
    files = asyncio.run(generate_and_check())
    if files:
        master_audio = os.path.join(SCRIPT_DIR, "scratch", "master_narration.mp3")
        mix_audio(files, master_audio)
