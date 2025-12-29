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
                template_example = "以下是每個章節對應的範本參考內容，請為每個標題生成類似風格和內容的文字：\n\n"
                for i, title in enumerate(outline_titles):
                    if title in template_sections:
                        content = template_sections[title]
                        template_example += f"【{i+1}. {title}】的參考內容：\n{content[:500]}...\n\n"
                    else:
                        template_example += f"【{i+1}. {title}】的參考內容：\n根據客戶需求提供專業服務內容，包含具體實施方案和效益分析。\n\n"

                prompt = (
                    f"請為新客戶需求《{customer_need}》撰寫完整服務建議書。\n\n"
                    f"{template_example}"
                    f"【重要】請完全使用以下確切的章節標題（不能修改標題名稱）：\n{outline_str}\n\n"
                    f"要求：\n"
                    f"1. 必須使用上面列出的確切標題名稱，不能修改或替換標題\n"
                    f"2. 為每個標題生成內容時，請參考該標題對應的範本內容風格和結構\n"
                    f"3. 內容要與範本風格類似，但根據新客戶需求進行適當調整\n"
                    f"4. 每個章節需明確分開\n"
                    f"5. 用繁體中文撰寫\n"
                    f"6. 每個章節最少100字\n"
                    f"7. 保持專業服務建議書的格式和語氣\n"
                    f"8. 確保內容與標題相關，文題相符"
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

def write_proposal_docx(filename, outline_titles, content_blocks, template_analyzer=None, template_file_path=None):
    """
    生成帶有目錄、高級格式的 Word 文檔，複製範本文件格式
    """
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE

    doc = Document()

    # 如果有範本文件，嘗試讀取其樣式信息
    template_styles = {}
    if template_file_path and os.path.exists(template_file_path):
        try:
            template_doc = Document(template_file_path)

            # 讀取範本文檔的樣式信息
            for style in template_doc.styles:
                if style.type == WD_STYLE_TYPE.PARAGRAPH:
                    style_name = style.name
                    if 'Heading' in style_name or 'Title' in style_name or 'Normal' in style_name:
                        template_styles[style_name] = {
                            'font_size': getattr(style.font, 'size', None),
                            'font_bold': getattr(style.font, 'bold', None),
                            'font_italic': getattr(style.font, 'italic', None),
                        }

            print(f"成功讀取範本樣式: {len(template_styles)} 個樣式")

        except Exception as e:
            print(f"讀取範本樣式失敗: {e}")
            template_styles = {}

    # 添加封面 - 嘗試使用範本的標題樣式
    title_para = doc.add_paragraph()
    title_run = title_para.add_run('服務建議書')

    # 如果有範本樣式，嘗試應用
    if 'Title' in template_styles and template_styles['Title'].get('font_size'):
        title_run.font.size = template_styles['Title']['font_size']
    else:
        title_run.font.size = Pt(24)

    if 'Title' in template_styles and template_styles['Title'].get('font_bold') is not None:
        title_run.font.bold = template_styles['Title']['font_bold']
    else:
        title_run.font.bold = True

    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 添加日期和生成信息
    import datetime
    date_para = doc.add_paragraph()
    date_run = date_para.add_run(f'生成日期: {datetime.datetime.now().strftime("%Y年%m月%d日")}')

    # 應用 Normal 樣式（如果有的話）
    if 'Normal' in template_styles and template_styles['Normal'].get('font_size'):
        date_run.font.size = template_styles['Normal']['font_size']

    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 添加目錄頁面
    doc.add_page_break()

    # 目錄標題 - 使用範本樣式
    toc_title_para = doc.add_paragraph()
    toc_title_run = toc_title_para.add_run('目錄')
    toc_title_run.font.size = Pt(16)
    toc_title_run.font.bold = True
    toc_title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 添加空行
    doc.add_paragraph()

    # 創建專業的目錄內容
    toc_para = doc.add_paragraph()

    for i, title in enumerate(outline_titles, 1):
        # 根據階層決定縮進
        if template_analyzer:
            hierarchy_info = template_analyzer.get_hierarchy_info(title)
            if 'Heading 2' in hierarchy_info:
                indent = "    "  # 子項目縮進
            elif 'Heading 3' in hierarchy_info:
                indent = "        "  # 子子項目縮進
            else:
                indent = ""  # 主要項目
        else:
            indent = ""

        # 添加目錄項目
        toc_item = f"{indent}{i}. {title}"
        # 計算點點點的數量，使頁碼對齊右邊
        dots = "." * (80 - len(toc_item.encode('gbk', errors='ignore')))
        toc_item += f"{dots}{i+2}\n"

        toc_run = toc_para.add_run(toc_item)
        if 'Normal' in template_styles and template_styles['Normal'].get('font_size'):
            toc_run.font.size = template_styles['Normal']['font_size']

    # 添加說明
    doc.add_paragraph()
    note_para = doc.add_paragraph()
    note_run = note_para.add_run('註: 目錄頁碼為預估值，實際頁碼以 Word 文件顯示為準')
    note_run.font.size = Pt(9)
    note_run.font.italic = True
    note_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 添加內容頁面
    doc.add_page_break()

    # 添加內容章節
    for i, (title, content) in enumerate(zip(outline_titles, content_blocks)):
        # 決定標題等級和樣式
        if template_analyzer:
            hierarchy_info = template_analyzer.get_hierarchy_info(title)
            if 'Heading 1' in hierarchy_info:
                level = 1
                style_name = 'Heading 1'
            elif 'Heading 2' in hierarchy_info:
                level = 2
                style_name = 'Heading 2'
            elif 'Heading 3' in hierarchy_info:
                level = 3
                style_name = 'Heading 3'
            else:
                level = 1
                style_name = 'Heading 1'
        else:
            level = 1
            style_name = 'Heading 1'

        # 添加標題 - 嘗試使用範本樣式
        heading_para = doc.add_paragraph()
        heading_run = heading_para.add_run(title)

        # 應用範本的標題樣式（如果有的話）
        if style_name in template_styles:
            style_info = template_styles[style_name]
            if style_info.get('font_size'):
                heading_run.font.size = style_info['font_size']
            if style_info.get('font_bold') is not None:
                heading_run.font.bold = style_info['font_bold']
            if style_info.get('font_italic') is not None:
                heading_run.font.italic = style_info['font_italic']
        else:
            # 使用預設樣式
            heading_run.font.size = Pt(14 - level)  # H1: 14pt, H2: 13pt, H3: 12pt
            heading_run.font.bold = True

        # 設置段落格式
        if level == 1:
            heading_para.style = 'Heading 1' if 'Heading 1' in [s.name for s in doc.styles] else None
        elif level == 2:
            heading_para.style = 'Heading 2' if 'Heading 2' in [s.name for s in doc.styles] else None
        elif level == 3:
            heading_para.style = 'Heading 3' if 'Heading 3' in [s.name for s in doc.styles] else None

        # 添加內容
        content_para = doc.add_paragraph(content)

        # 應用 Normal 樣式（如果有的話）
        if 'Normal' in template_styles and template_styles['Normal'].get('font_size'):
            for run in content_para.runs:
                run.font.size = template_styles['Normal']['font_size']

        # 添加分隔線（除了最後一個章節）
        if i < len(outline_titles) - 1:
            doc.add_paragraph()  # 空行分隔

    # 添加頁腳
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    # 為所有段落添加頁碼（如果需要）
    for section in doc.sections:
        footer = section.footer
        footer_para = footer.paragraphs[0]
        footer_para.text = "第 {PAGE} 頁 / 共 {NUMPAGES} 頁"
        footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.save(filename)
