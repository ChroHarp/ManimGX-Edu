# 立方和幾何動畫專案 (Sum of Cubes Geometric Animation)

本專案使用 **Manim CE** 製作經典的「立方和公式」$a^3 + b^3 = (a+b)(a^2 - ab + b^2)$ 三維空間幾何證明與剛體重排動畫，並結合 **Edge-TTS** 台灣男聲配音（`zh-TW-YunJheNeural`）、破音字發音校正（「為」讀「唯」）與 FFmpeg 毫秒級音畫同步合成。

---

## 幾何推導流程 (Geometric Derivation Steps)

```
a³ 與 b³ 並排
  ↓
從 a³ 切出 a × b × b
  ↓
把這條接到 b³
  ↓
形成 (a+b) × b × b
  ↓
回頭看 a³ 的剩餘 L 形截面
  ↓
L 形依平方差方式剛體重排
  ↓
形成 a × (a-b) × (a+b)
  ↓
兩塊轉成共同長度 a+b
  ↓
截面變成 a(a-b) + b²
  ↓
整理為 a² - ab + b²
  ↓
得到立方和公式：a³ + b³ = (a+b)(a² - ab + b²)
```

---

## 專案結構 (Project Structure)

```
SumOfCubes/
├── sum_of_cubes.py             # Manim CE 核心 3D 幾何動畫腳本
├── build_master_video.py       # 台灣男聲 Edge-TTS 生成與 FFmpeg 音畫同步管線
├── SumOfCubes_with_voice.mp4   # 最終含配音的完整教學影片
├── master_narration.mp3        # FFmpeg 精確延遲混音後的音軌
├── audio/                      # 語音切片暫存資料夾
└── README.md                   # 專案詳細說明文檔
```

---

## 執行與渲染方式 (How to Run)

### 1. 渲染 Manim 動畫
```bash
# 720p 快速預覽
manim -qm SumOfCubes/sum_of_cubes.py SumOfCubes

# 1080p60 高畫質輸出
manim -qh SumOfCubes/sum_of_cubes.py SumOfCubes
```

### 2. 合成配音與最終影片
```bash
python SumOfCubes/build_master_video.py
```
執行後會：
1. 自動調用微軟神經語音 `zh-TW-YunJheNeural` 生成各句教學旁白。
2. 自動利用 `ffprobe` 檢驗每一句旁白的長度與呼吸間隔，確保零搶音（`No Overlap`）。
3. 透過 FFmpeg `filter_complex adelay + amix` 進行無損音畫時間軸壓製，輸出 `SumOfCubes_with_voice.mp4`。
