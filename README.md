# 🤖 AI 服務建議書生成器 (Gemini 版本)

python -m venv venv
# 啟動虛擬環境
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

本專案支援：
- ✅ **範本學習**：讀取 Word/PDF 格式的現有建議書作為範本
- ✅ **智慧分析**：自動分析範本結構和章節內容
- ✅ **AI 改寫**：使用 Google Gemini AI 根據新需求改寫內容
- ✅ **互動介面**：Streamlit 視覺化操作介面
- ✅ **多格式輸出**：生成專業 Word 格式建議書
- ✅ **錯誤處理**：智慧處理 API 額度問題

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
## 進階整合 Google Drive
如需串接Google Drive自動抓範本、自動上傳：
1. 申請service account並下載 credentials.json 放在專案目錄
2. 改 main.py 及 drive_utils.py（參照前述demo或洽詢協助）
3. 於main.py串流下載、分析docx格式並將AI產出自動上傳

建議試跑本地，不需API key即可工作（如有Gemini API Key自動串接AI，不填則用假內容）。
