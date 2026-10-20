---
name: manim-math-animation
description: 指導 ManimGX (Rust + wgpu 核心，相容 Manim CE API) 幾何與數學動畫製作、2D 版面自動檢查 (manimgx inspect)、靜態型別檢查 (ty check)、3D 空間幾何拆解、螢幕固定圖層（字幕與公式）、台灣男聲配音（Edge-TTS 雲哲 + self.say 自動同步）、數學破音字校正，以及「程式放 GitHub、成品影片同步 Google Drive (方案 B)」的完整工作流程與風格規範。
---

# ManimGX 數學幾何動畫與配音自動同步規範 (ManimGX Math Animation Skill)

本技能定義了以 **ManimGX (`academa-labs/manimgx`)** 為核心引擎，製作高品質 3D/2D 幾何數學教學動畫、台灣男聲旁白配音（`edge-tts`）、破音字發音自動校正、雙軌雲端儲存架構，以及「靜態型別檢查 $\to$ 版面自動檢查 $\to$ GPU 極速渲染 $\to$ 雲端雙軌同步」的完整設計原則與代碼架構規範。

---

## 0. 標準化 4+1 步極速工作流程 (Agentic 5-Step Loop)

在開發或修改任何數學動畫時，**嚴禁盲目直接算圖或手動推算旁白秒數**，必須嚴格遵循以下標準閉環：

1. **撰寫腳本 (Author)**：
   * 統一匯入 `import manimgx as m`（或繼承專案根目錄 `manimgx_tw_helper.py` 中的 `TWScene` / `TWThreeDScene`）。
   * **禁止使用** `import manim` 或 `config.no_latex_cleanup = True`（ManimGX 內建 Typst 數學排版與原生 x264 編碼，無 LaTeX 暫存鎖定問題）。
   * 優先使用 `self.say("旁白台詞...", anim1, anim2)` 讓動畫自動跟隨語音時長同步，徹底淘汰手動硬編碼 `start` 秒數的外部 FFmpeg 腳本。
2. **靜態型別檢查 (Type Check)**：
   * 執行 `ty check <scene_file.py>`。
   * 必須確保 **0 錯誤 (`All checks passed!`)**，在 0.1 秒內排除未定義變數、拼錯的關鍵字參數或 `.animate` 鏈型別錯誤。
3. **版面與分鏡自動檢查 (Inspect & Storyboard)**：
   * 執行 `manimgx inspect <scene_file.py>`（或針對特定秒數 `manimgx inspect <scene_file.py> -t 5.0,12.5,end`）。
   * ManimGX 會在不編碼影片的情況下極速抽樣所有 `play` / `wait` 結束畫面，輸出 `<Scene>.storyboard.png` 分鏡表，並在 2D 場景自動檢測：
     * **文字重疊 (`texts overlap`)**
     * **線條或色塊壓過文字 (`line/fill over text`)**
     * **物件超出畫面邊界 (`past the edge`)**
     * **字體過小 (`small label`)**
   * 檢視輸出的 `*.storyboard.png` 分鏡圖，若 `manimgx inspect` 回傳 `exit code 1`，必須根據紅框編號與行號修正座標後再次 `inspect`，直到版面清晰無誤。
4. **GPU 極速渲染交付 (Render)**：
   * 草稿快速驗證：`manimgx render <scene_file.py> -r 1280x720 --fps 30`
   * 正式成品輸出：`manimgx render <scene_file.py>`（預設輸出 1920×1080 @ 60fps MP4，並自動混入 `self.say` 音軌與產出 `.srt` 字幕）。
   * 直式短影音 (9:16)：`manimgx render <scene_file.py> -r 1080x1920`（ManimGX 直式預設寬 8 × 高 14.2 單位；若移植舊版 9×16 座標腳本，可在開頭設定 `m.config.frame_height = 16.0`）。
5. **雲端雙軌同步交付 (Sync & Backup - 方案 B)**：
   * 渲染完成後，執行 `powershell -ExecutionPolicy Bypass -File .\sync_to_gdrive.ps1`，將各主題目錄下的最終 `.mp4` 增量備份至 Google Drive（`ManimGX-media` 資料夾）。
   * 執行 `git add .` 與 `git commit` 將程式碼與設定推送到 GitHub（因 `.gitignore` 已配置，不會夾帶任何大型影片與暫存切片）。

---

## 1. 核心視覺風格與動畫設計原則 (Animation Aesthetics & Principles)

### 1.1 3B1B 式啟發性步進推導
* **拒絕一蹴而就**：數學證明與公式推導必須「按步就班、循序漸進」，物件到位後才出現對應式子。
* **變換保留結構**：公式或幾何體變換時，使用 `m.ReplacementTransform` 或 `m.TransformMatchingTex` 平滑過渡對應部分，輔以色塊或文字位移（如由底面積逐步推進至 $(a-b)(a^2+ab+b^2)$，再補齊左側等號與外框）。
* **重點醒目框選**：最終結論公式使用 `m.SurroundingRectangle(buff=0.2, color=m.YELLOW)` 進行高亮收尾。

### 1.2 螢幕固定圖層 (HUD Layer) 與 3D 物件分層規範
在 `TWThreeDScene`（或 `m.ThreeDScene`）中，必須嚴格區分「螢幕固定 2D 物件」與「空間 3D 物件」：
1. **底部字幕 (Captions)**：
   * 統一固定在螢幕二維層：`self.camera.add_fixed_in_frame_mobjects(group)`，放置於 `to_edge(m.DOWN, buff=0.45)`。
   * **關鍵防坑**：在 ManimGX 中，`self.add_fixed_in_frame_mobjects(mob)` 會同時呼叫 `self.add(mob)` 導致物件立即顯示；若要在 `self.play(m.FadeIn(group))` 時才淡入，必須呼叫 **`self.camera.add_fixed_in_frame_mobjects(group)`**（已封裝於 `TWThreeDScene.make_caption` 與 `make_top_formula`）。
2. **頂部動態公式 (Top Formula)**：
   * 同樣透過 `self.camera.add_fixed_in_frame_mobjects(obj)` 固定在二維層，位於 `to_edge(m.UP, buff=0.45)`，預設使用 `m.YELLOW`。
3. **空間標籤 (3D World Billboard Labels)**：
   * 標註在 3D 幾何體上的文字/公式（如 $a^3$、$b^3$、$a^2$、$ab$、$a-b$），必須使用 `TWThreeDScene` 提供的 **`self.add_fixed_orientation_mobjects(mobj)`**（利用 ManimGX 相機旋轉矩陣 `rotation(phi, theta, gamma).T` 動態對齊鏡頭），確保相機旋轉時文字永遠正對觀眾，不產生傾斜變形。
   * 在鏡頭切換（如正視角切換至俯視角）前，必須將不再適用的前視標籤與輔助標線即時 `FadeOut` 收淨。

### 1.3 空間拆解與剛體動線規範 (Rigid Body Motion & Collision-Free Path)
* **幾何銜接無縫切換**：在挖除/拆分幾何體時（例如 $a^3$ 挖去 $b^3$），應預先建構好拆分後的三個長方體（`carved_A`），在挖除塊抽離前透過 `FadeOut(cube_A)` 與 `FadeIn(carved_A)` 同步替換，外觀完全一致無破綻。
* **平行不交錯動線**：
  1. **預先規劃錨點**：預先計算最終攤平排齊的座標軸（如 `left_edge`、間距 `gap`、中心點 `final_pos1, final_pos2, final_pos3`）。
  2. **分階段剛體位移**：先沿各自專屬軸向往外脫離 $\to$ 使用 `m.Rotate` 原地剛體翻轉 $\to$ 平行滑入最終目標錨點。

---

## 2. 配音規格與發音校正規範 (TTS & Pronunciation Protocol)

### 2.1 原生 `YunJheVoice` 語音引擎與快取機制
* **TTS 引擎**：採用 `manimgx_tw_helper.py` 中的 `YunJheVoice`（底層串接微軟神經網絡語音 `edge-tts`，預設台灣男聲 **`zh-TW-YunJheNeural`**，語速預設 `+15%`）。
* **自動雜湊快取**：ManimGX 會自動將 `self.say()` 合成的音檔與單詞時間軸儲存在場景檔案旁的 `voice/` 目錄下。只要台詞未改動，重複渲染時完全離線零延遲讀取。

### 2.2 數學破音字自動校正與字幕分離原則 (Heteronyms Handling)
`YunJheVoice` 內建 `fix_tw_heteronyms()`，會在**送入 `edge-tts` 的最後一刻**自動執行同音異字替換，因此**在撰寫 `self.say("...")` 時，請直接書寫標準正體中文字**（確保畫面與 `.srt` 字幕為正統漢字，而語音自動讀出正確二聲/一聲）：
1. **「為」字自動校正（陽平二聲 `wéi`）**：
   * 凡「邊長為」、「體積為」、「面積為」、「長度為」、「斜邊為」、「夾角為」、「為骨架」或「為 + 數字/代號」，引擎內部自動轉為「**唯**」送入 TTS。
2. **「和」與「差」字自動校正**：
   * 凡「立方和」、「平方和」、「總和」、「和角」，引擎內部自動轉為「**核 / 禾**」（二聲 `hé`）。
   * 凡「差角」，引擎內部自動轉為「**插角**」（一聲 `chā`）。
3. **數學符號口語念法慣例**：
   * `self.say()` 的文稿請寫成自然口語讀音，例如：
     * $a^3 - b^3$：寫作 `"a 三方減 b 三方"`
     * $(a-b)(a^2+ab+b^2)$：寫作 `"a 減 b，乘上 a 平方加 a b 加 b 平方"`
   * 若需在單句 `self.say()` 中使用 `[...]` 括號對齊多個局部動畫，請在中文括號前後保留空格（如 `"先考慮 [邊長為 a] 的 [正方體]"`），以利分詞時間軸精確對位。

---

## 3. 雲端雙軌架構規範 (Cloud Sync & Backup Standard - 方案 B)

為了避免雲端硬碟（如 Google Drive）背景同步鎖死虛擬環境與渲染碎片，並確保 GitHub 儲存庫保持輕量，專案採用嚴格分離機制：

1. **工作目錄永遠維持在本地硬碟**（例如 `D:\WebDesign\ManimCEAnimate`），確保 Agent 與編譯器享有原生 NVMe/SSD 讀寫性能。
2. **`.gitignore` 嚴格把關**：
   * 永久排除 `media/`、`*.mp4`、`partial_movie_files/`、`Tex/`、`tts/`、`scratch/`、`*.mp3`。
   * GitHub 只儲存 `.py`、`.md`、`.toml`、`.ps1` 等純文字代碼與設定，倉庫體積控制在數 MB 以內。
3. **自動增量同步至 Google Drive**：
   * 透過專案根目錄的 `sync_to_gdrive.ps1`，自動搜尋掛載的 Google Drive 上的 `ManimGX-media` 資料夾（如 `G:\我的雲端硬碟\數學教學\ManimGX-media`）。
   * 只針對最終生成的 `.mp4` 影片進行增量備份，自動依主題建立對應目錄，不拷貝無用的分段切片暫存。

---

## 4. 專案標準代碼模板 (Reference Templates)

### 4.1 2D 幾何推導標準模板 (`TWScene`)
```python
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import manimgx as m
import numpy as np
from manimgx_tw_helper import TWScene, YunJheVoice


class GeometryConcept2D(TWScene):
    voice = YunJheVoice(rate="+15%")

    def construct(self) -> None:
        cap1 = self.make_caption("先考慮直角三角形，斜邊長為", ("math", "1"))
        tri = m.Polygon([-2, -1, 0], [2, -1, 0], [2, 1.5, 0], color=m.BLUE, fill_opacity=0.4)

        self.say(
            "先考慮一個斜邊長為 1 的直角三角形。",
            m.FadeIn(cap1, shift=m.UP * 0.08),
            m.Create(tri, run_time=1.2),
        )
        self.wait(0.5)
```

### 4.2 3D 空間幾何拆解標準模板 (`TWThreeDScene`)
```python
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import manimgx as m
import numpy as np
from manimgx_tw_helper import TWThreeDScene, YunJheVoice


class GeometryConcept3D(TWThreeDScene):
    voice = YunJheVoice(rate="+15%")

    def construct(self) -> None:
        self.set_camera_orientation(phi=65 * m.DEGREES, theta=-45 * m.DEGREES, zoom=0.92)

        cap1 = self.make_caption("先考慮一個邊長為", r"a", "的正方體")
        top_formula = self.make_top_formula(r"a^3", scale=1.05)
        cube = m.Cube(side_length=3.0, fill_color=m.BLUE_D, fill_opacity=0.5, stroke_color=m.BLUE_E, stroke_width=2)

        lbl = m.MathTex(r"a^3").move_to([0, 0, 2.2])
        self.add_fixed_orientation_mobjects(lbl)

        self.say(
            "先考慮一個邊長為 a 的正方體，體積為 a 三方。",
            m.FadeIn(cap1),
            m.FadeIn(top_formula),
            m.DrawBorderThenFill(cube, run_time=1.5),
            m.FadeIn(lbl),
        )
        self.wait(1.0)
```
