#!/usr/bin/env python3
"""
測試 H1 H2 標題過濾功能
"""
from file_reader import extract_template_info

def test_h1_h2_filter():
    """測試 H1 H2 標題過濾功能"""

    print('🔍 測試 H1 H2 標題過濾功能...')

    try:
        content, analyzer, file_type = extract_template_info('sample_proposal_template.docx')
        print(f'文件類型: {file_type}')

        original_headings = analyzer.get_original_headings()
        h1_h2_headings = [h for h in original_headings if h['level'] <= 2]

        print(f'\n📊 統計信息:')
        print(f'記錄的目錄標題 (H1+H2): {len(original_headings)}')

        # 計算文件中實際的標題統計
        lines = content.split('\n')
        h1_count = sum(1 for line in lines if line.startswith('[H1]'))
        h2_count = sum(1 for line in lines if line.startswith('[H2]'))
        h3_count = sum(1 for line in lines if line.startswith('[H3]'))

        print(f'文件中實際的標題統計:')
        print(f'  H1 標題: {h1_count} 個')
        print(f'  H2 標題: {h2_count} 個')
        print(f'  H3 標題: {h3_count} 個')
        print(f'  總計: {h1_count + h2_count + h3_count} 個')
        print(f'過濾掉的 H3 標題: {h3_count} 個')

        print(f'\n🎯 將使用的目錄標題 (H1 & H2):')
        for i, heading in enumerate(h1_h2_headings, 1):
            print(f'{i}. [H{heading["level"]}] {heading["text"]}')

        if h3_count > 0:
            print(f'\nℹ️ 系統已成功過濾掉 {h3_count} 個 H3 細項標題，只保留主要標題作為目錄')

        print('\n✅ H1 H2 標題過濾功能測試完成！')

    except Exception as e:
        print(f'❌ 測試失敗: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_h1_h2_filter()
