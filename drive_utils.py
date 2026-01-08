"""
Google Drive 工具模組
用於搜尋和管理服務建議書檔案，作為 RAG 資料庫
"""

import os
import io
import re
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import tempfile
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Drive API 範圍
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class GoogleDriveClient:
    """Google Drive API 客戶端"""

    def __init__(self, credentials_path: str = 'credentials.json'):
        """
        初始化 Google Drive 客戶端

        Args:
            credentials_path: credentials.json 檔案路徑
        """
        self.credentials_path = credentials_path
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Google Drive API 認證"""
        creds = None

        # 檢查是否有儲存的認證資訊
        token_path = 'token.json'
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # 如果沒有有效的認證資訊，進行認證流程
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"找不到 credentials.json 檔案: {self.credentials_path}\n"
                        "請從 Google Cloud Console 下載並放置在此目錄中。"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # 儲存認證資訊
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        # 建立 Drive API 服務
        self.service = build('drive', 'v3', credentials=creds)
        print("✅ Google Drive API 認證成功")

class ProposalSearchEngine:
    """服務建議書搜尋引擎"""

    def __init__(self, drive_client: GoogleDriveClient):
        """
        初始化搜尋引擎

        Args:
            drive_client: GoogleDriveClient 實例
        """
        self.drive_client = drive_client
        self.proposal_files = []  # 快取的建議書檔案列表

    def search_proposal_files(self,
                            customer_type: Optional[str] = None,
                            application_type: Optional[str] = None,
                            max_results: int = 20) -> List[Dict]:
        """
        搜尋服務建議書檔案

        Args:
            customer_type: 客戶類型 (如: 公司名稱、行業)
            application_type: 應用類型 (如: AI, CRM, 數據分析)
            max_results: 最大搜尋結果數量

        Returns:
            檔案資訊列表，每個檔案包含 id, name, mimeType, modifiedTime 等資訊
        """
        query_parts = []

        # 檔案類型過濾 - 只找 Word 文件和 PDF
        query_parts.append("(mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document' or mimeType='application/pdf')")

        # 檔案名稱包含建議書相關關鍵字
        name_keywords = ['建議書', '提案', 'proposal', '服務', '方案']
        name_conditions = " or ".join([f"name contains '{kw}'" for kw in name_keywords])
        query_parts.append(f"({name_conditions})")

        # 客戶類型過濾
        if customer_type:
            customer_keywords = customer_type.split()
            customer_conditions = " or ".join([f"name contains '{kw}'" for kw in customer_keywords])
            query_parts.append(f"({customer_conditions})")

        # 應用類型過濾
        if application_type:
            app_keywords = application_type.split()
            app_conditions = " or ".join([f"name contains '{kw}'" for kw in app_keywords])
            query_parts.append(f"({app_conditions})")

        # 組合查詢
        query = " and ".join(query_parts)

        try:
            results = self.drive_client.service.files().list(
                q=query,
                pageSize=max_results,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, parents)",
                orderBy="modifiedTime desc"
            ).execute()

            files = results.get('files', [])
            self.proposal_files = files

            print(f"🔍 找到 {len(files)} 個相關的服務建議書檔案")
            for file in files[:5]:  # 只顯示前5個
                print(f"  - {file['name']} ({file['modifiedTime'][:10]})")

            return files

        except Exception as e:
            print(f"❌ 搜尋檔案失敗: {e}")
            return []

    def download_file_content(self, file_id: str, file_name: str) -> Optional[str]:
        """
        下載檔案內容並提取文字

        Args:
            file_id: Google Drive 檔案 ID
            file_name: 檔案名稱 (用於確定檔案類型)

        Returns:
            提取的文字內容，如果失敗則返回 None
        """
        try:
            # 建立下載請求
            request = self.drive_client.service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)

            # 下載檔案
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"📥 下載進度: {int(status.progress() * 100)}%")

            file_content.seek(0)

            # 根據檔案類型提取文字
            if file_name.lower().endswith('.docx'):
                return self._extract_docx_content(file_content)
            elif file_name.lower().endswith('.pdf'):
                return self._extract_pdf_content(file_content)
            else:
                print(f"❌ 不支援的檔案格式: {file_name}")
                return None

        except Exception as e:
            print(f"❌ 下載檔案失敗: {e}")
            return None

    def _extract_docx_content(self, file_content: io.BytesIO) -> str:
        """從 DOCX 檔案提取文字內容"""
        try:
            from docx import Document

            # 儲存到臨時檔案
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(file_content.getvalue())
                temp_path = temp_file.name

            # 讀取 Word 文件
            doc = Document(temp_path)

            # 提取所有段落文字
            content_lines = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    # 保留標題階層資訊
                    style_name = paragraph.style.name
                    if style_name in ['Heading 1', 'Heading 2', 'Heading 3', 'Title']:
                        level = 1
                        if 'Heading' in style_name:
                            try:
                                level = int(style_name.split()[1])
                            except:
                                level = 1
                        content_lines.append(f"[H{level}]{paragraph.text.strip()}")
                    else:
                        content_lines.append(paragraph.text.strip())

            # 清理臨時檔案
            os.unlink(temp_path)

            return '\n'.join(content_lines)

        except Exception as e:
            print(f"❌ 讀取 DOCX 檔案失敗: {e}")
            return ""

    def _extract_pdf_content(self, file_content: io.BytesIO) -> str:
        """從 PDF 檔案提取文字內容"""
        try:
            import PyPDF2

            # 建立 PDF 讀取器
            pdf_reader = PyPDF2.PdfReader(file_content)

            # 提取所有頁面的文字
            content_lines = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text.strip():
                    content_lines.extend(text.split('\n'))

            return '\n'.join(content_lines)

        except Exception as e:
            print(f"❌ 讀取 PDF 檔案失敗: {e}")
            return ""

    def build_rag_database(self,
                          customer_type: Optional[str] = None,
                          application_type: Optional[str] = None,
                          max_files: int = 5) -> Dict[str, str]:
        """
        建立 RAG 資料庫 - 搜尋並下載相關的服務建議書內容

        Args:
            customer_type: 客戶類型
            application_type: 應用類型
            max_files: 最多處理的檔案數量

        Returns:
            文件名稱到內容的映射字典
        """
        print(f"🔍 搜尋相關的服務建議書 (客戶: {customer_type}, 應用: {application_type})...")

        # 搜尋相關檔案
        files = self.search_proposal_files(customer_type, application_type, max_files)

        if not files:
            print("⚠️ 未找到相關的服務建議書檔案")
            return {}

        # 下載並處理檔案內容
        rag_database = {}
        processed_count = 0

        for file in files:
            if processed_count >= max_files:
                break

            file_id = file['id']
            file_name = file['name']

            print(f"📖 處理檔案: {file_name}")

            content = self.download_file_content(file_id, file_name)
            if content and len(content.strip()) > 100:  # 確保內容不為空
                rag_database[file_name] = content
                processed_count += 1
                print(f"✅ 已處理 {file_name} ({len(content)} 字符)")
            else:
                print(f"⚠️ 跳過 {file_name} (內容太少或無法讀取)")

        print(f"📚 RAG 資料庫建立完成，共 {len(rag_database)} 個參考文件")
        return rag_database

def initialize_drive_client(credentials_path: str = 'credentials.json') -> Optional[GoogleDriveClient]:
    """
    初始化 Google Drive 客戶端

    Args:
        credentials_path: credentials.json 檔案路徑

    Returns:
        GoogleDriveClient 實例，如果失敗則返回 None
    """
    try:
        return GoogleDriveClient(credentials_path)
    except Exception as e:
        print(f"❌ Google Drive 認證失敗: {e}")
        print("請確認：")
        print("1. 已下載 credentials.json 並放置在專案目錄")
        print("2. 已啟用 Google Drive API")
        print("3. 已設定正確的 OAuth 同意畫面")
        return None

def create_proposal_search_engine(drive_client: GoogleDriveClient) -> ProposalSearchEngine:
    """
    建立服務建議書搜尋引擎

    Args:
        drive_client: GoogleDriveClient 實例

    Returns:
        ProposalSearchEngine 實例
    """
    return ProposalSearchEngine(drive_client)
