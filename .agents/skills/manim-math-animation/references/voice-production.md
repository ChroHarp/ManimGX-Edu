# 上片前的專屬聲線轉換

僅在使用者確認分鏡、旁白及節奏，並表示要製作上片成品後使用。前期測試、改稿、改分鏡與節奏比較，全部使用台灣中文 Edge-TTS。不要為每一輪試片啟動 Colab。

## 已選定的方向

- 流程：已確認的台灣中文 Edge-TTS 音訊 → Colab Seed-VC F0 → 最終音畫合成。
- 聲線為使用者選定的原始 F0 方向，保留低音、沙啞特色；升 2／4 半音版本已淘汰。不要額外升調或以兩人波形疊加製造混聲。
- Drama 3 的台灣口音尚未通過驗收，不作為此流程的預設替代。
- 目前 ArcDegree 來源基準：`zh-TW-YunJheNeural`、語速 `+12%`、音高 `+0Hz`。其他作品若已有使用者確認的 Edge-TTS 設定，沿用其設定，不擅自套用新語速或音高。正式轉換直接重用已驗收的來源，不重生一份節奏不同的 TTS。

## F0 設定與素材

| 設定 | 值 |
| --- | --- |
| F0 condition | true |
| Auto F0 adjust | false |
| Pitch shift | 0 |
| Seed | 42 |
| Diffusion steps | 30 |
| CFG | 0.7 |
| Timbre blend | 1.0，唯一音色目標 |

選擇紀錄位於 `D:/WebDesign/Colab-VoiceLab/experiments/taiwan-voice-20261028/selected_voice.json`；原始選定中文樣本為同資料夾的 `f0.wav`。轉換目標為 `D:/WebDesign/Colab-VoiceLab/VoiceSample/Tsuda_clean_ref.wav`；本專案已有工作副本 `ArcDegree/narration_f0/target.wav`。以選擇紀錄與檔案雜湊核對素材，不把 `f0.wav` 和實際轉換目標參考混為一談。

已記錄的後續 F0 重跑及本專案轉換固定 Seed-VC revision `51383efd921027683c89e5348211d93ff12ac2a8`。原始選定樣本沒有保存模型版本及權重雜湊，不能聲稱逐位元重現原始樣本。新批次須記錄實際 revision、權重雜湊、參考／來源雜湊及參數。

## 操作

1. 來源文字與畫面字幕分開保存；只對語音端做 O、數字與破音字讀音校正。逐句保存來源音訊、逐字稿與設定。
2. 快取識別包含文字、聲音、語速、音高、來源音訊、參考音訊、模型及轉換參數。只有上述條件相同才重用；不要只按 `vertical_03.wav` 這類檔名判斷。
3. 檢查 Colab 當前登入、工作階段與資源，不採信舊日誌餘額。依當前授權執行；既有授權涵蓋同一工作時，不反覆詢問。工具若要求新的具體授權，說明被擋的動作與原因。
4. 僅轉換新句及變更句，保留未改動音檔；一次載入模型處理本批素材。使用 task 專屬工作階段，結果下載完成或流程失敗後，關閉自己建立的工作階段，保留輸出與診斷。
5. 轉換入口可參考 `ArcDegree/convert_narration_remote.py` 與 `ArcDegree/run_turning_colab.sh`。這些是 ArcDegree 實作範例，路徑、工作階段名稱與輸出目錄必須配合當前作品調整；不要直接套用舊的 `run_seedvc_colab.py`。
6. 保留原始轉換音訊，另製作響度一致的交付副本；本次基準為 -18 LUFS、true peak -2 dB。不額外升調、拉伸時長或重度降噪來改變聲線。
7. 重新讀取實際音檔長度，調整分鏡末端停留及字幕。動畫動作維持正常速度；不要透過拉長旋轉、變形或移動來填滿旁白。
8. 執行型別、版面與動作中間幀檢查，再渲染；確認完整解碼、字幕齊全、音軌無重疊且末句播完。檔案檢查不能取代實聽，不據此宣稱台灣口音、無雙聲感或聲線品質已驗收。
9. 保留前版試片，依本次主題與檔名限定 Google Drive 同步範圍，並核對副本。不要由上片成品製作推論獲得發布或推送程式碼的授權。

## 可參考的既有實作

- `ArcDegree/narration_scene.py`：語音與動畫並行、分鏡末端等待；可指定作品音訊及時間軸目錄。
- `ArcDegree/prepare_turning_narration.py`：只改六句、其餘四句直接重用的範例；它只用檔案存在判斷來源快取，跨改稿重用前須補上上述完整快取識別，不能盲目重跑。
- `ArcDegree/verify_turning_delivery.py`：音畫與字幕檢查、指定段落音檔雜湊保持一致。
- `ArcDegree/VERTICAL_TURNING.md`：本次分鏡與交付紀錄，不取代專案的兩階段規則。
