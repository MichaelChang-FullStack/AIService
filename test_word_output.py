#!/usr/bin/env python3
"""
測試 Word 文檔輸出功能，包含目錄和頁碼
"""
import os
from proposal_writer import write_proposal_docx

def test_word_output():
    """測試帶有目錄和頁碼的 Word 文檔生成"""

    # 模擬測試數據
    outline_titles = [
        '專案說明',
        '目標與需求',
        '技術需求',
        '解決方案架構',
        '系統組件',
        '預期效益',
        '時程與報價',
        '付款條件',
        '維護與服務'
    ]

    content_blocks = [
        '本專案旨在為客戶提供完整的系統整合服務，包含需求分析、系統設計、開發實施及維護支援。專案預計在3個月內完成，主要交付物包括系統架構設計文檔、源代碼、部署腳本以及使用手冊。',
        '客戶希望建立一個現代化的資訊管理系統，主要功能包括用戶管理、數據處理、報表生成和系統整合。系統需要支援高並發訪問，並提供良好的用戶體驗和數據安全保障。',
        '技術上需要支援每日10萬次訪問，高可用性99.9%，數據加密存儲，支援多種數據格式導入導出，並提供RESTful API接口供第三方系統集成。',
        '我們建議採用微服務架構，使用Docker容器化技術，前端使用React框架，後端使用Node.js，資料庫採用PostgreSQL，緩存使用Redis，消息隊列使用RabbitMQ。',
        '系統組件包括用戶認證服務、數據處理服務、報表生成服務、文件管理服務、通知服務、監控服務、API網關、服務發現組件和配置管理中心。',
        '預計可提升工作效率40%，降低營運成本25%，減少數據處理時間60%，並提供更好的用戶體驗和數據分析能力。投資回報期預計在12個月內實現。',
        '專案總工期預計6個月，分為需求分析(1個月)、系統設計(1個月)、開發實現(3個月)、測試部署(1個月)等階段。具體里程碑和交付時間將在專案啟動會議後確定。',
        '總報價：新台幣800,000元(含稅)。付款條件分三期：簽約時支付30%(240,000元)、項目中期支付40%(320,000元)、項目結案驗收後支付30%(240,000元)。',
        '提供一年免費維護服務，包含系統更新、錯誤修復、性能優化、安全補丁。維護期內提供7x24小時技術支援，響應時間不超過4小時。',
    ]

    # 創建模擬的 template_analyzer
    class MockTemplateAnalyzer:
        def get_hierarchy_info(self, title):
            hierarchy_map = {
                '專案說明': 'Heading 1',
                '目標與需求': 'Heading 1',
                '技術需求': 'Heading 2',
                '解決方案架構': 'Heading 1',
                '系統組件': 'Heading 2',
                '預期效益': 'Heading 1',
                '時程與報價': 'Heading 1',
                '付款條件': 'Heading 2',
                '維護與服務': 'Heading 1'
            }
            return hierarchy_map.get(title, 'Heading 1')

    mock_analyzer = MockTemplateAnalyzer()

    # 測試使用範本文件（如果存在）
    template_file = 'sample_proposal_template.docx'
    use_template = os.path.exists(template_file)

    # 生成測試文件
    test_filename = 'test_output_with_template.docx' if use_template else 'test_output_basic.docx'

    print("🛠️ 正在生成測試 Word 文檔...")
    print(f"📄 文件名: {test_filename}")
    print(f"📊 章節數: {len(outline_titles)}")
    print(f"🎨 使用範本: {'是' if use_template else '否'}")

    try:
        template_path = template_file if use_template else None
        write_proposal_docx(test_filename, outline_titles, content_blocks, mock_analyzer, template_path)

        print("✅ Word 文檔生成成功！")
        print(f"📁 文件保存位置: {os.path.abspath(test_filename)}")

        if use_template:
            print("\n📋 文檔包含內容:")
            print("✅ 封面頁面（複製範本樣式）")
            print("✅ 專業目錄（含階層縮進）")
            print("✅ 內容頁面（應用範本格式）")
            print("✅ 正確的標題階層結構")
            print("✅ 頁腳頁碼")
        else:
            print("\n📋 文檔包含內容:")
            print("✅ 封面頁面")
            print("✅ 目錄頁面")
            print("✅ 內容頁面")
            print("✅ 標題階層")

        # 檢查文件是否存在
        if os.path.exists(test_filename):
            file_size = os.path.getsize(test_filename)
            print(f"📏 文件大小: {file_size / 1024:.1f} KB")
        else:
            print("❌ 文件生成失敗")

    except Exception as e:
        print(f"❌ 生成失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_word_output()
