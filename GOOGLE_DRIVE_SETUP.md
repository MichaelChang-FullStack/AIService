# 🔗 Google Drive API 設置指南

本指南將幫助您設定 Google Drive API，讓 AI 可以從您的 Google Drive 搜尋服務建議書作為 RAG 參考資料庫。

## 📋 前置準備

### 1. 建立 Google Cloud Project
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 記下您的專案 ID

### 2. 啟用 Google Drive API
1. 在 Google Cloud Console 中，進入 **"API 和服務" > "程式庫"**
2. 搜尋 "Google Drive API"
3. 點擊 **"啟用"**

### 3. 建立 OAuth 2.0 認證資訊
1. 進入 **"API 和服務" > "認證"**
2. 點擊 **"建立認證資訊" > "OAuth 2.0 用戶端 ID"**
3. 應用程式類型選擇 **"桌面應用程式"**
4. 設定名稱（例如：AI 建議書生成器）
5. 下載認證檔案，重新命名為 `credentials.json`

### 4. 設定 OAuth 同意畫面
1. 在認證頁面中，點擊 **"OAuth 同意畫面"**
2. 選擇 **"外部"** 用戶類型
3. 填寫應用程式資訊：
   - 應用程式名稱：AI 服務建議書生成器
   - 使用者支援電子郵件：您的電子郵件
   - 開發者聯絡資訊：您的電子郵件
4. 儲存並繼續

## 📁 檔案放置

1. 將下載的 `credentials.json` 檔案放置在專案目錄中：
   ```
   proposal_generator_demo/
   ├── credentials.json  ← 放置在此
   ├── main.py
   ├── drive_utils.py
   └── ...
   ```

## 🗂️ Google Drive 檔案組織建議

為了讓搜尋更準確，建議您在 Google Drive 中這樣組織檔案：

### 資料夾結構建議
```
我的雲端硬碟/
├── 服務建議書/
│   ├── 客戶A/
│   │   ├── A公司_AI_建議書.docx
│   │   └── A公司_系統整合_建議書.pdf
│   ├── 客戶B/
│   │   ├── B公司_CRM_建議書.docx
│   │   └── B公司_數據分析_建議書.docx
│   └── 客戶C/
│       └── C公司_網站開發_建議書.docx
```

### 檔案命名規則
建議使用以下命名格式：
- `{客戶名稱}_{應用類型}_建議書.{副檔名}`
- 例如：
  - `ABC公司_AI_建議書.docx`
  - `XYZ科技_CRM_建議書.pdf`
  - `123企業_系統整合_建議書.docx`

## 🚀 使用方式

### 1. 首次使用認證
當您第一次啟用 Google Drive RAG 功能時：
1. 系統會自動開啟瀏覽器進行認證
2. 選擇您的 Google 帳號
3. 點擊 **"允許"** 授權應用程式存取您的 Google Drive
4. 認證完成後，系統會儲存認證資訊（`token.json`）

### 2. 在應用程式中使用
1. 啟動 Streamlit 應用程式：
   ```bash
   streamlit run main.py
   ```

2. 在 **"Google Drive RAG 參考資料庫"** 區塊：
   - 勾選 **"啟用 Google Drive RAG 資料庫"**
   - 輸入搜尋關鍵字（客戶類型）
   - 選擇應用類型
   - 點擊 **"搜尋相關建議書"**

3. 系統會自動：
   - 搜尋相關的服務建議書
   - 下載並分析檔案內容
   - 建立 RAG 參考資料庫

4. 生成建議書時，AI 會參考這些歷史建議書的寫作風格和內容結構

## 🔍 搜尋邏輯

系統使用以下條件搜尋相關檔案：

### 檔案類型過濾
- 只搜尋 `.docx` 和 `.pdf` 檔案

### 關鍵字過濾
- 檔案名稱包含：建議書、提案、proposal、服務、方案
- 客戶類型：檔案名稱包含輸入的客戶關鍵字
- 應用類型：檔案名稱包含選擇的應用類型

### 排序規則
- 按修改時間降序排列（最新的檔案優先）

## ⚠️ 重要注意事項

### 安全性
- `credentials.json` 和 `token.json` 檔案請勿分享給他人
- 這些檔案包含您的 Google Drive 存取權限

### 權限範圍
- 應用程式只會**讀取**您的 Google Drive 檔案
- 不會修改或刪除任何檔案
- 只會存取檔案名稱和內容，不會存取其他個人資訊

### API 限制
- Google Drive API 有每日配額限制
- 如果遇到配額問題，請稍後再試或升級 Google Cloud 方案

### 檔案大小限制
- 單一檔案大小限制為 10MB
- 建議將大型檔案分成多個小檔案

## 🛠️ 疑難排解

### 認證失敗
```
❌ Google Drive 認證失敗: [Errno 2] No such file or directory: 'credentials.json'
```
**解決方案**：
- 確認 `credentials.json` 檔案已放置在專案目錄中

### 權限錯誤
```
❌ Google Drive 認證失敗: Access blocked: This app's request is invalid
```
**解決方案**：
- 確認 OAuth 同意畫面已正確設定
- 確認應用程式已發佈（Publishing status）

### 搜尋無結果
```
⚠️ 未找到相關的服務建議書檔案
```
**解決方案**：
- 檢查檔案命名是否符合規則
- 確認檔案放置在可存取的資料夾中
- 調整搜尋關鍵字

## 📞 技術支援

如果您在設定過程中遇到問題，請檢查：
1. Google Cloud Console 的設定
2. 檔案放置位置
3. 網路連線狀況
4. Google Drive 檔案權限

設定完成後，您就可以享受 AI 參考歷史成功案例來生成更專業的服務建議書了！🎉
