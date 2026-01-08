"""
Google Drive RAG 功能演示
展示如何使用歷史服務建議書作為 AI 生成的參考資料庫
"""

import os
import sys

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from file_reader import DocumentReader, ProposalTemplateAnalyzer
from proposal_writer import gpt_generate

def create_mock_rag_database():
    """創建模擬的 RAG 資料庫"""
    print("📚 創建模擬 RAG 參考資料庫...")

    # 模擬從 Google Drive 搜尋到的相關服務建議書
    mock_rag_db = {
        "ABC公司_AI_建議書.docx": """
[H1]服務建議書

[H1]專案說明
本公司專注於提供AI解決方案，協助客戶實現智慧化轉型。
我們擁有豐富的AI專案經驗，團隊由資深AI工程師和專案經理組成。

[H1]解決方案架構
採用微服務架構，前端使用React，後端使用Python FastAPI，
資料庫使用PostgreSQL，AI模型部署在雲端環境。

[H1]專案時程
專案總工期為6個月，分為需求分析、設計開發、測試部署三個階段。
""",

        "XYZ科技_CRM_建議書.docx": """
[H1]服務建議書

[H1]公司簡介
XYZ科技是一家專注於企業級軟體解決方案的科技公司，
擁有超過10年的軟體開發經驗。

[H1]專案團隊
專案團隊由以下人員組成：
- 專案經理：負責專案進度管控和客戶溝通
- 系統架構師：負責系統整體架構設計
- 開發工程師：負責程式開發和實作
- 測試工程師：負責系統測試和品質把關

[H1]服務內容
提供完整的CRM系統開發服務，包括需求分析、系統設計、
程式開發、測試部署和維護支援。
"""
    }

    print(f"✅ 已建立模擬 RAG 資料庫，包含 {len(mock_rag_db)} 個參考文件")
    return mock_rag_db

def test_rag_generation():
    """測試使用 RAG 資料庫生成內容"""
    print("\n🤖 測試 AI 內容生成 (使用 RAG 參考資料庫)...")

    # 模擬的客戶需求
    customer_need = "為一家製造業客戶開發智慧工廠管理系統，需要整合現有設備數據，實現生產排程優化和實時監控"

    # 模擬的標題結構
    outline_titles = [
        "專案說明",
        "解決方案架構",
        "專案團隊",
        "服務內容",
        "專案時程"
    ]

    # 建立模擬 RAG 資料庫
    rag_database = create_mock_rag_database()

    print(f"\n📝 客戶需求: {customer_need}")
    print(f"\n📋 建議書章節結構: {', '.join(outline_titles)}")

    # 使用 AI 生成內容 (會使用模擬內容，因為沒有 API key)
    generated_content = gpt_generate(
        outline_titles=outline_titles,
        customer_need=customer_need,
        rag_database=rag_database
    )

    print("\n📄 AI 生成的建議書內容:")
    print("=" * 50)
    print(generated_content)
    print("=" * 50)

    return generated_content

def demonstrate_rag_benefits():
    """展示 RAG 的好處"""
    print("\n🎯 RAG 功能的好處:")
    print("=" * 50)

    benefits = [
        "✅ 參考歷史成功案例：AI 可以學習過去成功建議書的寫作風格",
        "✅ 提升內容專業性：參考現有建議書確保內容符合業界標準",
        "✅ 保持一致性：新生成的建議書風格與歷史案例保持一致",
        "✅ 節省準備時間：不需要每次都重新設計建議書結構",
        "✅ 智慧化搜尋：系統自動從 Google Drive 找到最相關的參考文件",
        "✅ 靈活性調整：AI 會根據新客戶需求調整參考內容",
    ]

    for benefit in benefits:
        print(benefit)

def main():
    """主函數"""
    print("🚀 Google Drive RAG 功能演示")
    print("=" * 60)

    print("此演示展示如何使用 Google Drive 中的歷史服務建議書作為 AI 的參考資料庫")
    print("讓 AI 只能參考這些歷史資料來生成相似格式的客製化服務建議書")

    # 測試 RAG 生成
    generated_content = test_rag_generation()

    # 展示 RAG 好處
    demonstrate_rag_benefits()

    print("\n📚 實際使用步驟:")
    print("=" * 30)
    print("1. 設定 Google Drive API (參考 GOOGLE_DRIVE_SETUP.md)")
    print("2. 將您的服務建議書上傳到 Google Drive")
    print("3. 在應用程式中啟用 'Google Drive RAG 資料庫'")
    print("4. 輸入客戶類型和應用類型，系統會自動搜尋相關建議書")
    print("5. AI 會參考這些歷史建議書來生成新內容")

    print("\n💡 檔案命名建議:")
    print("- ABC公司_AI_建議書.docx")
    print("- XYZ科技_CRM_建議書.pdf")
    print("- 123企業_數據分析_建議書.docx")

    print("\n🎉 RAG 功能讓 AI 生成的建議書更加專業和一致！")

if __name__ == "__main__":
    main()
