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

    # 創建一個模擬的服務建議書內容（模擬 Word 標題階層）
    sample_content = """[H1]專案說明

本專案旨在為客戶提供完整的系統整合服務，包含需求分析、系統設計、開發實施及維護支援。

[H1]目標與需求

客戶希望建立一個現代化的資訊管理系統，主要功能包括：
1. 用戶管理
2. 數據處理
3. 報表生成
4. 系統整合

[H2]技術需求
需要支援高並發處理和數據安全加密。

[H1]解決方案架構

我們建議採用微服務架構，使用 Docker 容器化技術，前端使用 React，後端使用 Node.js，資料庫採用 PostgreSQL。

[H2]系統組件
包含 API 閘道、服務發現、配置管理等核心組件。

[H1]預期效益

預計可提升工作效率 40%，降低營運成本 25%，並提供更好的用戶體驗。

[H1]時程與報價

專案總工期預計 6 個月，分為三個階段實施。
總報價：新台幣 800,000 元（含稅）。

[H2]付款條件
分三期付款：簽約時 30%、中期 40%、結案時 30%。

[H1]維護與服務

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

    # 顯示原始標題順序（只顯示 H1 和 H2）
    original_headings = analyzer.get_original_headings()
    h1_h2_headings = [h for h in original_headings if h['level'] <= 2]
    if h1_h2_headings:
        print(f"\n🎯 目錄標題 (H1 & H2) 順序 ({len(h1_h2_headings)} 個):")
        for i, heading in enumerate(h1_h2_headings, 1):
            print(f"{i}. [H{heading['level']}] {heading['text']} ({heading['source']})")

    if original_headings:
        filtered_count = len(original_headings) - len(h1_h2_headings)
        if filtered_count > 0:
            print(f"ℹ️ 已過濾掉 {filtered_count} 個 H3 及以下的細項標題")

    # 檢查原始內容中的標記
    has_markers = "[H" in sample_content
    print(f"\n原始內容是否包含標題標記: {has_markers}")

    print(f"\n📝 分析出的章節:")
    for title, content in sections.items():
        # 獲取章節來源信息
        hierarchy_info = analyzer.get_hierarchy_info(title)
        source = analyzer.get_section_source(title)

        print(f"• {title} ({hierarchy_info}, {source})")
        print(f"  內容長度: {len(content)} 字符")
        print(f"  內容預覽: {content[:80]}...")
        print()

    print("✅ 文件讀取和分析功能測試完成！")

    # 測試實際的文件讀取
    print("\n🔍 測試真實文件讀取...")

    # 測試範例文件
    test_file = 'sample_proposal_template.docx'
    if os.path.exists(test_file):
        print(f"📁 測試讀取文件: {test_file}")
        try:
            from file_reader import extract_template_info
            content, analyzer, file_type = extract_template_info(test_file)
            print(f"✅ 成功讀取 {file_type.upper()} 文件")
            print(f"📊 分析結果: 檢測到 {len(analyzer.get_section_titles())} 個章節")

            # 顯示目錄標題（只顯示 H1 和 H2）
            original_headings = analyzer.get_original_headings()
            h1_h2_headings = [h for h in original_headings if h['level'] <= 2]
            if h1_h2_headings:
                print(f"🎯 目錄標題 (H1 & H2) ({len(h1_h2_headings)} 個):")
                for i, heading in enumerate(h1_h2_headings[:8], 1):  # 顯示前8個
                    print(f"  {i}. [H{heading['level']}] {heading['text']}")

                if len(h1_h2_headings) > 8:
                    print(f"  ... 還有 {len(h1_h2_headings) - 8} 個標題")

            if original_headings:
                filtered_count = len(original_headings) - len(h1_h2_headings)
                if filtered_count > 0:
                    print(f"ℹ️ 已過濾掉 {filtered_count} 個 H3 及以下的細項標題")
            else:
                print("⚠️ 未檢測到原始標題順序")

            # 顯示分析摘要
            print(f"\n📋 章節摘要:")
            for title in analyzer.get_section_titles()[:3]:  # 只顯示前3個
                source = analyzer.get_section_source(title)
                hierarchy = analyzer.get_hierarchy_info(title)
                print(f"  • {title} ({hierarchy}, {source})")

            if len(analyzer.get_section_titles()) > 3:
                print(f"  ... 還有 {len(analyzer.get_section_titles()) - 3} 個章節")

        except Exception as e:
            print(f"❌ 讀取文件失敗: {e}")
    else:
        print("ℹ️ 範例文件不存在，請先運行: python create_sample_docx.py")

    # 檢查其他範本文件
    template_files = [
        '範本.docx',
        '範本.pdf',
        'template.docx',
        'template.pdf'
    ]

    found_files = []
    for filename in template_files:
        if os.path.exists(filename):
            found_files.append(filename)
            print(f"📁 發現額外範本文件: {filename}")

    if not found_files:
        print("ℹ️ 未發現其他範本文件")
        print("💡 您可以通過 Streamlit 介面上傳 .docx 或 .pdf 文件進行測試")
    else:
        print(f"\n🎯 總共發現 {len(found_files) + (1 if os.path.exists(test_file) else 0)} 個範本文件")

if __name__ == "__main__":
    test_file_reader()
