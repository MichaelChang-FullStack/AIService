from docx import Document
import os

def extract_headings(docx_path):
    # 若本地有 docx 就讀取並剖析 heading，否則返回空
    if not os.path.exists(docx_path):
        return []
    doc = Document(docx_path)
    headings = []
    for para in doc.paragraphs:
        if para.style.name in ['Heading 1', 'Heading 2']:
            headings.append((para.style.name, para.text.strip()))
    return headings

def get_sample_headings():
    # 回傳 mock 樣板結構
    return [
        ('Heading 1', '專案說明'),
        ('Heading 1', '目標與需求'),
        ('Heading 1', '解決方案架構'),
        ('Heading 1', '預期效益'),
        ('Heading 1', '時程與報價'),
        ('Heading 1', '維護與服務')
    ]

def merge_heading_structures(list_of_headings):
    # 快速合併必有標題名單（demo 只保留全部出現項）
    if not list_of_headings or all(len(hs) == 0 for hs in list_of_headings):
        return [t[1] for t in get_sample_headings()]
    from collections import Counter
    all_titles = [h[1] for headings in list_of_headings for h in headings]
    most_common = [t for t, c in Counter(all_titles).most_common()]
    return most_common or [t[1] for t in get_sample_headings()]
