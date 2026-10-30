# 等長圓弧與圓心角：明亮背景試片

場景 `equal_length_arc_angles.py`，本次輸出 `EqualLengthArcAnglesLight.mp4`。依使用者後續要求，改成明亮背景，加入 Edge-TTS 雲哲配音；不使用 Colab 或專屬聲線轉換。最初的無配音版本保留在 `EqualLengthArcAngles.mp4`。

六段分鏡：等長線段 a、b、c → 保持長度彎成不同半徑的圓弧，對齊起點與切向證明無法完全疊合 → 箭頭沿 a 移動、量出偏轉 → 畫出 a 的圓心與半徑，將偏轉角與圓心角對應 → 同步在 b、c 重複 → 固定各自半徑，先移到共同圓心，再調整張角至相同。

在三弧比較完成（原無聲版約 0:22）後，新增獨立置中的結論分鏡：「一個圓弧除了長度以外，還可以測量角度，其角度就是所對的圓心角」。配音版依實際句長安排停留，所以秒數會與原版不同。底部說明向上移約 0.75em（畫面邊距由 0.85 增加至 1.23），並將此偏好寫入專案 AGENTS.md。

前五段保持等長，角度因半徑不同而異；最後調整張角時，長度不再保持相同，畫面明示這項變化。最終結論限定為「同心圓中，對應同一圓心角的圓弧，角度相同」，不宣稱所有同心圓弧必然同角。畫面不指定特殊角度數值。

彎曲使用固定弧長的曲率插值，並非把線段任意縮放成圓弧。沿弧箭頭的位置與方向依相同參數計算，方向始終與半徑垂直。偏轉角與圓心角的方向對照，透過同時旋轉起終方向呈現。

配音先執行 `python ArcDegree/prepare_equal_edge_narration.py`：10 句旁白，`zh-TW-YunJheNeural`、語速 +12%、音高 +0Hz，依文字與設定雜湊快取。聲音與顯示文字分開保存，正常速度動畫與音訊並行，只在段落末端補上語音尚餘時間。

驗證：`ty check ArcDegree/equal_length_arc_angles.py`、完整 `manimgx inspect` 與動作中途抽樣，再用 `manimgx render ArcDegree/equal_length_arc_angles.py EqualLengthArcAngles --fps 60 -o ArcDegree/EqualLengthArcAnglesLight.mp4` 輸出；執行 `python -m ArcDegree.verify_equal_length_arcs` 檢查等長彎曲、切向方向、完整解碼、1080×1920／60fps、10 句字幕與音訊銜接。原無聲成品可用 `--silent` 選項驗證。

同步僅針對本次影片：`sync_to_gdrive.ps1 -Topics ArcDegree -VideoNames EqualLengthArcAnglesLight.mp4`。

原無聲版為 32.367 秒、1080×1920／60fps，37 個版面抽樣與 6 個動作中間幀檢查通過，已同步至指定 Google Drive。

本次明亮配音版已完成：63.650 秒、1080×1920／60fps、H.264 + AAC；10 段 Edge-TTS 旁白與字幕齊全，無音軌重疊或尾句截斷，完整解碼通過。52 個版面抽樣檢查通過，結論分鏡約 36.54–44.32 秒。影片已同步至指定 Google Drive，未使用 Colab。

後續結論版面調整：字卡下移，上方加入單一圓弧、兩條半徑、圓心及同為 θ 的角度標記，標明「圓弧角度＝圓心角」。字幕檔、完整時間軸及影片解碼後音訊均已與調整前比對，完全一致；僅變更該段畫面。
