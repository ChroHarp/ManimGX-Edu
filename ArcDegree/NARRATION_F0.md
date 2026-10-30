# ArcDegree 選定 F0 聲線配音

後續直幅分鏡更新另見 `VERTICAL_TURNING.md`，新版成品為 `ArcDegreeVerticalTurning.mp4`；這份文件以下記錄最初的 F0 版本。

## 聲線與來源

依「建立台灣中文新聲線基準」聊天及 Colab-VoiceLab 的 `selected_voice.json`，採用原始 F0 方向：保留低音、沙啞特色，不使用已淘汰的升 2／4 半音版本。Drama 3 的台灣口音尚未通過使用者驗收，本次採台灣中文 TTS → Seed-VC F0。

旁白來自原版 `ArcDegreeLandscape.srt`（12 句）與 `ArcDegreeVertical.srt`（10 句）。顯示文字保留，語音端將 O、90 度及必要破音字改成口語發音。Microsoft Edge-TTS 雲哲、語速 +12%、音高 +0 Hz；使用者已明確同意雲端處理。

Seed-VC：F0=true、auto_f0_adjust=false、pitch_shift=0、seed=42、30 steps、CFG=0.7、timbre_blend=1.0，沿用 Tsuda_clean_ref.wav 為唯一音色目標，不疊加兩人波形。固定 Seed-VC revision `51383efd921027683c89e5348211d93ff12ac2a8`，對應後續已記錄的 F0 重跑版本；原始選定基準沒有模型版本紀錄，不能宣稱逐位元重現原始聲線。

## 時間安排

兩份 `_f0.py` 保留原版所有 `self.play` 呼叫與速度。`build_narrated_scenes.py` 以語法結構比對確認直幅 13 段、橫幅 21 段動畫呼叫皆未改動。每句旁白在對應分鏡開始時播放，只在分鏡結束且語音尚未播完時補上停留；不拉長動畫動作。字幕依實際語音長度另行輸出，原版字幕與影片保留。

## 執行順序

1. `python ArcDegree/prepare_narration.py`：生成語速 +12% 的來源音訊及 manifest、上傳封裝。
2. 檢查 Colab status / usage，建立本次專用 T4 session；`setup_narration_remote.py` 安裝依賴，`warm_narration_remote.py` 可預先載入模型。
3. 在 WSL 執行 `bash ArcDegree/run_narration_colab.sh`：上傳、轉換、下載，EXIT trap 關閉本次 session。程式直接使用新入口，不使用舊的 `run_seedvc_colab.py`。
4. `python ArcDegree/finish_narration.py`：確認 22 句齊全，製作響度調整副本，保留原始轉換檔。音訊只調整音量，不做升調、時間拉伸或降噪。
5. `python ArcDegree/build_narrated_scenes.py`，依專案流程先 `ty check`、`manimgx inspect`，檢視分鏡後正式渲染兩份 `_f0.py`。
6. 執行專案 `sync_to_gdrive.ps1 -Topics ArcDegree -VideoNames ArcDegreeLandscapeF0.mp4,ArcDegreeVerticalF0.mp4`，只同步本次兩個成品到 Google Drive。

## 產物與品質界線

音訊與執行記錄在 `narration_f0/`：`source_rate12/`、`converted/`、`final/`、`manifest.json`，以及 `converted/conversion.json` 的模型、權重雜湊、GPU、套件與參數。此目錄是本機媒體工作資料，不納入 Git。

最終成品名稱為 `ArcDegreeLandscapeF0.mp4` 與 `ArcDegreeVerticalF0.mp4`，原檔保留。檔案與音畫時長檢查不能代替實聽；台灣口音、沙啞感、單人感與咬字仍需使用者播放驗收。

## 本次完成紀錄（2026-10-28）

兩版皆已渲染、完整解碼檢查通過，1920×1080 橫幅 53.217 秒／1080×1920 直幅 47.367 秒，皆 60fps、H.264 + AAC。12／10 句字幕齊全，旁白時間區間無重疊，影片結尾涵蓋完整音軌；響度調整後的旁白峰值約 -2 dBFS。版面檢查橫幅 47 個／直幅 43 個抽樣皆無問題。

Colab session `arcdegreef020261028` 已下載結果並關閉。兩個新影片已複製至 `G:\我的雲端硬碟\數學教學\ManimGX-media\ArcDegree`。同步工具新增可選的主題與檔名篩選，這次只處理兩個新影片。
