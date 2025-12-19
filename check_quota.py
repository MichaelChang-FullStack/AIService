#!/usr/bin/env python3
"""
Google AI 配額檢查與升級指南腳本
"""
import os
import webbrowser

def check_api_key():
    """檢查 API Key 設定"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print(f"✅ GOOGLE_API_KEY 已設定: {api_key[:8]}...")
        return True
    else:
        print("❌ GOOGLE_API_KEY 未設定")
        return False

def show_quota_info():
    """顯示配額相關資訊"""
    print("\n" + "="*50)
    print("📊 Google AI 免費額度說明")
    print("="*50)
    print("• 每日免費額度：有限制")
    print("• 主要限制：")
    print("  - 輸入 token 數量")
    print("  - 請求次數 (每分鐘/每日)")
    print("  - 不同模型有不同限制")
    print("\n💡 當額度用完時，系統會自動切換到模擬模式")

def show_upgrade_options():
    """顯示升級選項"""
    print("\n" + "="*50)
    print("🚀 升級方案選項")
    print("="*50)

    options = {
        "1": {
            "name": "Google AI Studio 付費方案",
            "url": "https://aistudio.google.com/",
            "description": "直接在 AI Studio 升級，支援更多額度"
        },
        "2": {
            "name": "Google Cloud Vertex AI",
            "url": "https://cloud.google.com/vertex-ai",
            "description": "企業級方案，更高的額度和進階功能"
        },
        "3": {
            "name": "檢查目前用量",
            "url": "https://ai.google.dev/usage?tab=rate-limit",
            "description": "查看目前的使用情況和限制"
        }
    }

    for key, option in options.items():
        print(f"{key}. {option['name']}")
        print(f"   {option['description']}")
        print(f"   連結: {option['url']}")
        print()

    while True:
        choice = input("請選擇要開啟的頁面 (1-3)，或按 Enter 跳過: ").strip()
        if choice in options:
            print(f"正在開啟 {options[choice]['name']}...")
            webbrowser.open(options[choice]['url'])
            break
        elif choice == "":
            break
        else:
            print("無效選擇，請重新輸入")

def main():
    print("🔍 Google AI 配額檢查工具")
    print("-" * 30)

    # 檢查 API Key
    has_key = check_api_key()

    # 顯示配額資訊
    show_quota_info()

    # 顯示升級選項
    show_upgrade_options()

    print("\n" + "="*50)
    print("💡 使用建議")
    print("="*50)
    print("1. 免費額度通常每天會重置")
    print("2. 升級付費方案可獲得更多額度")
    print("3. 額度用完時仍可使用模擬模式生成建議書")
    print("4. 設定環境變數可避免重複輸入 API Key")

    if has_key:
        print("\n🎯 現在可以運行主程式:")
        print("python -m streamlit run main.py")
    else:
        print("\n⚠️  建議先設定 API Key 以獲得最佳體驗")
        print("設定方式: $env:GOOGLE_API_KEY='您的金鑰'")

if __name__ == "__main__":
    main()
