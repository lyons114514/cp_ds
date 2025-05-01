import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0056b3; /* 深蓝色 */
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px #eee;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        text-align: center;
        border-top: 4px solid #007bff; /* 蓝色 */
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-value {
        font-size: 2.0rem;
        font-weight: 600;
        color: #0056b3;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        line-height: 1.3;
    }
     .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 2px solid #dee2e6;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        border: none;
        border-bottom: 4px solid transparent;
        transition: border-bottom 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #007bff;
        border-bottom: 4px solid #007bff;
    }
    h3 {
        color: #0056b3;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 5px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 静态数据字典 (从文本提取的关键指标)
data_points = {
    "auto": {
        "welding_precision": "±0.02 mm",
        "line_changeover_old": "8 小时",
        "line_changeover_new": "15 分钟",
        "flexible_models": 10,
        "assembly_yield_old": "92%",
        "assembly_yield_new": "99.5%",
        "assembly_cost_reduction": "70%",
        "defect_detection_speed": "2000 帧/秒",
        "defect_miss_rate": "0.01%",
        "qc_cost_saving_yearly": "> 2 亿元"
    },
    "electronics": {
        "packaging_pressure_precision": "0.1 N·m",
        "packaging_efficiency_increase": "3 倍",
        "packaging_defect_rate": "50 ppm",
        "smt_cycle_reduction": "18%",
        "smt_oee": "92%",
        "machining_tolerance_old": "±5 µm",
        "machining_tolerance_new": "±1 µm",
        "tool_wear_accuracy": "98%"
    },
    "general": {
        "agv_count": 100,
        "agv_payload": "20 吨级",
        "agv_response_time": "0.5 秒",
        "agv_logistics_efficiency": "40%",
        "agv_inventory_turnover": "35%",
        "robot_arm_precision": "0.1 mm",
        "dangerous_task_replacement": "90%",
        "economic_loss_avoidance_yearly": "> 8 亿元",
        "robot_positioning_accuracy_new": "0.01 mm",
        "robot_positioning_accuracy_old": "0.1 mm",
        "force_control_response": "毫秒级"
    },
    "battery_case": {
        "sorting_efficiency_old": "200 片/分钟",
        "sorting_efficiency_new": "1200 片/分钟",
        "defect_detection_rate": "99.99%"
    }
}

def main():
    # 从CSV文件加载数据
    data_file_path = 'data/manufacturing_trends.csv'
    if os.path.exists(data_file_path):
        df_trends = pd.read_csv(data_file_path, index_col='Year', encoding='utf-8-sig')
    else:
        st.error("数据文件未找到，请确保 'data/manufacturing_trends.csv' 存在。")
        st.stop()

    latest_year = df_trends.index[-1]  # 2025E
    year_2023 = '2023'

    # --- 页面标题 ---
    st.markdown("<h1 class='main-header'>AI赋能中国智能制造深度分析</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6c757d; margin-bottom: 2rem;'>探索人工智能在汽车、电子及通用工业领域的应用突破与产业影响</p>", unsafe_allow_html=True)

    # --- 关键指标概览 ---
    st.subheader(f"关键成果与趋势 ({year_2023} / {latest_year})")
    cols_metrics = st.columns(4)
    with cols_metrics[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df_trends.loc[year_2023, 'Market_Size_CNY_B']} 十亿</div>
            <div class="metric-label">中国工业机器人市场规模 ({year_2023})</div>
        </div>
        """, unsafe_allow_html=True)
    with cols_metrics[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df_trends.loc[year_2023, 'Robot_Density_Auto']} 台/万人</div>
            <div class="metric-label">汽车行业机器人密度 ({year_2023})</div>
        </div>
        """, unsafe_allow_html=True)
    with cols_metrics[2]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df_trends.loc[latest_year, 'Flexible_Line_Share']}%</div>
            <div class="metric-label">AI驱动柔性产线占比 ({latest_year}目标)</div>
        </div>
        """, unsafe_allow_html=True)
    with cols_metrics[3]:
         st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df_trends.loc[latest_year, 'Predictive_Maint_Accuracy']}%</div>
            <div class="metric-label">预测性维护准确率 ({latest_year}预计)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 创建选项卡 ---
    tab_auto, tab_elec, tab_general, tab_impact = st.tabs([
        "🚗 **汽车制造**",
        "📱 **电子制造**",
        "🏭 **通用工业**",
        "📈 **技术突破与产业影响**"
    ])

    # --- Tab 1: 汽车制造 ---
    with tab_auto:
        st.header("汽车制造：迈向全流程自动化与柔性生产")
        auto_data = data_points['auto']

        st.subheader("焊接与装配场景：精度与效率双提升")
        cols_auto1 = st.columns(3)
        with cols_auto1[0]:
            st.metric(label="AI视觉引导焊接定位精度", value=auto_data['welding_precision'])
        with cols_auto1[1]:
            st.metric(label="生产线换型时间", value=auto_data['line_changeover_new'], delta=f"原为{auto_data['line_changeover_old']}")
        with cols_auto1[2]:
            st.metric(label="单线人力成本降低 (AI协作装配)", value=f"-{auto_data['assembly_cost_reduction']}")

        st.markdown(f"*   **柔性生产**: 可适应多达 `{auto_data['flexible_models']}` 款车型混线制造。")
        st.markdown(f"*   **良品率提升**: AI协作机器人使车门装配良品率从 `{auto_data['assembly_yield_old']}` 提升至 `{auto_data['assembly_yield_new']}`。")

        st.markdown("---")
        st.subheader("质量检测智能化：高速、精准、降本")
        cols_auto2 = st.columns(3)
        with cols_auto2[0]:
            st.metric(label="AI焊缝检测速度", value=auto_data['defect_detection_speed'])
        with cols_auto2[1]:
            st.metric(label="AI焊缝检测漏检率", value=f"低至 {auto_data['defect_miss_rate']}")
        with cols_auto2[2]:
            st.metric(label="年节省质检成本", value=auto_data['qc_cost_saving_yearly'])

        # 图表：焊接精度趋势
        fig_precision = go.Figure()
        fig_precision.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Welding_Precision'], mode='lines+markers', name='定位精度 (mm)', line=dict(color='royalblue')))
        fig_precision.update_layout(title='AI驱动焊接定位精度提升趋势 (模拟)', yaxis_title='毫米 (mm)', hovermode="x unified", yaxis_range=[0, 0.11])
        st.plotly_chart(fig_precision, use_container_width=True, key="welding_precision")

    # --- Tab 2: 电子制造 ---
    with tab_elec:
        st.header("电子制造：高精度柔性生产与效率优化")
        elec_data = data_points['electronics']

        st.subheader("芯片封装与SMT贴装：效率与良率的关键")
        cols_elec1 = st.columns(3)
        with cols_elec1[0]:
            st.metric(label="AI力控封装压力精度", value=elec_data['packaging_pressure_precision'])
        with cols_elec1[1]:
            st.metric(label="芯片封装效率提升", value=elec_data['packaging_efficiency_increase'])
        with cols_elec1[2]:
            st.metric(label="封装不良率", value=f"降至 {elec_data['packaging_defect_rate']}")

        st.markdown(f"*   **SMT优化**: AI动态路径规划使贴装周期缩短 `{elec_data['smt_cycle_reduction']}`，设备综合效率(OEE)提升至 `{elec_data['smt_oee']}`。")

        st.markdown("---")
        st.subheader("微型元件精密加工：突破精度极限")
        cols_elec2 = st.columns(2)
        with cols_elec2[0]:
            st.metric(label="AI自适应磨削加工公差", value=elec_data['machining_tolerance_new'], delta=f"原为{elec_data['machining_tolerance_old']}")
        with cols_elec2[1]:
            st.metric(label="刀具磨损监测准确率", value=elec_data['tool_wear_accuracy'])

    # --- Tab 3: 通用工业 ---
    with tab_general:
        st.header("通用工业：AI赋能复杂与危险场景")
        general_data = data_points['general']

        st.subheader("重工领域智能搬运：效率与柔性的提升")
        cols_gen1 = st.columns(4)
        with cols_gen1[0]:
             st.markdown(f"""
             <div class="metric-card" style="border-top-color: #fd7e14;">
                 <div class="metric-value">{general_data['agv_count']}+</div>
                 <div class="metric-label">AI导航AGV部署数量</div>
             </div>
             """, unsafe_allow_html=True)
        with cols_gen1[1]:
             st.markdown(f"""
             <div class="metric-card" style="border-top-color: #fd7e14;">
                 <div class="metric-value">{general_data['agv_payload']}</div>
                 <div class="metric-label">单台AGV运输能力</div>
             </div>
             """, unsafe_allow_html=True)
        with cols_gen1[2]:
             st.markdown(f"""
             <div class="metric-card" style="border-top-color: #fd7e14;">
                 <div class="metric-value">{general_data['agv_logistics_efficiency']}</div>
                 <div class="metric-label">物流效率提升</div>
             </div>
             """, unsafe_allow_html=True)
        with cols_gen1[3]:
            st.markdown(f"""
             <div class="metric-card" style="border-top-color: #fd7e14;">
                 <div class="metric-value">{general_data['agv_inventory_turnover']}</div>
                 <div class="metric-label">库存周转率提高</div>
             </div>
             """, unsafe_allow_html=True)

        st.markdown(f"*   **快速响应**: 路径动态优化响应时间仅 `{general_data['agv_response_time']}`。")

        st.markdown("---")
        st.subheader("危险环境作业：机器换人保障安全")
        cols_gen2 = st.columns(3)
        with cols_gen2[0]:
            st.metric(label="AI绝缘臂操作精度", value=f"{general_data['robot_arm_precision']} 级")
        with cols_gen2[1]:
            st.metric(label="替代高危任务比例", value=f"> {general_data['dangerous_task_replacement']}")
        with cols_gen2[2]:
            st.metric(label="年避免经济损失", value=general_data['economic_loss_avoidance_yearly'])

    # --- Tab 4: 技术突破与产业影响 ---
    with tab_impact:
        st.header("技术突破与产业影响：塑造制造未来")
        general_data = data_points['general']
        battery_case = data_points['battery_case']

        st.subheader("核心技术指标显著提升")
        cols_tech = st.columns(2)
        with cols_tech[0]:
            st.metric(label="工业机器人重复定位精度", value=f"{general_data['robot_positioning_accuracy_new']} 级", delta=f"传统{general_data['robot_positioning_accuracy_old']}级")
        with cols_tech[1]:
            st.metric(label="力控响应速度", value=general_data['force_control_response'])

        st.markdown("---")
        st.subheader("预测性维护效果")
        cols_pred = st.columns(2)
        with cols_pred[0]:
            fig_pred_acc = go.Figure()
            fig_pred_acc.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Predictive_Maint_Accuracy'], mode='lines+markers', name='预测准确率 (%)', line=dict(color='mediumseagreen')))
            fig_pred_acc.update_layout(title='预测性维护准确率提升趋势', yaxis_title='%', hovermode="x unified", yaxis_range=[65, 100])
            st.plotly_chart(fig_pred_acc, use_container_width=True, key="predictive_maint_accuracy")
        with cols_pred[1]:
            fig_downtime = go.Figure()
            fig_downtime.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Downtime_Reduction'], mode='lines+markers', name='停机时间减少率 (%)', line=dict(color='tomato')))
            fig_downtime.update_layout(title='设备停机时间减少趋势', yaxis_title='%', hovermode="x unified")
            st.plotly_chart(fig_downtime, use_container_width=True, key="downtime_reduction")

        st.markdown("---")
        st.subheader("市场规模与渗透率")
        cols_market = st.columns(2)
        with cols_market[0]:
            fig_market_size = go.Figure()
            fig_market_size.add_trace(go.Bar(x=df_trends.index, y=df_trends['Market_Size_CNY_B'], name='市场规模 (十亿)', marker_color='cornflowerblue'))
            fig_market_size.update_layout(title='中国工业机器人市场规模 (十亿元)', yaxis_title='十亿元', hovermode="x unified")
            st.plotly_chart(fig_market_size, use_container_width=True, key="market_size")
        with cols_market[1]:
            fig_density = go.Figure()
            fig_density.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Robot_Density_Auto'], mode='lines+markers', name='汽车行业', line=dict(color='#1f77b4')))
            fig_density.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Robot_Density_Electronics'], mode='lines+markers', name='电子行业', line=dict(color='#ff7f0e')))
            fig_density.update_layout(title='重点行业机器人密度增长 (台/万人)', yaxis_title='台/万人', hovermode="x unified")
            st.plotly_chart(fig_density, use_container_width=True, key="robot_density")

        st.markdown(f"*   **机器人密度**: 2023年汽车、电子行业机器人密度分别达 `{df_trends.loc[year_2023,'Robot_Density_Auto']}` 台/万人和 `{df_trends.loc[year_2023,'Robot_Density_Electronics']}` 台/万人，较2015年增长约3倍。")

        st.markdown("---")
        st.subheader("未来趋势预测 (至2025E)")
        cols_trends = st.columns(2)
        with cols_trends[0]:
            fig_flex_share = go.Figure()
            fig_flex_share.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Flexible_Line_Share'], mode='lines+markers', name='柔性产线占比 (%)', line=dict(color='purple')))
            fig_flex_share.update_layout(title='AI驱动柔性生产线占比趋势', yaxis_title='%', hovermode="x unified", yaxis_range=[0, 50])
            st.plotly_chart(fig_flex_share, use_container_width=True, key="flexible_line_share")
        with cols_trends[1]:
            fig_domestic_share = go.Figure()
            fig_domestic_share.add_trace(go.Scatter(x=df_trends.index, y=df_trends['Domestic_Robot_Share'], mode='lines+markers', name='国产化率 (%)', line=dict(color='green')))
            fig_domestic_share.update_layout(title='工业机器人国产化率提升趋势', yaxis_title='%', hovermode="x unified", yaxis_range=[35, 80])
            st.plotly_chart(fig_domestic_share, use_container_width=True, key="domestic_robot_share")

        st.markdown("---")
        st.subheader("案例：新能源电池智能制造")
        st.markdown(f"""
        某新能源电池企业通过 **AI视觉+数字孪生技术** 实现：
        *   电芯分选效率：`{battery_case['sorting_efficiency_new']}` ( 人工仅 `{battery_case['sorting_efficiency_old']}` )
        *   缺陷检出率：`{battery_case['defect_detection_rate']}`
        这有力支撑了企业的快速产能扩张需求。
        """)

    # --- 页脚 ---
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #6c757d; font-size: 0.85em;'>数据来源: 根据用户提供信息及公开报告模拟 | 更新时间: 2024年</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
