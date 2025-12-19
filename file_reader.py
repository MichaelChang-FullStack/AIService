"""
文件讀取模組
支援讀取 Word (.docx) 和 PDF 文件作為服務建議書範本
"""
import os
import re
from docx import Document
import PyPDF2
import pdfplumber
import mimetypes

class DocumentReader:
    """通用文件讀取器"""

    @staticmethod
    def read_file(file_path):
        """
        根據文件類型讀取內容
        返回: (content, file_type)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 檢測文件類型
        mime_type, _ = mimetypes.guess_type(file_path)

        if file_path.lower().endswith('.docx') or (mime_type and 'word' in mime_type):
            return DocumentReader.read_docx(file_path), 'docx'
        elif file_path.lower().endswith('.pdf') or (mime_type and 'pdf' in mime_type):
            return DocumentReader.read_pdf(file_path), 'pdf'
        else:
            raise ValueError(f"不支援的文件類型: {file_path}")

    @staticmethod
    def read_docx(file_path):
        """讀取 Word 文檔"""
        try:
            doc = Document(file_path)
            content = []

            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    content.append(paragraph.text.strip())

            return '\n'.join(content)
        except Exception as e:
            raise Exception(f"讀取 Word 文件失敗: {e}")

    @staticmethod
    def read_pdf(file_path):
        """讀取 PDF 文檔"""
        content = []

        try:
            # 首先嘗試使用 pdfplumber (更好的文本提取)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content.append(text.strip())
        except Exception:
            # 如果 pdfplumber 失敗，使用 PyPDF2 作為備用
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        if text:
                            content.append(text.strip())
            except Exception as e:
                raise Exception(f"讀取 PDF 文件失敗: {e}")

        if not content:
            raise Exception("無法從 PDF 文件中提取文本內容")

        return '\n'.join(content)

class ProposalTemplateAnalyzer:
    """服務建議書範本分析器"""

    def __init__(self, template_content):
        self.template_content = template_content
        self.sections = {}

    def analyze_structure(self):
        """
        分析範本結構，提取章節標題和內容
        """
        lines = self.template_content.split('\n')
        current_section = None
        current_content = []

        # 常見的章節關鍵字
        section_keywords = [
            '專案', '項目', '服務', '方案', '架構', '需求', '目標',
            '效益', '成果', '時程', '進度', '報價', '價格', '維護',
            '支援', '結論', '總結', '建議', '說明', '概述', '介紹'
        ]

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 檢查是否為章節標題
            is_section = False
            for keyword in section_keywords:
                if keyword in line and len(line) < 50:  # 避免過長的行被誤認為標題
                    is_section = True
                    break

            # 檢查是否包含數字標題 (如 1. 2. 等)
            if re.match(r'^\d+[\.\s]', line):
                is_section = True

            # 檢查是否為大寫或特定格式的標題
            if line.isupper() or line.istitle():
                is_section = True

            if is_section:
                # 保存之前的章節
                if current_section and current_content:
                    self.sections[current_section] = '\n'.join(current_content)

                # 開始新章節
                current_section = line
                current_content = []
            else:
                # 添加到當前章節內容
                if current_section:
                    current_content.append(line)

        # 保存最後一個章節
        if current_section and current_content:
            self.sections[current_section] = '\n'.join(current_content)

        return self.sections

    def get_section_titles(self):
        """獲取所有章節標題"""
        return list(self.sections.keys())

    def get_section_content(self, title):
        """獲取指定章節的內容"""
        return self.sections.get(title, "")

    def generate_outline_summary(self):
        """生成範本大綱摘要"""
        if not self.sections:
            return "無法分析範本結構"

        summary = "範本結構分析：\n"
        for i, (title, content) in enumerate(self.sections.items(), 1):
            # 截取內容預覽 (前100個字符)
            preview = content[:100] + "..." if len(content) > 100 else content
            summary += f"{i}. {title}\n   內容預覽: {preview}\n\n"

        return summary

def extract_template_info(file_path):
    """
    從文件路徑提取範本信息
    返回: (content, analyzer, file_type)
    """
    content, file_type = DocumentReader.read_file(file_path)
    analyzer = ProposalTemplateAnalyzer(content)
    analyzer.analyze_structure()

    return content, analyzer, file_type
