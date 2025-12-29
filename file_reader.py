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
        """讀取 Word 文檔並保留標題階層"""
        try:
            doc = Document(file_path)
            structured_content = []
            current_heading_level = 0

            for paragraph in doc.paragraphs:
                if not paragraph.text.strip():
                    continue

                text = paragraph.text.strip()

                # 檢查是否為標題樣式 - 更精確的判斷
                style_name = paragraph.style.name
                heading_level = 0

                # 精確匹配標準標題樣式
                if style_name in ['Heading 1', 'Heading 2', 'Heading 3', 'Heading 4', 'Heading 5', 'Heading 6', 'Heading 7', 'Heading 8', 'Heading 9']:
                    # 從 "Heading 1" 提取數字 1
                    try:
                        heading_level = int(style_name.split()[1])
                    except (ValueError, IndexError):
                        heading_level = 1  # 預設為 1
                elif style_name == 'Title':
                    heading_level = 1  # Title 視為最高等級標題
                # 避免誤判：排除包含 "Heading" 但不是標準樣式的段落
                elif 'Heading' in style_name and not style_name.startswith('Heading '):
                    # 如果是自定義樣式名稱包含 Heading，但不是標準格式，則不視為標題
                    pass

                # 根據標題等級添加標記
                if heading_level > 0:
                    # 添加標題標記和等級信息
                    marked_text = f"[H{heading_level}]{text}"
                    structured_content.append(marked_text)
                else:
                    # 普通段落
                    structured_content.append(text)

            return '\n'.join(structured_content)
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
        self.section_sources = {}  # 記錄每個章節的來源
        self.hierarchy_info = {}  # 記錄每個章節的階層信息
        self.original_headings = []  # 記錄原始標題的順序和內容

    def analyze_structure(self):
        """
        分析範本結構，提取章節標題和內容（基於 Word 標題階層）
        """
        lines = self.template_content.split('\n')
        current_section = None
        current_content = []
        heading_hierarchy = {}  # 追蹤標題階層

        # 調試信息
        found_markers = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 檢查是否為標記的標題 [H1]標題內容
            heading_match = re.match(r'^\[H(\d+)\](.+)$', line)
            if heading_match:
                found_markers = True
                heading_level = int(heading_match.group(1))
                heading_text = heading_match.group(2).strip()

                # 只記錄 H1 和 H2 標題作為目錄標題，過濾掉 H3 及以下的細項標題
                # 但是仍然要記錄 H3 等級，以便在統計中顯示
                if heading_level <= 2:
                    # 記錄原始標題順序（只包含 H1 和 H2）
                    self.original_headings.append({
                        'text': heading_text,
                        'level': heading_level,
                        'source': 'word_hierarchy'
                    })

                # 保存之前的章節
                if current_section and current_content:
                    self.sections[current_section] = '\n'.join(current_content)

                # 開始新章節 - 處理所有標題等級，確保每個標題都有對應內容
                current_section = heading_text
                current_content = []
                heading_hierarchy[heading_text] = heading_level
                self.section_sources[heading_text] = "word_hierarchy"
                self.hierarchy_info[heading_text] = f"Heading {heading_level}"
            else:

                # 如果還沒有遇到任何標題，將內容添加到一個預設章節
                if current_section is None:
                    current_section = "內容說明"
                    current_content = []

                # 添加到當前章節內容
                if current_section:
                    current_content.append(line)

        # 保存最後一個章節
        if current_section and current_content:
            self.sections[current_section] = '\n'.join(current_content)

        # 如果沒有找到任何結構化的標題，嘗試使用舊的關鍵字方法
        if not self.sections or not found_markers:
            if not found_markers:
                self._fallback_analysis()

        return self.sections

    def _is_potential_heading(self, line):
        """
        判斷一行文本是否可能是標題
        """
        if len(line) < 3 or len(line) > 80:  # 長度不合適
            return False

        # 擴展的關鍵字檢查 - 包含用戶提到的具體標題類型
        heading_keywords = [
            '專案', '項目', '服務', '方案', '架構', '需求', '目標',
            '效益', '成果', '時程', '進度', '報價', '價格', '維護',
            '支援', '結論', '總結', '建議', '說明', '概述', '介紹',
            '簡介', '公司', '人力', '配置', '團隊', '小組', '分析',
            '設計', '實施', '開發', '測試', '部署', '背景', '流程',
            '方法', '技術', '功能', '特點', '系統', '平台', '應用',
            '客戶', '用戶', '使用者', '管理', '資料', '數據', '資料庫',
            '介面', '界面', '前端', '後端', '伺服器', '雲端', '安全',
            '整合', '解決', '規劃', '執行', '監控', '報告', '統計'
        ]

        keyword_count = sum(1 for keyword in heading_keywords if keyword in line)
        if keyword_count >= 1:
            return True

        # 檢查是否有數字標題格式 (1. 2. (1) 等)
        if re.match(r'^\d+[\.\)\s]', line):
            return True

        # 檢查是否有特殊符號開頭
        if line[0] in ['•', '○', '●', '-', '—', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '（', '【', '[']:
            return True

        # 檢查是否包含公司名稱或專有名詞的模式
        if '公司' in line or '科技' in line or '人力' in line:
            return True

        return False

    def _fallback_analysis(self):
        """
        備用分析方法：當無法從 Word 標題階層獲取結構時使用
        """
        lines = self.template_content.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 使用智慧標題檢測
            is_section = self._is_potential_heading(line)

            if is_section:
                # 記錄原始標題順序（備用分析，只記錄主要標題）
                self.original_headings.append({
                    'text': line,
                    'level': 1,  # 備用分析的關鍵字標題預設為 H1
                    'source': 'keyword_analysis'
                })

                # 保存之前的章節
                if current_section and current_content:
                    self.sections[current_section] = '\n'.join(current_content)

                # 開始新章節
                current_section = line
                current_content = []
                self.section_sources[line] = "keyword_analysis"
                self.hierarchy_info[line] = "關鍵字識別"
            else:
                # 添加到當前章節內容
                if current_section:
                    current_content.append(line)

        # 保存最後一個章節
        if current_section and current_content:
            self.sections[current_section] = '\n'.join(current_content)

    def get_section_titles(self):
        """獲取所有章節標題"""
        return list(self.sections.keys())

    def get_section_content(self, title):
        """獲取指定章節的內容"""
        return self.sections.get(title, "")

    def get_section_source(self, title):
        """獲取指定章節的來源類型"""
        return self.section_sources.get(title, "unknown")

    def get_hierarchy_info(self, title):
        """獲取指定章節的階層信息"""
        return self.hierarchy_info.get(title, "無階層信息")

    def get_original_headings(self):
        """獲取原始標題的完整列表（按順序）"""
        return self.original_headings

    def get_original_heading_texts(self):
        """獲取原始標題文字列表（按順序）"""
        return [heading['text'] for heading in self.original_headings]

    def get_detailed_analysis(self):
        """獲取詳細的分析結果，包含階層信息"""
        analysis = []
        for title in self.get_section_titles():
            source = self.get_section_source(title)
            hierarchy = self.get_hierarchy_info(title)
            content_preview = self.get_section_content(title)[:100] + "..." if len(self.get_section_content(title)) > 100 else self.get_section_content(title)
            analysis.append({
                'title': title,
                'source': source,
                'hierarchy': hierarchy,
                'content_preview': content_preview,
                'content_length': len(self.get_section_content(title))
            })
        return analysis

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
