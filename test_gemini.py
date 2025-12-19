import os
import google.genai as genai

# 測試 Gemini API 並列出可用模型
def test_gemini():
    gemini_key = os.getenv('GOOGLE_API_KEY', None)
    if not gemini_key:
        gemini_key = input("請輸入您的 Google AI API Key: ").strip()
        if not gemini_key:
            print("未提供 API Key，測試取消")
            return

    try:
        client = genai.Client(api_key=gemini_key)

        # 首先列出所有可用模型
        print("正在檢查可用模型...")
        models = client.models.list()
        print("可用模型列表:")
        gemini_models = []
        for model in models:
            if 'gemini' in model.name.lower():
                gemini_models.append(model.name)
                print(f"  - {model.name}")

        if not gemini_models:
            print("未找到任何 Gemini 模型，請檢查您的 API 權限")
            return

        # 嘗試使用第一個可用的 Gemini 模型
        model_to_use = gemini_models[0]
        print(f"\n使用模型: {model_to_use}")

        response = client.models.generate_content(
            model=model_to_use,
            contents="請用繁體中文說 'Hello, World!'"
        )
        print("API 測試成功!")
        print("回應:", response.text)

    except Exception as e:
        print(f"API 測試失敗: {e}")
        print("請檢查您的 API Key 是否正確，或是否啟用了 Gemini 模型權限")
        print("\n可能的解決方案:")
        print("1. 確認 API Key 正確")
        print("2. 檢查 Google Cloud Console 是否啟用了 Generative Language API")
        print("3. 確認您的 Google Cloud 專案有足夠的配額")

if __name__ == "__main__":
    test_gemini()
