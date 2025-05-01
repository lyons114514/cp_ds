import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# 自定义CSS样式
st.markdown("""
<style>
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# 生成模拟数据
def generate_data():
    # 生成月度数据
    dates = pd.date_range(start='2023-01-01', end='2025-12-31', freq='M')
    
    # 拼多多数据
    pdd_data = pd.DataFrame({
        'date': dates,
        'conversion_rate': np.linspace(20, 35, len(dates)) + np.random.normal(0, 1, len(dates)),
        'user_time': np.linspace(20, 28, len(dates)) + np.random.normal(0, 0.5, len(dates)),
        'ai_gmv_share': np.linspace(25, 42, len(dates)) + np.random.normal(0, 1, len(dates))
    })
    
    # 抖音数据
    douyin_data = pd.DataFrame({
        'date': dates,
        'video_generated': np.linspace(5, 10, len(dates)) + np.random.normal(0, 0.2, len(dates)),
        'roi_improvement': np.linspace(30, 50, len(dates)) + np.random.normal(0, 2, len(dates)),
        'sme_adoption': np.linspace(40, 70, len(dates)) + np.random.normal(0, 1, len(dates))
    })
    
    # 内容审核数据
    content_data = pd.DataFrame({
        'date': dates,
        'accuracy': np.linspace(98, 99.5, len(dates)) + np.random.normal(0, 0.1, len(dates)),
        'daily_review': np.linspace(5, 8, len(dates)) + np.random.normal(0, 0.2, len(dates)),
        'manual_reduction': np.linspace(30, 60, len(dates)) + np.random.normal(0, 2, len(dates))
    })
    
    # 小红书数据
    xiaohongshu_data = pd.DataFrame({
        'date': dates,
        'monthly_notes': np.linspace(1, 3, len(dates)) + np.random.normal(0, 0.1, len(dates)),
        'efficiency_boost': np.linspace(2, 3, len(dates)) + np.random.normal(0, 0.1, len(dates)),
        'viral_content': np.linspace(8, 15, len(dates)) + np.random.normal(0, 0.5, len(dates))
    })
    
    return pdd_data, douyin_data, content_data, xiaohongshu_data

# 生成数据
pdd_data, douyin_data, content_data, xiaohongshu_data = generate_data()

def load_market_share_data():
    # 移动支付市场份额
    payment_data = pd.DataFrame({
        '平台': ['支付宝', '微信支付', '云闪付', '其他'],
        '份额': [48.5, 39.2, 9.8, 2.5]
    })
    
    # 智慧零售市场份额
    retail_data = pd.DataFrame({
        '平台': ['阿里巴巴', '京东', '拼多多', '美团', '其他'],
        '份额': [41.3, 32.5, 13.2, 8.5, 4.5]
    })
    
    # 智慧出行市场份额
    travel_data = pd.DataFrame({
        '平台': ['滴滴', '高德', '美团打车', '曹操出行', '其他'],
        '份额': [45.2, 28.6, 15.8, 6.9, 3.5]
    })
    
    # 智能客服市场份额
    service_data = pd.DataFrame({
        '平台': ['百度智能云', '阿里云', '腾讯云', '华为云', '其他'],
        '份额': [35.8, 28.4, 20.3, 12.5, 3.0]
    })
    
    return payment_data, retail_data, travel_data, service_data

def main():
    # 主标题
    st.title("AI在电商与内容平台的应用分析")

    # 创建选项卡
    tab1, tab2, tab3 = st.tabs(["电商平台AI应用", "内容平台AI应用", "市场格局分析"])

    with tab1:
        st.header("电商平台AI应用效果分析")
        
        # 拼多多指标
        st.subheader("拼多多AI推荐系统效果")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("商品点击转化率提升", "35%", "↑15%")
        with col2:
            st.metric("用户日均停留时长", "28分钟", "↑40%")
        with col3:
            st.metric("2025年AI驱动GMV占比", "42%", "↑17%")
        
        # 拼多多趋势图
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=pdd_data['date'], y=pdd_data['conversion_rate'],
                                 name='转化率(%)', line=dict(color='#1f77b4')))
        fig1.add_trace(go.Scatter(x=pdd_data['date'], y=pdd_data['ai_gmv_share'],
                                 name='AI驱动GMV占比(%)', line=dict(color='#ff7f0e')))
        fig1.update_layout(title='AI应用效果趋势',
                          xaxis_title='日期',
                          yaxis_title='百分比(%)')
        st.plotly_chart(fig1, use_container_width=True)
        
        # 抖音指标
        st.subheader("AI广告创意引擎效果")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("年度AI生成视频", "1亿条+", "↑200%")
        with col2:
            st.metric("广告投放ROI提升", "50%", "↑20%")
        with col3:
            st.metric("中小商家使用率", "70%", "↑30%")

    with tab2:
        st.header("内容平台AI应用效果分析")
        
        # 内容审核指标
        st.subheader("大模型内容审核效果")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("违规内容识别准确率", "99.5%", "↑1.5%")
        with col2:
            st.metric("日均审核量", "8亿条", "↑60%")
        with col3:
            st.metric("人工复核需求减少", "60%", "↓")
        
        # 审核效果趋势图
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=content_data['date'], y=content_data['accuracy'],
                                 name='识别准确率(%)', line=dict(color='#2ca02c')))
        fig2.add_trace(go.Scatter(x=content_data['date'], y=content_data['manual_reduction'],
                                 name='人工复核减少比例(%)', line=dict(color='#d62728')))
        fig2.update_layout(title='内容审核效果趋势',
                          xaxis_title='日期',
                          yaxis_title='百分比(%)')
        st.plotly_chart(fig2, use_container_width=True)
        
        # 小红书指标
        st.subheader("AI图文助手效果")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("月度AI辅助生成笔记", "3000万篇", "↑200%")
        with col2:
            st.metric("创作者效率提升", "3倍", "↑200%")
        with col3:
            st.metric("爆款内容占比", "15%", "↑7%")

    with tab3:
        st.header("2023年中国智能应用市场格局分析")
        
        payment_data, retail_data, travel_data, service_data = load_market_share_data()
        
        # 移动支付市场
        st.subheader("移动支付市场份额分布")
        fig_payment = px.pie(
            payment_data,
            values='份额',
            names='平台',
            title='中国移动支付场景市场份额 (2023)',
            color_discrete_sequence=['rgb(33, 150, 243)', 'rgb(76, 175, 80)', 'rgb(244, 67, 54)', 'rgb(158, 158, 158)']
        )
        fig_payment.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_payment, use_container_width=True)
        
        # 智慧零售市场
        st.subheader("智慧零售市场份额分布")
        fig_retail = px.pie(
            retail_data,
            values='份额',
            names='平台',
            title='中国智慧零售场景市场份额 (2023)',
            color_discrete_sequence=['rgb(255, 87, 34)', 'rgb(233, 30, 99)', 'rgb(244, 67, 54)', 'rgb(255, 193, 7)', 'rgb(158, 158, 158)']
        )
        fig_retail.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_retail, use_container_width=True)
        
        # 智慧出行市场
        st.subheader("智慧出行市场份额分布")
        fig_travel = px.pie(
            travel_data,
            values='份额',
            names='平台',
            title='中国智慧出行场景市场份额 (2023)',
            color_discrete_sequence=['rgb(255, 87, 34)', 'rgb(33, 150, 243)', 'rgb(255, 193, 7)', 'rgb(63, 81, 181)', 'rgb(158, 158, 158)']
        )
        fig_travel.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_travel, use_container_width=True)
        
        # 智能客服市场
        st.subheader("智能客服市场份额分布")
        fig_service = px.pie(
            service_data,
            values='份额',
            names='平台',
            title='中国智能客服场景市场份额 (2023)',
            color_discrete_sequence=['rgb(33, 150, 243)', 'rgb(255, 87, 34)', 'rgb(76, 175, 80)', 'rgb(244, 67, 54)', 'rgb(158, 158, 158)']
        )
        fig_service.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_service, use_container_width=True)
        
        # 市场分析总结
        st.markdown("### 市场格局分析要点")
        st.markdown("""
        1. **移动支付市场**：
           * 支付宝以48.5%的份额领跑市场
           * 微信支付紧随其后占据39.2%
           * 云闪付占比9.8%，发展潜力较大
        
        2. **智慧零售市场**：
           * 阿里巴巴占据41.3%的市场份额
           * 京东以32.5%的份额位居第二
           * 拼多多和美团分别占据13.2%和8.5%的份额
        
        3. **智慧出行市场**：
           * 滴滴出行主导市场，占比45.2%
           * 高德和美团打车分别占据28.6%和15.8%
           * 曹操出行占据6.9%的细分市场
        
        4. **智能客服市场**：
           * 百度智能云领先，占比35.8%
           * 阿里云和腾讯云分别占据28.4%和20.3%
           * 华为云以12.5%的份额位居第四
        """)

# 页脚
st.markdown("---")
st.markdown("数据来源：IDC中国与艾瑞咨询联合发布的《2023中国AI应用场景研究报告》| 更新时间：2024年3月")

if __name__ == "__main__":
    main()
