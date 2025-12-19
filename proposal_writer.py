import os
from docx import Document

def gpt_generate(outline_titles, customer_need, model_name="gemini-2.5-flash-lite", template_content=None, template_sections=None):
    """
    使用新版 google.genai (Gemini) 產生建議書內容。
    可選: 提供範本內容和章節結構來生成類似內容。
    若無 API KEY 或失敗則回傳模擬內容。
    """
    gemini_key = os.getenv('GOOGLE_API_KEY', None)
    try:
        if gemini_key:
            import google.genai as genai
            # 新版 API 初始化方式
            client = genai.Client(api_key=gemini_key)

            
            print(f"🚀 正在使用 AI 模型: {model_name}")

            outline_str = "\n".join([f"{i+1}. {t}" for i, t in enumerate(outline_titles)])

            # 如果有範本內容，包含在 prompt 中
            if template_content and template_sections:
                template_example = "以下是參考範本的內容結構：\n\n"
                for title, content in template_sections.items():
                    template_example += f"章節：{title}\n內容：{content[:300]}...\n\n"

                prompt = (
                    f"請參考以下範本結構和內容，為新客戶需求《{customer_need}》撰寫完整服務建議書。\n\n"
                    f"{template_example}"
                    f"請按照以下章節架構撰寫：\n{outline_str}\n\n"
                    f"要求：\n"
                    f"1. 內容要與範本風格類似，但根據新客戶需求進行適當調整\n"
                    f"2. 每個章節需明確分開\n"
                    f"3. 用繁體中文撰寫\n"
                    f"4. 每個章節最少100字\n"
                    f"5. 保持專業服務建議書的格式和語氣"
                )
            else:
                prompt = (
                    f"請根據以下章節，為新客戶需求《{customer_need}》撰寫完整服務建議書，章節架構如下：\n{outline_str}\n\n每個章節需明確分開。用繁體中文，每章節最少100字。"
                )
            
            # 新版 API 呼叫方式
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            
            return response.text
        else:
            raise Exception('no_gemini_key')
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print(f"⚠️  Gemini API 免費額度已用完，使用模擬內容生成建議書")
            print("💡 如需更多使用額度，請前往 https://ai.google.dev 升級方案")
        else:
            print(f"DEBUG ERROR: 發生錯誤，執行模擬內容。錯誤：{e}")

        return '\n\n'.join([
            f'{title}\n這是針對新客戶需求 "{customer_need}" 產生的預設段落內容 (Gemini 免費額度已用完，改用模擬內容)。' for title in outline_titles
        ])

def write_proposal_docx(filename, outline_titles, content_blocks):
    doc = Document()
    doc.add_heading('服務建議書', 0)
    for title, content in zip(outline_titles, content_blocks):
        doc.add_heading(title, level=1)
        doc.add_paragraph(content)
    doc.save(filename)
