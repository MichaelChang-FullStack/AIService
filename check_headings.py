#!/usr/bin/env python3
"""
檢查 Word 文件中的標題等級
"""
from file_reader import extract_template_info

def check_headings():
    """檢查實際讀取的標題等級"""

    print('🔍 檢查實際讀取的標題等級...')

    try:
        content, analyzer, file_type = extract_template_info('sample_proposal_template.docx')
        original_headings = analyzer.get_original_headings()

        print(f'總共發現 {len(original_headings)} 個標題:')
        for i, heading in enumerate(original_headings, 1):
            print(f'{i}. 標題: "{heading["text"]}", 等級: H{heading["level"]}, 來源: {heading["source"]}')

        h1_count = sum(1 for h in original_headings if h['level'] == 1)
        h2_count = sum(1 for h in original_headings if h['level'] == 2)
        h3_count = sum(1 for h in original_headings if h['level'] == 3)

        print("\n📊 統計:")
        print(f'H1 標題: {h1_count} 個')
        print(f'H2 標題: {h2_count} 個')
        print(f'H3 標題: {h3_count} 個')

        h1_h2_filtered = [h for h in original_headings if h['level'] <= 2]
        print(f'\n🎯 過濾後 (H1+H2): {len(h1_h2_filtered)} 個標題')
        print(f'過濾掉: {len(original_headings) - len(h1_h2_filtered)} 個 H3+ 標題')

    except Exception as e:
        print(f'❌ 錯誤: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_headings()
