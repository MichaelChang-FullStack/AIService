import os
import streamlit as st
from docx_analyzer import extract_headings, merge_heading_structures, get_sample_headings
from proposal_writer import gpt_generate, write_proposal_docx
from file_reader import extract_template_info

st.title("🤖 AI 服務建議書生成器")

# 文件上傳區域
st.header("📄 選擇範本文件")
st.write("上傳現有的服務建議書作為範本（支援 .docx 和 .pdf 文件）")

uploaded_file = st.file_uploader(
    "選擇範本文件",
    type=['docx', 'pdf'],
    help="上傳您想要作為範本的服務建議書文件，系統會分析其結構並生成類似內容"
)

template_content = None
template_analyzer = None
template_file_type = None
outline_titles = []

if uploaded_file is not None:
    # 保存上傳的文件到臨時位置
    temp_path = f"temp_template.{uploaded_file.name.split('.')[-1]}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    try:
        # 讀取和分析範本文件
        with st.spinner('正在分析範本文件...'):
            template_content, template_analyzer, template_file_type = extract_template_info(temp_path)

        st.success(f"✅ 成功讀取範本文件（{template_file_type.upper()}）")

        # 從範本中提取原始標題（完全遵照範本的標題順序）
        original_headings = template_analyzer.get_original_headings() if template_analyzer else []
        outline_titles = [heading['text'] for heading in original_headings] if original_headings else []

        if not outline_titles:
            # 如果無法提取標題，使用備用分析結果
            outline_titles = template_analyzer.get_section_titles() if template_analyzer else []
            if not outline_titles:
                # 如果完全無法分析，使用預設結構
                outline_titles = [t[1] for t in get_sample_headings()]
                st.warning("⚠️ 無法從範本提取標題，將使用預設章節")
            else:
                st.info(f"📝 使用分析出的 {len(outline_titles)} 個標題")

        if original_headings:
            st.success(f"✅ 已載入範本的 {len(outline_titles)} 個標題，將完全遵照範本結構")
        else:
            st.info(f"📝 已載入 {len(outline_titles)} 個標題")

        # 顯示範本分析結果
        with st.expander("📊 範本分析結果", expanded=True):
            st.write("**將使用的標題結構：**")

            if original_headings:
                st.success("🎯 以下 H1 和 H2 標題將作為目錄標題使用：")

                # 只顯示 H1 和 H2 標題
                h1_h2_headings = [h for h in original_headings if h['level'] <= 2]
                for i, heading in enumerate(h1_h2_headings, 1):
                    level_indicator = "📌" if heading['level'] == 1 else "├─"
                    st.write(f"{i}. {level_indicator} **{heading['text']}** (Heading {heading['level']}, {heading['source']})")

                st.info("💡 系統只使用 H1 和 H2 標題作為目錄，避免過多細項標題。內容將根據新客戶需求進行改寫。")

                # 統計信息（只統計 H1 和 H2）
                h1_count = sum(1 for h in h1_h2_headings if h['level'] == 1)
                h2_count = sum(1 for h in h1_h2_headings if h['level'] == 2)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("主要標題 (H1)", h1_count)
                with col2:
                    st.metric("子標題 (H2)", h2_count)
            else:
                # 備用顯示
                st.warning("⚠️ 無法提取原始標題順序，顯示分析結果：")

                detailed_analysis = template_analyzer.get_detailed_analysis() if template_analyzer else []

                if detailed_analysis:
                    # 創建表格顯示分析結果
                    analysis_data = []
                    for item in detailed_analysis:
                        analysis_data.append({
                            '章節標題': item['title'],
                            '階層等級': item['hierarchy'],
                            '識別來源': item['source'],
                            '內容長度': f"{item['content_length']} 字符",
                            '內容預覽': item['content_preview'][:50] + "..." if len(item['content_preview']) > 50 else item['content_preview']
                        })

                    st.dataframe(analysis_data, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 讀取範本文件失敗: {e}")
        st.info("將使用預設章節結構繼續")
        template_content = None
        template_analyzer = None
        template_file_type = "default"
        original_headings = []
        outline_titles = [t[1] for t in get_sample_headings()]
    finally:
        # 清理臨時文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
else:
    # 沒有上傳範本時，使用預設結構
    st.info("ℹ️ 未上傳範本文件，將使用預設章節結構")
    outline_titles = [t[1] for t in get_sample_headings()]

st.header("📝 客戶需求設定")

st.write('請填寫新客戶需求與專案基本資訊：')
customer = st.text_input('客戶名稱/單位', 'XXX公司')
project_type = st.selectbox('專案類型', ['AI', '系統整合', '數據分析', 'CRM', '其它'])
customer_need = st.text_area('請描述專案需求(可多行)',
                           '協助搭建AI驅動數據平台，整合現有系統，提供即時分析和預測功能...',
                           height=100)

# 檢查 API 狀態
api_status = "✅ 可用" if os.getenv('GOOGLE_API_KEY') else "⚠️ 未設定 API Key"
st.info(f"**AI 模型狀態**: {api_status} (使用 Gemini AI)")

# 顯示當前設定摘要
st.subheader("📋 生成設定摘要")

if template_content and template_analyzer:
    original_headings = template_analyzer.get_original_headings()
    if original_headings:
        st.success("🎯 將使用範本的確切標題結構")
        with st.expander("查看將使用的標題列表", expanded=False):
            for i, heading in enumerate(original_headings, 1):
                st.write(f"{i}. **{heading['text']}** (Heading {heading['level']})")
    else:
        st.info("📝 使用分析出的標題結構")

col1, col2 = st.columns(2)
with col1:
    if template_content:
        st.success("✅ 已載入範本文件")
        st.write(f"**範本類型**: {template_file_type.upper()}")
        st.write(f"**標題數量**: {len(outline_titles)}")
    else:
        st.info("📝 使用預設結構")

with col2:
    st.write(f"**客戶**: {customer}")
    st.write(f"**專案類型**: {project_type}")
    st.write(f"**AI 狀態**: {api_status}")

if st.button('🚀 產生專屬建議書', type='primary'):
    if not customer.strip():
        st.error("❌ 請輸入客戶名稱")
        st.stop()

    if not customer_need.strip():
        st.error("❌ 請描述專案需求")
        st.stop()

    with st.spinner('🤖 AI 正在根據範本生成內容中...'):
        # 準備範本信息
        template_sections = None
        if template_analyzer:
            template_sections = template_analyzer.sections

        # 為每個 outline_title 找到對應的範本內容
        template_sections_for_titles = {}
        if template_analyzer:
            for title in outline_titles:
                # 嘗試精確匹配
                if title in template_sections:
                    template_sections_for_titles[title] = template_sections[title]
                else:
                    # 如果沒有精確匹配，嘗試模糊匹配
                    best_match = None
                    best_score = 0
                    for section_title, content in template_sections.items():
                        # 簡單的相似度計算：共同詞彙數量
                        title_words = set(title.split())
                        section_words = set(section_title.split())
                        common_words = title_words.intersection(section_words)
                        score = len(common_words)
                        if score > best_score:
                            best_score = score
                            best_match = content
                    if best_match:
                        template_sections_for_titles[title] = best_match
                    else:
                        # 如果還是沒有匹配，使用預設內容
                        template_sections_for_titles[title] = "根據客戶需求提供專業服務內容"

        # 生成內容
        proposal_raw = gpt_generate(
            outline_titles,
            customer_need,
            template_content=template_content,
            template_sections=template_sections_for_titles
        )

        # 檢查是否為模擬內容
        is_mock_content = "模擬內容" in proposal_raw
        if is_mock_content:
            st.warning("🔄 目前使用模擬內容生成。如需 AI 生成，請設定 Google API Key 或升級免費額度。")
        else:
            st.success("🎉 已使用 Gemini AI 根據範本生成專業內容！")

        # 解析生成內容
        content_blocks = []
        if proposal_raw.strip():
            # 嘗試按章節拆分內容
            sections = proposal_raw.split('\n\n')
            for section in sections:
                if section.strip():
                    content_blocks.append(section.strip())

            # 如果拆分後的區塊數量少於章節數量，用最後的區塊填充
            while len(content_blocks) < len(outline_titles):
                content_blocks.append("根據客戶需求和範本分析，此章節內容將在專案細節確認後補充。")
        else:
            content_blocks = ['AI自動產生內容' for _ in outline_titles]

        # 生成文件名和保存
        filename = f'{customer}_{project_type}_建議書.docx'
        save_path = os.path.join('.', filename)

        # 傳遞範本文件路徑以複製格式
        template_file_path = None
        if uploaded_file:
            # 重新創建臨時文件路徑，因為原來的可能已被刪除
            temp_path = f"temp_template_{hash(uploaded_file.name)}.{uploaded_file.name.split('.')[-1]}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            template_file_path = temp_path

        write_proposal_docx(save_path, outline_titles, content_blocks, template_analyzer, template_file_path)

        # 清理臨時文件
        if template_file_path and os.path.exists(template_file_path):
            try:
                os.remove(template_file_path)
            except:
                pass

        st.success(f'✅ 已產生專屬建議書: {filename}')

        # 下載按鈕
        with open(save_path, 'rb') as f:
            st.download_button(
                label='📥 下載建議書 Word 文件',
                data=f,
                file_name=filename,
                mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                type='primary'
            )

        # 提供額度相關資訊
        if is_mock_content:
            st.info("""
            **💡 升級建議：**
            - 前往 [Google AI Studio](https://aistudio.google.com/) 升級付費方案
            - 或等待每日免費額度重置
            - 設定環境變數：`$env:GOOGLE_API_KEY="您的金鑰"`
            """)
        else:
            st.balloons()
            st.info('🎯 建議書已生成！可根據需要進一步修改或聯繫我們討論專案細節。')

# 添加說明區域
with st.expander("❓ 使用說明", expanded=False):
    st.markdown("""
    ### 📖 如何使用

    1. **上傳範本**：選擇現有的服務建議書文件（.docx 或 .pdf）作為範本
    2. **分析結構**：系統會自動分析範本的章節結構
    3. **設定需求**：輸入客戶信息和專案需求
    4. **生成建議書**：AI 會根據範本結構生成類似內容，但針對新客戶需求進行調整

    ### 🎯 功能特色

    - **智慧分析**：自動識別服務建議書的章節結構
    - **內容改寫**：根據新需求調整範本內容，保持專業風格
    - **多格式支援**：支援 Word 和 PDF 格式的範本文件
    - **AI 優化**：使用 Gemini AI 確保內容品質和相關性

    ### 🔧 技術支援

    如遇到問題，請檢查：
    - 文件格式是否正確
    - API Key 是否正確設定
    - 網路連線是否正常
    """)