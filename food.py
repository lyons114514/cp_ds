import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF8F00; /* 橙色 */
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px #ccc;
    }
    .metric-card {
        background-color: #FFF3E0; /* 浅橙色背景 */
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 5px solid #FF8F00; /* 橙色边框 */
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #EF6C00; /* 深橙色 */
    }
    .metric-label {
        font-size: 0.95rem;
        color: #555;
        margin-top: 0.3rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px; /* 减小标签间距 */
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F5F5F5; /* 标签背景色 */
        border-radius: 4px 4px 0px 0px;
        padding: 10px 15px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFF3E0; /* 选中标签背景色 */
        border-bottom: 3px solid #FF8F00; /* 选中标签下边框 */
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_food_ai_data():
    try:
        data = pd.read_csv('data/food_ai_data.csv', index_col='Year')
        return data
    except FileNotFoundError:
        st.error("找不到数据文件：data/food_ai_data.csv")
        return None

# 修改数据读取部分
df_food = load_food_ai_data()
if df_food is None:
    st.stop()
latest_year_food = df_food.index.max()
latest_data_food = df_food.loc[latest_year_food]

# 标题
st.markdown("<h1 class='main-header'>AI赋能食品产业：安全、便捷与效率</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- 关键指标展示 ---
st.subheader(f"关键进展 ({latest_year_food}年)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{latest_data_food['Traceability_Coverage']}%</div>
        <div class="metric-label">主要食品品类溯源覆盖率</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">-{latest_data_food['Avg_Delivery_Time_Reduction']}%</div>
        <div class="metric-label">外卖平均配送时长缩短 (AI调度)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{latest_data_food['Pest_Detection_Accuracy']}%</div>
        <div class="metric-label">AI病虫害识别准确率 (智慧农业)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{latest_data_food['Smart_Fridge_Penetration']}%</div>
        <div class="metric-label">智能冰箱市场渗透率</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 创建选项卡 ---
tab_safety, tab_delivery, tab_agri, tab_kitchen, tab_summary = st.tabs([
    "🛡️ 食品安全 (Safety)",
    "🚀 便捷配送 (Convenience)",
    "🌿 智慧农业 (Efficiency)",
    "🍳 智能厨房 (Convenience)",
    "💡 总结洞察 (Summary)"
])

# --- Tab 1: 食品安全 ---
with tab_safety:
    st.subheader("食品安全溯源体系建设")
    col1, col2 = st.columns(2)
    with col1:
        fig_trace_cov = px.line(df_food, y='Traceability_Coverage', markers=True,
                               title="主要食品品类溯源系统覆盖率 (%)",
                               labels={'value': '覆盖率 (%)', 'Year': '年份'})
        st.plotly_chart(fig_trace_cov, use_container_width=True)
        st.markdown("*   基于区块链、二维码等技术，溯源覆盖率稳步提升。")
    with col2:
        fig_trust = px.line(df_food, y='Consumer_Trust_Index', markers=True,
                           title="消费者对可溯源食品的信任度指数 (基准100)",
                           labels={'value': '信任指数', 'Year': '年份'})
        st.plotly_chart(fig_trust, use_container_width=True)
        st.markdown("*   溯源系统提升了消费者信心。")

    st.subheader("AI在食品安全中的作用 (数据分析)")
    fig_warning = px.line(df_food, y='Disease_Warning_Improvement', markers=True,
                         title="大数据分析对食源性疾病预警准确率的提升 (%)",
                         labels={'value': '准确率提升 (%)', 'Year': '年份'})
    st.plotly_chart(fig_warning, use_container_width=True)
    st.markdown("""
    *   **AI角色**: 虽然直接的AI检测应用仍在发展，但AI在 **大数据分析** 方面作用显著。通过分析溯源数据、市场流通数据、舆情信息等，AI可以：
        *   **预测风险**: 提前识别潜在的食品安全风险区域或环节。
        *   **精准预警**: 提高食源性疾病爆发的预警准确性和时效性。
        *   **优化监管**: 帮助监管部门更有效地分配资源，进行精准抽检。
    *   **技术基础**: 区块链、物联网传感器提供了可靠的数据源，AI负责从海量数据中挖掘价值，提升整体食品安全保障水平。
    """)

# --- Tab 2: 便捷配送 ---
with tab_delivery:
    st.subheader("AI驱动的外卖与即时零售效率提升")
    col1, col2 = st.columns(2)
    with col1:
        fig_dispatch = px.line(df_food, y='AI_Dispatch_Adoption', markers=True,
                              title="外卖平台AI智能调度系统渗透率 (%)",
                              labels={'value': '渗透率 (%)', 'Year': '年份'})
        st.plotly_chart(fig_dispatch, use_container_width=True)
        st.markdown(f"*   主流平台AI调度渗透率已达 **{latest_data_food['AI_Dispatch_Adoption']}%**。")
    with col2:
        fig_time_reduct = px.line(df_food, y='Avg_Delivery_Time_Reduction', markers=True,
                                 title="AI调度带来的平均配送时长缩短率 (%)",
                                 labels={'value': '时长缩短率 (%)', 'Year': '年份'})
        st.plotly_chart(fig_time_reduct, use_container_width=True)
        st.markdown(f"*   智能路径规划、订单合并使配送效率显著提升，时长缩短 **{latest_data_food['Avg_Delivery_Time_Reduction']}%**。")

    st.subheader("无人配送探索与市场发展")
    col1, col2 = st.columns(2)
    with col1:
        fig_unmanned = px.bar(df_food, y='Unmanned_Delivery_Cities',
                             title="无人配送 (车/机器人) 试点城市数量",
                             labels={'value': '城市数量', 'Year': '年份'})
        fig_unmanned.update_traces(marker_color='#FFB74D') # 橙色柱状图
        st.plotly_chart(fig_unmanned, use_container_width=True)
        st.markdown("*   无人配送技术在特定场景（园区、社区）逐步落地试点。")
    with col2:
        fig_market_del = px.area(df_food, y='Delivery_Market_Size_CNY',
                                title="中国外卖与即时零售市场规模 (万亿人民币)",
                                labels={'value': '市场规模 (万亿)', 'Year': '年份'}, markers=True)
        # Convert Trillion to Billion for axis label if needed
        fig_market_del.update_yaxes(title_text="市场规模 (万亿人民币)")
        st.plotly_chart(fig_market_del, use_container_width=True)
        st.markdown(f"*   市场规模持续增长至 **{latest_data_food['Delivery_Market_Size_CNY']:.2f} 万亿** 人民币。")

    st.markdown("""
    **AI核心作用**:
    *   **效率核心**: AI智能调度是外卖平台的核心竞争力，通过实时数据分析，动态优化骑手路径、订单分配，极大提升配送效率，降低运营成本。
    *   **未来探索**: 无人配送依赖于AI的自主导航、避障和环境感知能力。
    """)

# --- Tab 3: 智慧农业 ---
with tab_agri:
    st.subheader("AI在农业生产中的应用与效率提升")
    col1, col2 = st.columns(2)
    with col1:
        fig_pest = px.line(df_food, y='Pest_Detection_Accuracy', markers=True,
                          title="AI视觉病虫害识别准确率 (%)",
                          labels={'value': '准确率 (%)', 'Year': '年份'})
        st.plotly_chart(fig_pest, use_container_width=True)
        st.markdown(f"*   基于无人机或地面设备的图像识别准确率达 **{latest_data_food['Pest_Detection_Accuracy']}%**。")
    with col2:
        fig_water = px.line(df_food, y='Water_Saving_Rate', markers=True,
                           title="精准灌溉系统平均节水率 (%)",
                           labels={'value': '节水率 (%)', 'Year': '年份'})
        st.plotly_chart(fig_water, use_container_width=True)
        st.markdown(f"*   AI分析土壤、气象数据，指导精准灌溉，节水率达 **{latest_data_food['Water_Saving_Rate']}%**。")

    st.subheader("自动化与市场发展")
    col1, col2 = st.columns(2)
    with col1:
        fig_harvest = px.line(df_food, y='Automated_Harvesting_Rate', markers=True,
                             title="自动化采摘在高价值作物中应用比例 (%)",
                             labels={'value': '应用比例 (%)', 'Year': '年份'})
        st.plotly_chart(fig_harvest, use_container_width=True)
        st.markdown("*   自动化采摘技术难度高，目前应用比例仍较低，是未来发展方向。")
    with col2:
        fig_market_agri = px.area(df_food, y='Smart_Agri_Market_Size_CNY',
                                 title="中国智慧农业市场规模 (千亿人民币)",
                                 labels={'value': '市场规模 (千亿)', 'Year': '年份'}, markers=True)
        fig_market_agri.update_yaxes(title_text="市场规模 (千亿人民币)")
        st.plotly_chart(fig_market_agri, use_container_width=True)
        st.markdown(f"*   智慧农业市场稳步增长，规模达 **{latest_data_food['Smart_Agri_Market_Size_CNY']:.2f} 千亿** 人民币。")

    st.markdown("""
    **AI核心作用**:
    *   **精准化**: AI替代人眼进行病虫害识别，分析数据实现精准水肥管理，提高资源利用率。
    *   **自动化**: 驱动采摘机器人等自动化设备，解决农业劳动力短缺问题（仍处于早期）。
    *   **预测性**: 分析气象、土壤、作物生长数据，预测产量和病害风险。
    """)

# --- Tab 4: 智能厨房 ---
with tab_kitchen:
    st.subheader("智能厨房电器市场渗透与增长")
    col1, col2 = st.columns(2)
    with col1:
        fig_fridge = px.line(df_food, y='Smart_Fridge_Penetration', markers=True,
                            title="智能冰箱市场渗透率 (%)",
                            labels={'value': '渗透率 (%)', 'Year': '年份'})
        st.plotly_chart(fig_fridge, use_container_width=True)
        st.markdown(f"*   智能冰箱渗透率逐步提升至 **{latest_data_food['Smart_Fridge_Penetration']}%**。")
    with col2:
        fig_robot_growth = px.bar(df_food, y='Cooking_Robot_Sales_Growth',
                                 title="智能烹饪设备年销售额增长率 (%)",
                                 labels={'value': '增长率 (%)', 'Year': '年份'})
        fig_robot_growth.update_traces(marker_color='#FFA726') # 橙色柱状图
        st.plotly_chart(fig_robot_growth, use_container_width=True)
        st.markdown("*   智能烹饪设备市场处于高速增长期后趋于平稳。")

    st.subheader("市场规模")
    fig_market_kitchen = px.area(df_food, y='Smart_Kitchen_Market_Size_CNY',
                                title="中国智能厨房电器市场规模 (千亿人民币)",
                                labels={'value': '市场规模 (千亿)', 'Year': '年份'}, markers=True)
    fig_market_kitchen.update_yaxes(title_text="市场规模 (千亿人民币)")
    st.plotly_chart(fig_market_kitchen, use_container_width=True)
    st.markdown(f"*   智能厨房电器市场规模已达 **{latest_data_food['Smart_Kitchen_Market_Size_CNY']:.2f} 千亿** 人民币。")

    st.markdown("""
    **AI核心作用**:
    *   **便捷性**: 智能冰箱通过图像识别管理食材、AI推荐食谱；烹饪机器人自动执行菜单。
    *   **个性化**: 基于用户饮食习惯和健康数据，提供个性化的饮食建议和烹饪方案。
    *   **互联互通**: 作为智能家居的一部分，实现厨房电器的互联和智能控制。
    """)

# --- Tab 5: 总结洞察 ---
with tab_summary:
    st.subheader("AI在食品领域的赋能总结：聚焦安全、便捷与效率")

    st.markdown("""
    人工智能正在深刻地改变着食品产业的各个环节，其核心价值体现在提升**食品安全**保障水平、增加消费**便捷性**以及优化生产和流通**效率**。

    **1. 保障食品安全 (Safety):**
    *   **数据驱动的风险防控:** AI虽然不直接参与检测（目前主流仍是传统检测技术），但其强大的 **数据分析能力** 是关键。通过整合分析溯源数据、流通数据、消费反馈、舆情信息等，AI能有效 **预测潜在风险**、**提升食源性疾病预警准确率** (提升约 `{latest_data_food['Disease_Warning_Improvement']}%`)，并辅助 **精准监管**。
    *   **透明度提升:** 区块链等技术保证了数据的不可篡改，结合AI分析，提升了从农田到餐桌的 **透明度**，增强了消费者信心 (信任指数提升至 `{latest_data_food['Consumer_Trust_Index']:.1f}`)。

    **2. 提升消费便捷性 (Convenience):**
    *   **极致的即时配送:** 外卖和即时零售的繁荣离不开 **AI智能调度系统**。该系统实时优化配送路径，显著 **缩短配送时间** (平均缩短 `{latest_data_food['Avg_Delivery_Time_Reduction']}%`)，提升用户体验。无人配送是AI在末端配送便捷性上的未来探索方向。
    *   **智能化的家庭厨房:** 智能冰箱利用 **图像识别** 管理食材、**AI推荐** 健康食谱；烹饪机器人则致力于实现 **自动化烹饪**，解放用户双手，提升居家烹饪的便捷度和趣味性 (智能冰箱渗透率达 `{latest_data_food['Smart_Fridge_Penetration']}%`)。

    **3. 优化生产与流通效率 (Efficiency):**
    *   **智慧农业精准高效:** 在农业生产端，AI视觉技术用于 **病虫害精准识别** (准确率 `{latest_data_food['Pest_Detection_Accuracy']}%`)，结合传感器数据分析实现 **精准水肥管理** (节水率 `{latest_data_food['Water_Saving_Rate']}%`)，提升资源利用效率和作物产量。自动化采摘等技术也在逐步发展。
    *   **供应链优化:** AI也可应用于食品供应链管理，通过 **需求预测** 减少库存浪费，优化 **物流网络** 降低运输成本。

    **总结:** AI并非万能药，但在食品领域，它正扮演着越来越重要的 **"赋能者"** 角色。通过与物联网、大数据、机器人等技术结合，AI有效解决了食品安全中的信息不对称问题，提升了即时消费的便捷性，并推动了农业生产和食品流通的效率革命。未来，随着技术的进一步成熟，AI将在个性化营养、新型食品研发、可持续农业等方面带来更多创新。
    """)

# --- 页脚 ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>数据来源: 模拟数据，基于行业公开信息与发展趋势 | 更新时间: 2024年</div>", unsafe_allow_html=True)