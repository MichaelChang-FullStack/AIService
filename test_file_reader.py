#!/usr/bin/env python3
"""
測試文件讀取功能
"""
import os
from file_reader import DocumentReader, ProposalTemplateAnalyzer

def test_file_reader():
    """測試文件讀取功能"""

    # 測試模擬內容
    print("🔍 測試範本分析功能...")

    # 創建一個模擬的服務建議書內容
    sample_content = """
    專案說明

    本專案旨在為客戶提供完整的系統整合服務，包含需求分析、系統設計、開發實施及維護支援。

    目標與需求

    客戶希望建立一個現代化的資訊管理系統，主要功能包括：
    1. 用戶管理
    2. 數據處理
    3. 報表生成
    4. 系統整合

    解決方案架構

    我們建議採用微服務架構，使用 Docker 容器化技術，前端使用 React，後端使用 Node.js，資料庫採用 PostgreSQL。

    預期效益

    預計可提升工作效率 40%，降低營運成本 25%，並提供更好的用戶體驗。

    時程與報價

    專案總工期預計 6 個月，分為三個階段實施。
    總報價：新台幣 800,000 元（含稅）。

    維護與服務

    提供一年免費維護服務，包含系統更新、錯誤修復及技術支援。
    """

    print("📄 範本內容預覽:")
    print("-" * 50)
    print(sample_content[:300] + "...")
    print("-" * 50)

    # 測試分析器
    analyzer = ProposalTemplateAnalyzer(sample_content)
    sections = analyzer.analyze_structure()

    print("\n📊 分析結果:")
    print(f"檢測到 {len(sections)} 個章節:")

    for title, content in sections.items():
        print(f"• {title}")
        print(f"  內容長度: {len(content)} 字符")
        print(f"  內容預覽: {content[:50]}...")
        print()

    print("✅ 文件讀取和分析功能測試完成！")

    # 測試實際的文件讀取（如果有範本文件）
    print("\n🔍 檢查範本文件...")
    template_files = [
        'sample_template.docx',
        'sample_template.pdf',
        '範本.docx',
        '範本.pdf'
    ]

    found_files = []
    for filename in template_files:
        if os.path.exists(filename):
            found_files.append(filename)
            print(f"📁 發現範本文件: {filename}")

    if not found_files:
        print("ℹ️ 未發現範本文件，請手動放置 .docx 或 .pdf 文件到專案目錄")
        print("支援的文件類型: .docx, .pdf")
    else:
        print(f"\n🎯 發現 {len(found_files)} 個範本文件")
        print("您可以通過 Streamlit 介面上傳這些文件進行測試")

if __name__ == "__main__":
    test_file_reader()
