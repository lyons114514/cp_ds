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
        color: #1E88E5; /* 深蓝色 */
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px #ccc;
    }
    .metric-card {
        background-color: #f9f9f9;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 5px solid #1E88E5;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 0.95rem;
        color: #555;
        margin-top: 0.3rem;
    }
    .stTabs [data-baseweb="tab-list"] {
		gap: 24px;
	}
    .stTabs [data-baseweb="tab"] {
		height: 50px;
        white-space: pre-wrap;
		background-color: #F0F2F6;
		border-radius: 4px 4px 0px 0px;
		gap: 1px;
		padding-top: 10px;
		padding-bottom: 10px;
    }
	.stTabs [aria-selected="true"] {
  		background-color: #FFFFFF;
	}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_drone_data():
    try:
        data = pd.read_csv('data/drone_data.csv', index_col='Year')
        return data
    except FileNotFoundError:
        st.error("找不到数据文件：data/drone_data.csv")
        return None

# 修改数据读取部分
df = load_drone_data()
if df is None:
    st.stop()
latest_year = df.index.max()
latest_data = df.loc[latest_year]

# 标题
st.markdown("<h1 class='main-header'>中国无人机产业领导力与AI赋能分析</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- 关键指标展示 ---
st.subheader(f"关键指标 ({latest_year}年)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{latest_data['DJI_Share_Total']}%</div>
        <div class="metric-label">中国无人机全球市场份额(估计)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">${latest_data['Global_Market_Total']} B</div>
        <div class="metric-label">全球无人机市场规模</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{latest_data['AI_Adoption_Rate']}%</div>
        <div class="metric-label">AI技术在无人机中渗透率</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">>5</div>
        <div class="metric-label">AI驱动的主要新兴应用领域</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 创建选项卡 ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 市场格局与领导力",
    "🤖 AI赋能与应用拓展",
    "🔗 产业链优势分析",
    "💡 结论与展望"
])

# --- Tab 1: 市场格局与领导力 ---
with tab1:
    st.subheader("全球无人机市场增长趋势")
    fig_market_size = px.area(df, y=['Global_Market_Consumer', 'Global_Market_Industrial'],
                              title="全球无人机市场规模 (消费级 vs 行业级, 十亿美元)",
                              labels={'value': '市场规模 (十亿美元)', 'variable': '市场类型', 'Year': '年份'},
                              markers=True)
    fig_market_size.update_layout(hovermode="x unified")
    st.plotly_chart(fig_market_size, use_container_width=True)
    st.markdown("""
    *   **行业级市场**成为增长主要驱动力，年复合增长率超过 **30%**。
    *   消费级市场趋于稳定，但仍保持一定规模。
    """)

    st.subheader("中国无人机市场份额主导地位")
    fig_market_share = px.line(df, y=['DJI_Share_Consumer', 'DJI_Share_Industrial', 'DJI_Share_Total'],
                              title="中国(以大疆为代表)在全球无人机市场份额 (%)",
                              labels={'value': '市场份额 (%)', 'variable': '市场类型', 'Year': '年份'},
                              markers=True)
    fig_market_share.update_traces(hovertemplate='年份: %{x}<br>市场份额: %{y:.1f}%')
    fig_market_share.update_layout(hovermode="x unified", yaxis_range=[40, 85])
    st.plotly_chart(fig_market_share, use_container_width=True)
    st.markdown(f"""
    *   中国企业在**消费级市场**占据绝对优势，份额稳定在 **{latest_data['DJI_Share_Consumer']}%** 左右。
    *   在**行业级市场**，尽管竞争加剧，中国企业凭借技术和成本优势，仍保持 **{latest_data['DJI_Share_Industrial']}%** 以上的主导地位。
    *   整体市场份额维持在 **{latest_data['DJI_Share_Total']}%** 以上，显示出强大的综合竞争力。
    """)

# --- Tab 2: AI赋能与应用拓展 ---
with tab2:
    st.subheader("AI技术在无人机领域的渗透加速")
    fig_ai_adoption = px.line(df, y='AI_Adoption_Rate',
                             title="AI技术在无人机中的渗透率 (%)",
                             labels={'value': '渗透率 (%)', 'Year': '年份'},
                             markers=True)
    fig_ai_adoption.update_layout(hovermode="x unified", yaxis_range=[0, 100])
    st.plotly_chart(fig_ai_adoption, use_container_width=True)
    st.markdown(f"""
    *   AI技术（计算机视觉、自主导航、路径规划、智能避障等）渗透率从2018年的约 **{df['AI_Adoption_Rate'].iloc[0]}%** 快速增长至2025年的 **{latest_data['AI_Adoption_Rate']}%**。
    *   AI是推动无人机从简单航拍工具向智能化作业平台转变的核心动力。
    """)

    st.subheader("AI驱动的应用领域市场增长")
    app_cols = ['App_Market_Agriculture', 'App_Market_Surveying', 'App_Market_Security', 'App_Market_Logistics', 'App_Market_Filming']
    app_labels = {'App_Market_Agriculture': '精准农业', 'App_Market_Surveying': '测绘勘探',
                  'App_Market_Security': '安防巡逻', 'App_Market_Logistics': '物流配送', 'App_Market_Filming': '影视航拍'}
    df_app_market = df[app_cols].rename(columns=app_labels)

    fig_app_market = px.area(df_app_market,
                             title="主要AI赋能应用领域市场规模 (十亿美元)",
                             labels={'value': '市场规模 (十亿美元)', 'variable': '应用领域', 'Year': '年份'},
                             markers=False) # Use area chart for better visualization of components
    fig_app_market.update_layout(hovermode="x unified")
    st.plotly_chart(fig_app_market, use_container_width=True)
    st.markdown(f"""
    *   **精准农业**: 市场规模预计达到 **${latest_data['App_Market_Agriculture']} B**，AI实现变量喷洒、作物监测等。
    *   **测绘勘探**: 市场规模预计达到 **${latest_data['App_Market_Surveying']} B**，AI提升数据处理和建模效率。
    *   **安防巡逻**: 市场规模预计达到 **${latest_data['App_Market_Security']} B**，AI实现自主巡逻、异常识别。
    *   **物流配送**: 市场潜力巨大，预计达到 **${latest_data['App_Market_Logistics']} B**，AI解决"最后一公里"配送难题。
    *   **影视航拍**: 市场规模 **${latest_data['App_Market_Filming']} B**，AI带来更智能的跟随拍摄、轨迹规划。
    """)

    st.subheader("AI赋能的量化效益提升")
    col1, col2 = st.columns(2)
    with col1:
        fig_agri_eff = px.line(df, y=['Agri_Pesticide_Reduction', 'Agri_Yield_Increase'],
                              title="精准农业效益: 农药减施与产量提升 (%)",
                              labels={'value': '百分比 (%)', 'variable': '效益指标', 'Year': '年份'})
        fig_agri_eff.update_layout(hovermode="x unified")
        st.plotly_chart(fig_agri_eff, use_container_width=True)
        st.markdown(f"*   **农药减施率**可达 **{latest_data['Agri_Pesticide_Reduction']}%**，**产量提升率**可达 **{latest_data['Agri_Yield_Increase']}%**。")

        fig_security_eff = px.line(df, y='Security_Cost_Saving',
                                  title="安防巡逻效益: 人力成本节约率 (%)",
                                  labels={'value': '成本节约率 (%)', 'Year': '年份'})
        fig_security_eff.update_layout(hovermode="x unified")
        st.plotly_chart(fig_security_eff, use_container_width=True)
        st.markdown(f"*   无人机自主巡逻可节约人力成本高达 **{latest_data['Security_Cost_Saving']}%**。")

    with col2:
        fig_survey_eff = px.line(df, y='Survey_Time_Reduction',
                                title="测绘勘探效益: 作业时间缩短率 (%)",
                                labels={'value': '时间缩短率 (%)', 'Year': '年份'})
        fig_survey_eff.update_layout(hovermode="x unified")
        st.plotly_chart(fig_survey_eff, use_container_width=True)
        st.markdown(f"*   相比传统方法，无人机测绘可缩短作业时间 **{latest_data['Survey_Time_Reduction']}%**。")

        fig_logistics_eff = px.line(df, y='Logistics_Cost_Reduction',
                                   title="物流配送效益: 单次成本降低率 (%)",
                                   labels={'value': '成本降低率 (%)', 'Year': '年份'})
        fig_logistics_eff.update_layout(hovermode="x unified")
        st.plotly_chart(fig_logistics_eff, use_container_width=True)
        st.markdown(f"*   AI优化路径规划使单次配送成本降低 **{latest_data['Logistics_Cost_Reduction']}%**。")


# --- Tab 3: 产业链优势分析 ---
with tab3:
    st.subheader("中国无人机完整产业链布局")
    st.image("https://via.placeholder.com/1200x400.png?text=Placeholder+for+Drone+Supply+Chain+Diagram", 
             caption="示意图：中国无人机产业链", 
             use_container_width=True)

    st.markdown("""
    中国无人机产业形成了从**核心零部件**到**整机制造**再到**软件算法**和**应用服务**的完整闭环。

    **核心优势环节：**

    1.  **硬件制造与集成 (Hardware Manufacturing & Integration):**
        *   **规模化生产能力:** 依托强大的电子制造业基础，实现大规模、低成本生产。
        *   **核心部件自研/国产化:** 如飞控系统、图传系统、电池技术等环节取得突破，降低对外部依赖。
        *   **代表企业:** 大疆 (DJI), 极飞 (XAG - 农业领域) 等。
        *   **量化体现:** 全球70%以上的消费级无人机由中国制造。

    2.  **飞控与导航算法 (Flight Control & Navigation Algorithms):**
        *   **稳定可靠的飞控系统:** 保证飞行的稳定性和安全性，是无人机的"大脑"。
        *   **高精度定位导航:** 结合GPS/北斗、IMU、视觉传感器等实现厘米级定位。
        *   **自主飞行能力:** 路径规划、自主避障、精准降落等核心算法领先。
        *   **量化体现:** 大疆等企业的飞控系统在稳定性、易用性方面全球领先，支撑复杂应用场景。

    3.  **AI视觉技术 (AI Vision Technology):**
        *   **目标识别与跟踪:** 应用于安防监控、智能跟随拍摄等。
        *   **环境感知与三维重建:** 用于自主避障、测绘建模。
        *   **图像分析与处理:** 应用于精准农业作物监测、电力巡检缺陷识别等。
        *   **量化体现:** AI视觉技术使无人机识别农田病虫害准确率超过 **90%**，电力巡检效率提升 **5-10倍**。

    4.  **应用软件与平台 (Application Software & Platforms):**
        *   **易用的操控软件:** 降低用户使用门槛。
        *   **行业应用解决方案:** 提供针对特定行业的软硬件一体化方案（如农业植保、测绘数据处理平台）。
        *   **云服务与数据管理:** 支持大规模机队管理、数据存储和分析。
        *   **量化体现:** 大疆农业等平台管理着数百万亩农田的植保作业数据。

    **产业链协同效应：**
    *   上下游企业紧密合作，快速响应市场需求，加速技术迭代。
    *   完整的生态系统吸引了大量开发者和应用服务商，丰富了应用场景。
    *   规模效应进一步降低成本，巩固市场领导地位。
    """)


# --- Tab 4: 结论与展望 ---
with tab4:
    st.subheader("核心结论")
    st.markdown(f"""
    1.  **市场领导地位稳固:** 中国凭借以大疆为代表的领先企业，在全球无人机市场（特别是消费级）占据 **{latest_data['DJI_Share_Total']}%** 以上的主导份额，并在快速增长的行业级市场保持强劲竞争力。
    2.  **AI是核心驱动力:** AI技术渗透率的快速提升 (预计达 **{latest_data['AI_Adoption_Rate']}%**) 是无人机从单一功能向智能化、多场景应用平台转变的关键。AI显著提升了无人机在农业、测绘、安防、物流等领域的作业效率和智能化水平。
    3.  **全产业链优势:** 中国拥有从核心硬件、关键算法到应用服务的完整产业链，形成了强大的技术壁垒和成本优势，支持了技术的快速迭代和应用的广泛落地。例如，AI视觉技术使精准农业农药使用减少 **{latest_data['Agri_Pesticide_Reduction']}%**，测绘时间缩短 **{latest_data['Survey_Time_Reduction']}%**。
    4.  **应用场景持续拓展:** AI赋能下，无人机正从传统航拍、巡检拓展到更复杂的自主作业场景，如城市物流、应急救援、环境监测等，市场潜力巨大。
    """)

    st.subheader("未来展望")
    st.markdown("""
    *   **智能化水平持续提升:** 更高级别的自主飞行能力、更强的环境感知与决策能力将是发展重点。
    *   **行业应用深度融合:** 无人机将更紧密地融入各行业工作流，成为数字化转型的重要工具。
    *   **空域管理与法规完善:** 随着无人机数量和应用增加，智能化的空域管理系统和完善的法规体系将愈发重要。
    *   **集群作业与协同:** AI驱动的无人机集群技术将在物流、测绘、表演等领域发挥更大作用。
    *   **与其他技术融合:** 无人机将与5G、物联网、云计算、大数据等技术进一步融合，创造新的应用模式。
    """)

# --- 页脚 ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>数据来源: 模拟数据，基于行业公开报告和趋势分析 | 更新时间: 2024年</div>", unsafe_allow_html=True)
