# 直幅分鏡修改：同心圓弧與箭頭偏轉

場景：`arc_degree_vertical_turning.py` → `ArcDegreeVerticalTurning.mp4`。保留前版影片；這份場景獨立於原本的純圖形版與 F0 直幅版。

## 分鏡

1. 原有同心圓片頭，從圓心切出非直角的扇形；畫面與旁白不出現任何特定度數。
2. 留下三段同心圓弧，標示 A₁／A₂／A₃ 與 B₁／B₂／B₃。
3. 以 B 端固定，三弧同時減少曲率並保持長度，展直成平行線段，再彎回原位。原弧長比較段的字幕及 `vertical_05.wav` 音檔完整沿用。
4. 第一個箭頭沿內弧由 A₁ 到 B₁，箭頭方向始終為前進切線方向。下方圖解把起終方向放到同一頂點，以弧線標出偏轉角 δ₁。
5. 中弧與外弧的箭頭進行相同運動，得到 δ₂、δ₃，呈現三者偏轉角相等。
6. 將起終切向方向一起旋轉，使它們與兩條半徑方向對應，保留夾角；此時才引入圓心角 θ 並呈現 δ＝θ。
7. 以「圓弧度數＝箭頭偏轉角＝所對圓心角」總結，無特定角度數值。

程式中的數值只用於安排非特殊扇形的示意幾何；畫面、公式、旁白皆用一般角度符號，不將範例數值當作定義條件。

## 語音與節奏

沿用已選定的 F0 聲線：台灣雲哲來源 +12% 語速，再以 Seed-VC F0、原音高、30 steps、CFG 0.7、seed 42 轉換。只重製第 3、4、6、7、8、9 句，其餘四句直接沿用；使用者已同意不含特定度數的新旁白雲端生成。

動畫動作各自維持正常速度：展直 1.1 秒、彎回 1.1 秒、沿弧箭頭 1.5 秒。旁白尚未播完時，僅於分鏡末端停留，不拖慢動作。實際段落起訖由音檔長度決定，記錄於 `narration_turning/vertical_timeline.json`。

## 重製與檢查

1. `python ArcDegree/prepare_turning_narration.py`
2. `wsl bash ArcDegree/run_turning_colab.sh`，下載後自動關閉本次 Colab。
3. `python ArcDegree/prepare_turning_narration.py --finish`
4. `ty check ArcDegree/arc_degree_vertical_turning.py ArcDegree/narration_scene.py`
5. `manimgx inspect ArcDegree/arc_degree_vertical_turning.py ArcDegreeVerticalTurning`
6. 檢視分鏡及動作中間幀後，`manimgx render ArcDegree/arc_degree_vertical_turning.py ArcDegreeVerticalTurning --fps 60`
7. `python -m ArcDegree.verify_turning_delivery`
8. `sync_to_gdrive.ps1 -Topics ArcDegree -VideoNames ArcDegreeVerticalTurning.mp4`

`ARC_TURNING_LAYOUT_ONLY=1` 僅供配音尚未完成時檢查動作版面，借用前版音訊時長；正式影片必須使用新版配音，不能在此模式下交付。

幾何檢查涵蓋固定 B 端、展直前後長度一致、沿弧箭頭與半徑垂直、原弧長比較音檔雜湊相同。最終另驗證完整解碼、字幕及音軌時間。

## 本次交付（2026-10-28）

已輸出 1080×1920、60fps、45.633 秒的配音成品。正式分鏡 47 個抽樣與動作中間幀檢查均通過；完整解碼、10 句字幕、旁白銜接、固定 B 端與等弧長展直檢查通過。弧長比較段音檔與原版完全相同，旁白無特定度數。新版已同步至指定 Google Drive 的 `ManimGX-media/ArcDegree/ArcDegreeVerticalTurning.mp4`；Colab 已關閉。聽感仍需播放驗收。
