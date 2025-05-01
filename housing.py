import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 自定义CSS样式 ---
st.markdown("""
<style>
    /* 主题颜色 */
    :root {
        --primary-color: #007bff; /* 蓝色 */
        --secondary-color: #6c757d; /* 灰色 */
        --background-color: #f8f9fa;
        --card-background-color: #ffffff;
        --text-color: #343a40;
        --metric-value-color: #0056b3; /* 深蓝色 */
    }

    .main-header {
        font-size: 2.5rem;
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px #eee;
    }
    .metric-card {
        background-color: var(--card-background-color);
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        text-align: center;
        border-top: 4px solid var(--primary-color);
        height: 100%; /* 卡片等高 */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-value {
        font-size: 2.0rem; /* 稍微调小一点 */
        font-weight: 600; /* 加粗 */
        color: var(--metric-value-color);
        margin-bottom: 0.5rem; /* 值和标签间距 */
    }
    .metric-label {
        font-size: 0.9rem; /* 稍微调小一点 */
        color: var(--secondary-color);
        line-height: 1.3; /* 标签行高 */
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 2px solid #dee2e6; /* 标签栏下划线 */
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent; /* 透明背景 */
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        border: none; /* 移除默认边框 */
        border-bottom: 4px solid transparent; /* 底部边框，用于选中效果 */
        transition: border-bottom 0.3s ease; /* 平滑过渡 */
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent; /* 选中时也透明 */
        color: var(--primary-color); /* 选中时文字颜色 */
        border-bottom: 4px solid var(--primary-color); /* 选中时底部边框 */
    }
    h3 { /* 子标题样式 */
        color: var(--primary-color);
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 5px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    ul { /* 列表样式 */
        list-style: none;
        padding-left: 0;
    }
    li::before { /* 自定义列表项符号 */
        content: "🔹"; /* 使用蓝色菱形 */
        color: var(--primary-color);
        display: inline-block;
        width: 1em;
        margin-left: -1em;
        margin-right: 0.5em;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_smart_living_data():
    try:
        data = pd.read_csv('data/smart_living_data.csv', index_col='Year')
        return data
    except FileNotFoundError:
        st.error("找不到数据文件：data/smart_living_data.csv")
        return None

def main():
    # 立即加载数据
    df_trends = load_smart_living_data()
    if df_trends is None:
        st.stop()

    # --- 数据存储 ---
    # 使用字典存储提供的关键数据点
    data = {
        "home_ecosystem": {
            "shipments_2025": "2.81亿台",
            "shipments_growth_2025": "+7.8%",
            "ai_voice_share_2025": ">60%",
            "xiaomi_families": "1.2亿",
            "xiaomi_voice_interactions_daily": 15,
            "xiaomi_automation_rate": "75%",
            "response_time_now": "0.3秒",
            "response_time_2020": "1.5秒",
            "wake_up_error_rate": "<1%",
            "wake_up_error_rate_standard": "5%",
            "energy_reduction_xiaomi": "18%",
            "cost_saving_xiaomi_annual": "~300元",
            "xiaomi_devices_connected_2025": 20,
            "xiaomi_devices_connected_2020": 8,
            "xiaomi_user_rules": "5亿条"
        },
        "community_management": {
            "facial_recognition_adoption": "85%",
            "facial_recognition_accuracy": "99.7%",
            "visitor_efficiency_increase": "3倍",
            "high_rise_detection_coverage": "98%",
            "high_rise_detection_accuracy": ">95%",
            "dispute_reduction": "40%",
            "parking_search_time_ai": "30秒",
            "parking_search_time_traditional": "4分钟",
            "parking_utilization_rate": "92%",
            "unmanned_delivery_daily_orders": "200万单",
            "unmanned_delivery_cost_reduction": "50%",
            "unmanned_delivery_night_coverage": "80%",
            "ai_images_processed_daily": "10亿张",
            "ai_event_response_time": "<10秒"
        },
        "building_energy": {
            "hvac_energy_reduction": "25%",
            "lighting_energy_reduction": "30%",
            "predictive_maintenance_failure_reduction": "45%",
            "predictive_maintenance_cost_saving": "35%",
            "pv_efficiency_ai_2025": "22.5%",
            "pv_efficiency_avg": "19%",
            "storage_efficiency_ai_2025": "92%",
            "huawei_solar_home_ratio": "15%",
            "huawei_power_generation_annual": ">6000kWh",
            "huawei_grid_income_annual": "~1200元"
        },
        "trends_policy": {
            "data_security_compliance_2025": "90%",
            "privacy_risk_reduction": "70%",
            "edge_processing_boost": "5倍",
            "edge_response_time": "毫秒级"
        }
    }

    # --- 标题 ---
    st.markdown("<h1 class='main-header'>AI驱动中国智慧生活变革分析</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--secondary-color); margin-bottom: 2rem;'>探索人工智能在智能家居、智慧社区及建筑节能领域的突破与应用</p>", unsafe_allow_html=True)


    # --- 关键指标概览 ---
    st.subheader("关键指标速览")
    cols_metrics = st.columns(4)
    metrics_data = [
        (f"{data['home_ecosystem']['shipments_2025']}", "2025年智能家居设备出货量 (预计)"),
        (f"{data['home_ecosystem']['energy_reduction_xiaomi']}", "AIoT平台家庭平均节能"),
        (f"{data['community_management']['facial_recognition_adoption']}", "新建小区人脸识别门禁普及率"),
        (f"{data['building_energy']['hvac_energy_reduction']}", "智能楼宇空调平均节能")
    ]

    for i, (value, label) in enumerate(metrics_data):
        with cols_metrics[i]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 创建选项卡 ---
    tab_home, tab_community, tab_building, tab_trends = st.tabs([
        "🏠 **智能家居生态**",
        "🏘️ **智慧社区管理**",
        "🏢 **建筑节能优化**",
        "�� **趋势与政策**"
    ])

    # --- Tab 1: 智能家居生态 ---
    with tab_home:
        st.header("智能家居生态系统：全场景联动与用户习惯学习")
        ecosystem_data = data['home_ecosystem']

        st.markdown(f"""
        AI正驱动智能家居从单品智能走向 **生态互联** 和 **主动智能**。通过学习用户习惯，系统能自动执行场景，提升便捷性与舒适度，并优化能源使用。
        """)

        cols_home1 = st.columns(3)
        with cols_home1[0]:
            st.metric(label="2025年设备出货量 (预计)", value=ecosystem_data['shipments_2025'], delta=ecosystem_data['shipments_growth_2025'])
        with cols_home1[1]:
            st.metric(label="AI语音控制设备占比 (2025预计)", value=ecosystem_data['ai_voice_share_2025'])
        with cols_home1[2]:
            st.metric(label="AIoT平台平均家庭节能", value=ecosystem_data['energy_reduction_xiaomi'], help=f"户均年节省电费约{ecosystem_data['cost_saving_xiaomi_annual']}")

        st.markdown("---")
        st.subheader("市场增长与技术渗透")
        cols_chart_home1 = st.columns(2)
        with cols_chart_home1[0]:
            fig_shipments = go.Figure()
            fig_shipments.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Home_Shipments'], mode='lines+markers', name='设备出货量 (亿台)', line=dict(color='royalblue')))
            fig_shipments.update_layout(title='智能家居设备出货量增长趋势', yaxis_title='亿台', hovermode="x unified")
            st.plotly_chart(fig_shipments, use_container_width=True, key="smart_home_trend")
        with cols_chart_home1[1]:
            fig_voice = go.Figure()
            fig_voice.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Home_Voice_Share'], mode='lines+markers', name='AI语音设备占比 (%)', line=dict(color='mediumseagreen')))
            fig_voice.update_layout(title='AI语音控制设备占比趋势', yaxis_title='%', yaxis_range=[0, 100], hovermode="x unified")
            st.plotly_chart(fig_voice, use_container_width=True, key="adoption_rate")

        st.subheader("用户体验与效率提升")
        cols_chart_home2 = st.columns(2)
        with cols_chart_home2[0]:
            fig_resp_time = go.Figure()
            fig_resp_time.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Home_Response_Time'], mode='lines+markers', name='平均响应时间 (秒)', line=dict(color='firebrick')))
            fig_resp_time.update_layout(title='设备平均响应时间变化', yaxis_title='秒', hovermode="x unified")
            st.plotly_chart(fig_resp_time, use_container_width=True, key="response_time")
        with cols_chart_home2[1]:
            fig_conn_dev = go.Figure()
            fig_conn_dev.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Home_Connected_Devices'], mode='lines+markers', name='户均连接设备数', line=dict(color='darkorange')))
            fig_conn_dev.update_layout(title='户均智能设备连接数增长', yaxis_title='台', hovermode="x unified")
            st.plotly_chart(fig_conn_dev, use_container_width=True, key="connected_devices")

        st.markdown("---")
        st.subheader("典型生态案例：小米AIoT")
        cols_xiaomi = st.columns(3)
        with cols_xiaomi[0]:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color: #FF6F00;">
                <div class="metric-value">{ecosystem_data['xiaomi_families']}</div>
                <div class="metric-label">连接家庭数量</div>
            </div>
            """, unsafe_allow_html=True)
        with cols_xiaomi[1]:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color: #FF6F00;">
                <div class="metric-value">{ecosystem_data['xiaomi_voice_interactions_daily']}次</div>
                <div class="metric-label">用户日均语音交互</div>
            </div>
            """, unsafe_allow_html=True)
        with cols_xiaomi[2]:
           st.markdown(f"""
            <div class="metric-card" style="border-top-color: #FF6F00;">
                <div class="metric-value">{ecosystem_data['xiaomi_automation_rate']}</div>
                <div class="metric-label">场景自动化执行率</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        *   **设备连接增长**: 单户平均连接设备数从2020年的 `{ecosystem_data['xiaomi_devices_connected_2020']}` 台增至2025年的 `{ecosystem_data['xiaomi_devices_connected_2025']}` 台。
        *   **用户自定义能力**: 用户自定义场景规则数突破 `{ecosystem_data['xiaomi_user_rules']}`。
        """)

        st.markdown("---")
        st.subheader("AI驱动的性能与效率优化")
        cols_perf = st.columns(2)
        with cols_perf[0]:
            st.markdown("**响应速度提升:**")
            st.markdown(f"<ul><li>平均响应时间从 `{ecosystem_data['response_time_2020']}` 缩短至 `{ecosystem_data['response_time_now']}`</li></ul>", unsafe_allow_html=True)
        with cols_perf[1]:
            st.markdown("**交互准确性提高:**")
            st.markdown(f"<ul><li>误唤醒率降至 `{ecosystem_data['wake_up_error_rate']}` (远优于 `{ecosystem_data['wake_up_error_rate_standard']}` 的行业标准)</li></ul>", unsafe_allow_html=True)


    # --- Tab 2: 智慧社区管理 ---
    with tab_community:
        st.header("智慧社区管理：AI驱动的安全与效率升级")
        community_data = data['community_management']

        st.markdown("""
        AI技术正全面渗透社区管理，从 **安全防护** 到 **生活服务**，显著提升了社区管理的智能化水平、运行效率和居民体验。
        """)

        st.subheader("核心系统普及与应用")
        cols_chart_comm1 = st.columns(2)
        with cols_chart_comm1[0]:
            fig_facial = go.Figure()
            fig_facial.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Community_Facial_Adoption'], mode='lines+markers', name='人脸识别门禁普及率 (%)', line=dict(color='purple')))
            fig_facial.update_layout(title='新建小区人脸识别门禁普及率趋势', yaxis_title='%', yaxis_range=[0, 100], hovermode="x unified")
            st.plotly_chart(fig_facial, use_container_width=True, key="facial_adoption")
        with cols_chart_comm1[1]:
            fig_highrise = go.Figure()
            fig_highrise.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Community_HighRise_Coverage'], mode='lines+markers', name='高空抛物监测覆盖率 (%)', line=dict(color='teal')))
            fig_highrise.update_layout(title='高空抛物监测覆盖率增长', yaxis_title='%', yaxis_range=[0, 100], hovermode="x unified")
            st.plotly_chart(fig_highrise, use_container_width=True, key="high_rise_coverage")

        st.subheader("AI安防：精准识别与主动预警")
        cols_sec = st.columns(3)
        with cols_sec[0]:
            st.metric(label="人脸识别门禁普及率 (新建小区)", value=community_data['facial_recognition_adoption'], help=f"识别准确率 {community_data['facial_recognition_accuracy']}")
        with cols_sec[1]:
            st.metric(label="高空抛物监测覆盖率 (高层)", value=community_data['high_rise_detection_coverage'], help=f"事件追溯准确率 {community_data['high_rise_detection_accuracy']}")
        with cols_sec[2]:
            st.metric(label="社区安全纠纷减少", value=f"-{community_data['dispute_reduction']}")

        st.markdown(f"""
        *   **通行效率**: 人脸识别使访客通行效率提升 `{community_data['visitor_efficiency_increase']}`。
        *   **数据处理**: AI安防系统日均处理图像数据量达 `{community_data['ai_images_processed_daily']}`。
        *   **快速响应**: 异常事件平均响应时间缩短至 `{community_data['ai_event_response_time']}`。
        """)

        st.markdown("---")
        st.subheader("社区服务效率提升")
        cols_chart_comm2 = st.columns(2)
        with cols_chart_comm2[0]:
            fig_parking = go.Figure()
            fig_parking.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Community_Parking_Time'], mode='lines+markers', name='AI引导平均寻位时间 (秒)', line=dict(color='darkgoldenrod')))
            fig_parking.update_layout(title='AI引导下停车场寻位时间变化', yaxis_title='秒', hovermode="x unified")
            st.plotly_chart(fig_parking, use_container_width=True, key="parking_time")
        with cols_chart_comm2[1]:
            fig_delivery = go.Figure()
            fig_delivery.add_trace(go.Bar(x=df_trends.index, y=df_trends['Community_Unmanned_Orders'], name='无人配送日单量 (百万单)', marker_color='lightcoral'))
            fig_delivery.update_layout(title='社区无人配送日均订单量增长', yaxis_title='百万单', hovermode="x unified")
            st.plotly_chart(fig_delivery, use_container_width=True, key="unmanned_orders")

        st.markdown(f"*   **夜间服务**: 无人配送使夜间服务覆盖率扩大至 `{community_data['unmanned_delivery_night_coverage']}` (例如菜鸟驿站智能柜等)。")


    # --- Tab 3: 建筑节能优化 ---
    with tab_building:
        st.header("建筑节能：AI优化与可再生能源整合")
        building_data = data['building_energy']

        st.markdown("""
        AI算法结合物联网传感器，正在实现建筑能源的 **精细化管理** 和 **预测性维护**。同时，AI也在优化 **可再生能源** 的利用效率，推动建筑向低碳、零碳转型。
        """)

        st.subheader("楼宇能效提升趋势")
        cols_chart_bldg1 = st.columns(2)
        with cols_chart_bldg1[0]:
            fig_hvac = go.Figure()
            fig_hvac.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Building_HVAC_Reduction'], mode='lines+markers', name='空调能耗降低 (%)', line=dict(color='deepskyblue')))
            fig_hvac.update_layout(title='智能楼宇空调能耗降低趋势', yaxis_title='%', hovermode="x unified")
            st.plotly_chart(fig_hvac, use_container_width=True, key="hvac_reduction")
        with cols_chart_bldg1[1]:
            fig_maint = go.Figure()
            fig_maint.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Building_Maint_Cost_Saving'], mode='lines+markers', name='预测性维护成本节省 (%)', line=dict(color='darkviolet')))
            fig_maint.update_layout(title='预测性维护成本节省趋势', yaxis_title='%', hovermode="x unified")
            st.plotly_chart(fig_maint, use_container_width=True, key="maintenance_cost")

        st.markdown("---")
        st.subheader("可再生能源效率优化")
        cols_chart_bldg2 = st.columns(2)
        with cols_chart_bldg2[0]:
            fig_pv = go.Figure()
            fig_pv.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Building_PV_Efficiency_AI'], mode='lines+markers', name='AI优化光伏效率', line=dict(color='limegreen')))
            fig_pv.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Building_PV_Efficiency_Avg'], mode='lines', name='行业平均光伏效率', line=dict(color='gray', dash='dash')))
            fig_pv.update_layout(title='光伏发电效率对比', yaxis_title='%', hovermode="x unified", legend=dict(yanchor="bottom", y=0.01, xanchor="left", x=0.01))
            st.plotly_chart(fig_pv, use_container_width=True, key="pv_efficiency")
        with cols_chart_bldg2[1]:
            fig_storage = go.Figure()
            fig_storage.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Building_Storage_Efficiency'], mode='lines+markers', name='储能系统效率 (%)', line=dict(color='tomato')))
            fig_storage.update_layout(title='AI优化储能系统充放电效率趋势', yaxis_title='%', hovermode="x unified")
            st.plotly_chart(fig_storage, use_container_width=True, key="storage_efficiency")

        st.markdown(f"""
        *   **发电与收益 (华为"零碳社区"案例):**
            *   户均年发电量超 `{building_data['huawei_power_generation_annual']}`。
            *   余电上网年收益约 `{building_data['huawei_grid_income_annual']}`。
        """)


    # --- Tab 4: 趋势与政策 ---
    with tab_trends:
        st.header("技术趋势与政策环境")
        trends_data = data['trends_policy']

        st.markdown("""
        技术的持续迭代和国家政策的引导为AI在智慧生活领域的深入应用提供了有力支撑。
        """)

        st.subheader("政策支持与标准规范")
        cols_policy = st.columns(2)
        with cols_policy[0]:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color: #6f42c1;">
                <div class="metric-value">{trends_data['data_security_compliance_2025']}</div>
                <div class="metric-label">数据安全合规产品占比 (2025目标)</div>
            </div>
            """, unsafe_allow_html=True)
        with cols_policy[1]:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color: #6f42c1;">
                <div class="metric-value">-{trends_data['privacy_risk_reduction']}</div>
                <div class="metric-label">隐私泄露风险降低</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        *   **驱动力**: "中国制造2025"等战略推动智能家居、智慧城市标准化进程。
        *   **重点**: 数据安全和用户隐私保护成为行业规范的关键。
        """)

        st.markdown("---")
        st.subheader("技术迭代：边缘计算与AI芯片")
        cols_tech = st.columns(2)
        with cols_tech[0]:
             st.markdown(f"""
            <div class="metric-card" style="border-top-color: #fd7e14;">
                <div class="metric-value">x{trends_data['edge_processing_boost']}</div>
                <div class="metric-label">边缘计算本地数据处理能力提升</div>
            </div>
            """, unsafe_allow_html=True)
        with cols_tech[1]:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color: #fd7e14;">
                <div class="metric-value">{trends_data['edge_response_time']}</div>
                <div class="metric-label">设备离线响应速度</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        *   **核心**: AI芯片（如华为昇腾）的发展是关键，提升端侧智能水平。
        *   **优势**: 边缘计算减少了对云端的依赖，提高了响应速度，并有助于保护用户隐私。
        *   **影响**: 支持更复杂的本地AI应用，如更自然的语音交互、更精准的环境感知。
        """)

        st.markdown("---")
        st.subheader("政策驱动与合规进展")
        fig_compliance = go.Figure()
        fig_compliance.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Trends_Security_Compliance'], mode='lines+markers', name='数据安全合规产品占比 (%)', line=dict(color='rgb(111, 66, 193)'))) # 紫色
        fig_compliance.update_layout(title='数据安全合规产品占比提升趋势 (目标90%)', yaxis_title='%', yaxis_range=[0, 100], hovermode="x unified")
        st.plotly_chart(fig_compliance, use_container_width=True, key="compliance_trend")

        st.markdown("---")
        st.subheader("总结：AI重塑智慧生活")
        st.markdown("""
        综合来看，AI技术正以前所未有的深度和广度渗透到中国人的居住环境中：
        *   **家居层面**：从被动响应转向主动服务，实现更个性化、节能、便捷的居住体验。
        *   **社区层面**：提升了安全管理水平和公共服务效率，构建更安全、高效、便利的社区环境。
        *   **建筑层面**：推动了能源管理的精细化和可再生能源的普及，助力建筑行业低碳转型。

        在政策引导和技术创新的双重驱动下，中国智慧生活领域正从"功能化"加速迈向真正的"智慧化"，AI是这场变革的核心引擎。
        """)


    # --- 页脚 ---
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: var(--secondary-color); font-size: 0.85em;'>数据来源: 根据用户提供信息整理 | 更新时间: 2024年</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
