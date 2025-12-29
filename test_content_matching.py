#!/usr/bin/env python3
"""
測試內容匹配邏輯
"""
import os
from file_reader import extract_template_info

def test_content_matching():
    """測試內容匹配功能"""

    print('🔍 測試內容匹配邏輯...')

    try:
        # 載入範本
        content, analyzer, file_type = extract_template_info('sample_proposal_template.docx')
        print(f'✅ 成功載入範本文件 ({file_type})')

        # 獲取所有原始標題
        all_headings = analyzer.get_original_headings()
        print(f'📊 原始標題總數: {len(all_headings)}')

        # 過濾 H1 和 H2 標題
        h1_h2_headings = [h for h in all_headings if h['level'] <= 2]
        outline_titles = [h['text'] for h in h1_h2_headings]
        print(f'🎯 H1+H2 標題數: {len(outline_titles)}')

        # 獲取範本章節內容
        template_sections = analyzer.sections
        print(f'📝 範本章節數: {len(template_sections)}')

        # 測試內容匹配邏輯
        template_sections_for_titles = {}
        matched_count = 0

        print('\n🔗 內容匹配結果:')
        for title in outline_titles:
            if title in template_sections:
                template_sections_for_titles[title] = template_sections[title]
                content_length = len(template_sections[title])
                print(f'✅ {title}: {content_length} 字 (精確匹配)')
                matched_count += 1
            else:
                # 模糊匹配邏輯
                best_match = None
                best_score = 0
                for section_title, content in template_sections.items():
                    title_words = set(title.split())
                    section_words = set(section_title.split())
                    common_words = title_words.intersection(section_words)
                    score = len(common_words)
                    if score > best_score:
                        best_score = score
                        best_match = content

                if best_match:
                    template_sections_for_titles[title] = best_match
                    content_length = len(best_match)
                    print(f'⚠️ {title}: {content_length} 字 (模糊匹配，相似度: {best_score})')
                    matched_count += 1
                else:
                    template_sections_for_titles[title] = "根據客戶需求提供專業服務內容"
                    print(f'❌ {title}: 使用預設內容')

        print(f'\n📈 匹配統計:')
        print(f'總標題數: {len(outline_titles)}')
        print(f'成功匹配: {matched_count}')
        print(f'匹配率: {matched_count/len(outline_titles)*100:.1f}%')

        # 顯示前3個標題的內容預覽
        print(f'\n📖 內容預覽 (前3個):')
        for i, title in enumerate(outline_titles[:3]):
            content = template_sections_for_titles[title]
            preview = content[:100] + "..." if len(content) > 100 else content
            print(f'{i+1}. {title}:')
            print(f'   {preview}')
            print()

        print('✅ 內容匹配邏輯測試完成！')

    except Exception as e:
        print(f'❌ 測試失敗: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_content_matching()
