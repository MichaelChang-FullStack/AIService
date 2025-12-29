#!/usr/bin/env python3
"""
檢查 Word 文件中的樣式
"""
from docx import Document

def check_word_styles():
    """檢查 Word 文件中的實際樣式"""

    print('🔍 檢查 Word 文件中的實際樣式...')

    try:
        doc = Document('sample_proposal_template.docx')
        print('所有段落及其樣式:')

        heading_count = 0
        for i, para in enumerate(doc.paragraphs, 1):
            if para.text.strip():  # 只顯示有內容的段落
                if para.style.name.startswith('Heading'):
                    heading_count += 1
                    print(f'{i}. 標題段落: "{para.text}", 樣式: {para.style.name}')
                elif heading_count < 15:  # 只顯示前15個非標題段落
                    print(f'{i}. 普通段落: "{para.text[:50]}...", 樣式: {para.style.name}')

        print(f'\n總共發現 {heading_count} 個標題樣式段落')

    except Exception as e:
        print(f'❌ 錯誤: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_word_styles()
