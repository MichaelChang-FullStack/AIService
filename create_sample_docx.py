#!/usr/bin/env python3
"""
創建範例 Word 文檔來測試標題階層功能
"""
from docx import Document
from docx.shared import Inches
from docx.enum.style import WD_STYLE_TYPE

def create_sample_proposal():
    """創建一個範例服務建議書，包含不同等級的標題"""

    doc = Document()

    # 設定標題樣式（如果需要的話）
    # 注意：這裡我們將手動設定段落格式來模擬標題

    # 添加標題
    title = doc.add_heading('服務建議書範本', 0)

    # H1 標題：專案說明
    h1_1 = doc.add_heading('專案說明', 1)
    doc.add_paragraph('本專案旨在為客戶提供完整的系統整合服務，包含需求分析、系統設計、開發實施及維護支援。')

    # H1 標題：目標與需求
    h1_2 = doc.add_heading('目標與需求', 1)
    doc.add_paragraph('客戶希望建立一個現代化的資訊管理系統，主要功能包括：')
    doc.add_paragraph('1. 用戶管理')
    doc.add_paragraph('2. 數據處理')
    doc.add_paragraph('3. 報表生成')
    doc.add_paragraph('4. 系統整合')

    # H2 標題：技術需求
    h2_1 = doc.add_heading('技術需求', 2)
    doc.add_paragraph('需要支援高並發處理和數據安全加密。')

    # H1 標題：解決方案架構
    h1_3 = doc.add_heading('解決方案架構', 1)
    doc.add_paragraph('我們建議採用微服務架構，使用 Docker 容器化技術，前端使用 React，後端使用 Node.js，資料庫採用 PostgreSQL。')

    # H2 標題：系統組件
    h2_2 = doc.add_heading('系統組件', 2)
    doc.add_paragraph('包含 API 閘道、服務發現、配置管理等核心組件。')

    # H1 標題：預期效益
    h1_4 = doc.add_heading('預期效益', 1)
    doc.add_paragraph('預計可提升工作效率 40%，降低營運成本 25%，並提供更好的用戶體驗。')

    # H1 標題：時程與報價
    h1_5 = doc.add_heading('時程與報價', 1)
    doc.add_paragraph('專案總工期預計 6 個月，分為三個階段實施。')
    doc.add_paragraph('總報價：新台幣 800,000 元（含稅）。')

    # H2 標題：付款條件
    h2_3 = doc.add_heading('付款條件', 2)
    doc.add_paragraph('分三期付款：簽約時 30%、中期 40%、結案時 30%。')

    # H1 標題：維護與服務
    h1_6 = doc.add_heading('維護與服務', 1)
    doc.add_paragraph('提供一年免費維護服務，包含系統更新、錯誤修復及技術支援。')

    # H3 標題：系統更新細節（測試過濾功能）
    h3_1 = doc.add_heading('系統更新細節', 3)
    doc.add_paragraph('每月進行安全性更新和功能增強。')

    # H3 標題：錯誤修復流程（測試過濾功能）
    h3_2 = doc.add_heading('錯誤修復流程', 3)
    doc.add_paragraph('24小時內響應緊急錯誤，72小時內修復一般問題。')

    # 保存文件
    doc.save('sample_proposal_template.docx')
    print("✅ 已創建範例文件: sample_proposal_template.docx")
    print("📄 此文件包含多個階層的標題 (H1, H2, H3)，可用於測試標題階層過濾功能")
    print("🔍 系統將只使用 H1 和 H2 作為目錄標題，H3 標題將被過濾掉")

if __name__ == "__main__":
    create_sample_proposal()
