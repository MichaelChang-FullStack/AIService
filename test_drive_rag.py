"""
測試 Google Drive RAG 功能
"""

from drive_utils import initialize_drive_client, create_proposal_search_engine

def test_drive_connection():
    """測試 Google Drive 連線"""
    print("🔗 測試 Google Drive 連線...")

    try:
        # 初始化客戶端
        drive_client = initialize_drive_client()
        if not drive_client:
            print("❌ Google Drive 連線失敗")
            return False

        print("✅ Google Drive 連線成功")

        # 建立搜尋引擎
        search_engine = create_proposal_search_engine(drive_client)

        # 測試搜尋功能
        print("\n🔍 測試檔案搜尋功能...")
        files = search_engine.search_proposal_files(max_results=3)

        if files:
            print(f"✅ 找到 {len(files)} 個檔案")
            return True
        else:
            print("⚠️ 未找到服務建議書檔案（這可能是正常的，如果您的 Drive 中沒有相關檔案）")
            return True

    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_rag_database():
    """測試 RAG 資料庫建立"""
    print("\n📚 測試 RAG 資料庫建立...")

    try:
        drive_client = initialize_drive_client()
        if not drive_client:
            return False

        search_engine = create_proposal_search_engine(drive_client)

        # 測試建立 RAG 資料庫
        rag_db = search_engine.build_rag_database(
            customer_type="公司",
            application_type="AI",
            max_files=2
        )

        if rag_db:
            print(f"✅ RAG 資料庫建立成功，包含 {len(rag_db)} 個文件")
            for file_name, content in rag_db.items():
                print(f"  - {file_name}: {len(content)} 字符")
            return True
        else:
            print("⚠️ 未建立 RAG 資料庫（可能沒有找到相關檔案）")
            return True

    except Exception as e:
        print(f"❌ RAG 測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🧪 Google Drive RAG 功能測試")
    print("=" * 50)

    # 測試連線
    connection_ok = test_drive_connection()

    if connection_ok:
        # 測試 RAG 功能
        rag_ok = test_rag_database()

        if rag_ok:
            print("\n🎉 所有測試通過！Google Drive RAG 功能正常")
        else:
            print("\n⚠️ RAG 功能測試未完全通過，但連線正常")
    else:
        print("\n❌ 連線測試失敗，請檢查設定")

    print("\n💡 使用提示：")
    print("- 確保 credentials.json 檔案存在")
    print("- 確保 Google Drive 中有服務建議書檔案")
    print("- 檔案命名建議：{客戶名稱}_{應用類型}_建議書.docx")

if __name__ == "__main__":
    main()
