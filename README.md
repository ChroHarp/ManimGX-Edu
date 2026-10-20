# ManimCEAnimate (ManimGX 數學幾何動畫專案)

基於 **ManimGX (`academa-labs/manimgx`)** 打造的高品質 2D / 3D 數學幾何動畫與教學短影音創作庫。結合微軟神經網絡語音（Edge-TTS 台灣男聲「雲哲」）與破音字自動校正，實現「旁白與動畫自動同步、純淨程式碼 Git 託管、成品影片雲端備份」的現代化工作流。

---

## 專案核心特點

1. **極速渲染與原生排版**：採用 ManimGX（Rust + wgpu 核心），免除繁重的 LaTeX 暫存與環境鎖定，支援 Typst 極速數學排版與 GPU 加速渲染。
2. **語音動畫自動同步 (`self.say`)**：無需手動用外部 FFmpeg 硬編碼時間軸，動畫動作自動契合語音時長。
3. **台灣男聲口語校正**：內建 `manimgx_tw_helper.py`，自動校正數學破音字（如「為 wéi」、「和 hé」、「差 chā」）。
4. **雲端雙軌架構（方案 B）**：
   * **程式碼與設定 $\to$ GitHub**：完全排除大體積二進位檔，秒級推拉，乾淨輕量。
   * **渲染成品影片 $\to$ Google Drive**：影片一鍵增量備份至 `ManimGX-media`，避免本機空間被擠爆與 Google Drive 檔案鎖定卡死問題。

---

## 專案結構

```
ManimCEAnimate/
├── .agents/skills/             # Agent 規範與專業技能庫 (manim-math-animation)
├── .gitignore                  # 忽略 media/, *.mp4, tts/, 暫存與虛擬環境
├── manimgx_tw_helper.py        # 台灣配音輔助模組 (TWScene, TWThreeDScene, YunJheVoice)
├── sync_to_gdrive.ps1          # 方案 B：一鍵增量同步完成影片至 Google Drive
├── AngleSumDifference/         # 和差角公式幾何推導 (橫式 16:9 & 直式 9:16)
├── DifferenceOfCubes/          # 立方差公式 3D 剛體幾何拆解證明
├── LawOfCosines/               # 餘弦定理幾何拼圖證明
├── PtolemyTheorem/             # 托勒密定理動畫推導
├── QuantumDoubleSlit/          # 量子雙狹縫干涉物理動畫
└── SumOfCubes/                 # 立方和公式 3D 幾何拆解推導
```

---

## 極速開發 4 步工作流

在專案目錄下進行動畫開發時，請遵循標準 4 步循環：

### 1. 撰寫腳本
引用 `manimgx_tw_helper.py` 中的 `TWScene` 或 `TWThreeDScene`：
```python
import manimgx as m
from manimgx_tw_helper import TWScene, YunJheVoice

class MyScene(TWScene):
    voice = YunJheVoice(rate="+15%")
    def construct(self):
        self.say("我們先考慮一個直角三角形...", m.Create(...))
```

### 2. 靜態型別檢查 (0.1 秒抓錯)
```powershell
ty check <scene_file.py>
```

### 3. 版面與分鏡自動檢查 (免編碼極速診斷)
```powershell
manimgx inspect <scene_file.py>
```
自動輸出 `<Scene>.storyboard.png`，並檢查是否有文字重疊、色塊壓字、超出邊界或字體過小。

### 4. GPU 極速渲染
* **720p 快速預覽**：
  ```powershell
  manimgx render <scene_file.py> -r 1280x720 --fps 30
  ```
* **1080p 60fps 正式輸出**：
  ```powershell
  manimgx render <scene_file.py>
  ```
* **9:16 直式短影音**：
  ```powershell
  manimgx render <scene_file.py> -r 1080x1920
  ```

---

## 雲端備份與儲存管理（方案 B）

本專案將**程式碼庫**與**媒體成品**徹底解耦：

### 1. 影片備份至 Google Drive
當渲染出新的 `.mp4` 成品後，執行專屬 PowerShell 腳本：
```powershell
.\sync_to_gdrive.ps1
```
* **自動定位**：自動尋找掛載的 Google Drive 上的 `ManimGX-media` 資料夾（如 `G:\我的雲端硬碟\數學教學\ManimGX-media`）。
* **智慧增量**：只同步新增或有修改的最終 `.mp4` 檔案，自動略過數以萬計的 `partial_movie_files` 切片暫存。

### 2. 程式碼推送到 GitHub
由於 `.gitignore` 已嚴密過濾所有媒體與中間暫存檔，整個程式碼儲存庫僅幾百 KB：
```powershell
git add .
git commit -m "feat: updates and improvements"
git push
```
