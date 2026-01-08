# 🤖 AI 服務建議書生成器 (Gemini 版本)

python -m venv venv
# 啟動虛擬環境
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

本專案支援：
- ✅ **範本學習**：讀取 Word/PDF 格式的現有建議書作為範本
- ✅ **標題階層識別**：精確讀取 Word 文件的 Heading 1, Heading 2, Heading 3 等標準樣式
- ✅ **H1 H2 標題過濾**：自動過濾掉 H3 及以下的細項標題，只使用主要標題作為目錄
- ✅ **原始標題保留**：完全遵照範本文件的 H1 和 H2 標題順序和名稱
- ✅ **格式複製**：自動複製範本文件的字體樣式、格式設置
- ✅ **智慧分析**：自動分析範本結構，提供詳細的標題階層報告
- ✅ **AI 內容改寫**：使用 Google Gemini AI 根據新需求改寫內容，保持原有標題
- ✅ **專業輸出**：生成包含目錄、頁碼、正確階層的 Word 專業文檔
- ✅ **互動介面**：Streamlit 視覺化操作介面，顯示原始標題順序
- ✅ **錯誤處理**：智慧處理 API 額度問題，自動降級到模擬模式
- ✅ **Google Drive RAG**：從 Google Drive 搜尋歷史服務建議書作為 AI 寫作參考
- ✅ **智慧搜尋**：按客戶類型和應用類型自動找到相關的成功案例
- ✅ **內容參考**：AI 學習歷史建議書的專業寫作風格和內容結構

## 使用方式

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 設定 Google AI API Key (選用)
```bash
# PowerShell
$env:GOOGLE_API_KEY="您的Google_AI_API金鑰"

# 或直接在程式中輸入測試
python test_gemini.py
```

```bash
python check_quota.py
```

### 3. 運行互動網頁介面
```bash
python -m streamlit run main.py
```

### 4. 在瀏覽器輸入需求、產生並下載docx建議書

---
## ⚠️ 免費額度說明

- **Google Gemini AI 提供免費額度**：適合測試和輕度使用
- **額度用完時**：系統會自動切換到模擬模式，仍可正常生成建議書
- **升級付費方案**：前往 [Google AI Studio](https://aistudio.google.com/) 升級以獲得更多額度

---
## 🔗 Google Drive RAG 參考資料庫

### 什麼是 RAG？
RAG (Retrieval-Augmented Generation) 讓 AI 在生成內容時，可以參考相關的歷史資料作為知識庫，提升生成內容的專業性和準確性。

### 功能特色
- 🔍 **智慧搜尋**：根據客戶類型和應用類型自動搜尋相關的服務建議書
- 📚 **內容學習**：AI 會學習歷史成功案例的寫作風格和內容結構
- 🎯 **精準參考**：只參考高度相關的檔案，避免內容混亂
- 🚀 **提升品質**：生成的建議書更符合業界標準和客戶期望

### 快速開始
1. **設定 Google Drive API**：
   ```bash
   # 參考詳細設置指南
   cat GOOGLE_DRIVE_SETUP.md
   ```

2. **測試連線**：
   ```bash
   python test_drive_rag.py
   ```

3. **啟動應用程式**：
   ```bash
   streamlit run main.py
   ```

4. **使用 RAG 功能**：
   - 勾選 "啟用 Google Drive RAG 資料庫"
   - 輸入搜尋條件
   - 點擊 "搜尋相關建議書"
   - 生成建議書時 AI 會自動參考這些資料

### 檔案組織建議
在 Google Drive 中這樣組織您的服務建議書：
```
我的雲端硬碟/
├── 服務建議書/
│   ├── ABC公司/
│   │   ├── ABC公司_AI_建議書.docx
│   │   └── ABC公司_CRM_建議書.pdf
│   └── XYZ科技/
│       └── XYZ科技_系統整合_建議書.docx
```

### 搜尋邏輯
- **檔案類型**：只搜尋 .docx 和 .pdf 檔案
- **關鍵字匹配**：檔案名稱包含 "建議書"、"提案" 等關鍵字
- **客戶過濾**：檔案名稱包含客戶相關關鍵字
- **應用過濾**：檔案名稱包含應用類型關鍵字
- **排序**：按修改時間降序（最新的優先）

---
## ⚠️ 免費額度說明

- **Google Gemini AI 提供免費額度**：適合測試和輕度使用
- **額度用完時**：系統會自動切換到模擬模式，仍可正常生成建議書
- **升級付費方案**：前往 [Google AI Studio](https://aistudio.google.com/) 升級以獲得更多額度

---
## 📚 完整說明文件

- **[Google Drive 設置指南](GOOGLE_DRIVE_SETUP.md)** - 詳細的 API 設置步驟
- **[Word 範本準備指南](WORD_TEMPLATE_GUIDE.md)** - 如何準備最適合的範本檔案

建議先試跑本地功能，不需 API key 即可工作（如有 Gemini API Key 會自動啟用 AI 功能）。
