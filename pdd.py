import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import os

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        background: linear-gradient(to right, #FF6B6B 0%, #FF8E53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #FF6B6B;
        margin-top: 2rem;
        border-bottom: 2px solid #FF6B6B;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B6B;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# 替换generate_data函数为load_data函数
@st.cache_data
def load_data():
    """从CSV文件加载数据"""
    try:
        df = pd.read_csv('data/pdd_data.csv')
        # 将date列转换为datetime类型
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"读取数据文件失败: {e}")
        return None

# 删除创建目录的代码
# if not os.path.exists('data'):
#     os.makedirs('data')

# 加载数据
df = load_data()

def main():
    if df is not None:
        # 标题
        st.markdown("<h1 class='main-header'>AI驱动电子商务分析平台</h1>", unsafe_allow_html=True)

        # 关键指标展示
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">28%</div>
                <div class="metric-label">拼多多AI推荐转化率</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">15%</div>
                <div class="metric-label">行业平均转化率</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">35%</div>
                <div class="metric-label">2025年AI贡献GMV占比</div>
            </div>
            """, unsafe_allow_html=True)

        # 创建选项卡
        tab1, tab2, tab3 = st.tabs(["📈 转化率分析", "💰 GMV趋势", "🤖 AI贡献分析"])

        with tab1:
            st.markdown("<h2 class='sub-header'>转化率对比分析</h2>", unsafe_allow_html=True)
            
            # 转化率趋势对比
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['pdd_conversion'],
                name='拼多多AI推荐转化率',
                line=dict(color='#FF6B6B', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['industry_avg_conversion'],
                name='行业平均转化率',
                line=dict(color='#4A90E2', width=3)
            ))
            
            fig.update_layout(
                title='转化率趋势对比',
                xaxis_title='日期',
                yaxis_title='转化率',
                height=500,
                hovermode='x unified',
                yaxis_tickformat='.0%'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="conversion_trend")
            
            # 转化率提升分析
            improvement = (df['pdd_conversion'] - df['industry_avg_conversion']) / df['industry_avg_conversion'] * 100
            
            fig = px.bar(
                x=df['date'],
                y=improvement,
                title='AI推荐转化率提升效果',
                labels={'x': '日期', 'y': '提升百分比'},
                color=improvement,
                color_continuous_scale='Reds'
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="conversion_improvement")

        with tab2:
            st.markdown("<h2 class='sub-header'>GMV增长趋势</h2>", unsafe_allow_html=True)
            
            # GMV趋势分析
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['total_gmv'],
                name='总GMV',
                line=dict(color='#FF6B6B', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['ai_contributed_gmv'],
                name='AI贡献GMV',
                line=dict(color='#FFB6B6', width=3),
                fill='tonexty'
            ))
            
            fig.update_layout(
                title='GMV增长趋势及AI贡献',
                xaxis_title='日期',
                yaxis_title='GMV (亿元)',
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="gmv_trend")
            
            # 按年度统计
            yearly_data = df.groupby('year').agg({
                'total_gmv': 'sum',
                'ai_contributed_gmv': 'sum'
            }).reset_index()
            
            yearly_data['ai_contribution_rate'] = yearly_data['ai_contributed_gmv'] / yearly_data['total_gmv'] * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    yearly_data,
                    x='year',
                    y=['total_gmv', 'ai_contributed_gmv'],
                    title='年度GMV对比',
                    barmode='group',
                    labels={'value': 'GMV (亿元)', 'year': '年份', 'variable': '类型'},
                    color_discrete_sequence=['#FF6B6B', '#FFB6B6']
                )
                st.plotly_chart(fig, use_container_width=True, key="yearly_gmv")
            
            with col2:
                fig = px.line(
                    yearly_data,
                    x='year',
                    y='ai_contribution_rate',
                    title='AI贡献率年度变化',
                    labels={'ai_contribution_rate': 'AI贡献率 (%)', 'year': '年份'},
                    markers=True
                )
                fig.update_traces(line_color='#FF6B6B')
                st.plotly_chart(fig, use_container_width=True, key="ai_contribution_rate")

        with tab3:
            st.markdown("<h2 class='sub-header'>AI对电商的影响分析</h2>", unsafe_allow_html=True)
            
            # AI效果分析
            monthly_avg = df.groupby('month').agg({
                'pdd_conversion': 'mean',
                'industry_avg_conversion': 'mean',
                'ai_contributed_gmv': 'mean'
            }).reset_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 月度转化率模式
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=monthly_avg['month'],
                    y=monthly_avg['pdd_conversion'],
                    name='拼多多AI推荐',
                    mode='lines+markers',
                    line=dict(color='#FF6B6B', width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=monthly_avg['month'],
                    y=monthly_avg['industry_avg_conversion'],
                    name='行业平均',
                    mode='lines+markers',
                    line=dict(color='#4A90E2', width=3)
                ))
                
                fig.update_layout(
                    title='月度转化率模式',
                    xaxis_title='月份',
                    yaxis_title='转化率',
                    yaxis_tickformat='.0%'
                )
                
                st.plotly_chart(fig, use_container_width=True, key="monthly_conversion")
            
            with col2:
                # AI贡献GMV的月度模式
                fig = px.line(
                    monthly_avg,
                    x='month',
                    y='ai_contributed_gmv',
                    title='AI贡献GMV的月度模式',
                    labels={'ai_contributed_gmv': 'AI贡献GMV (亿元)', 'month': '月份'},
                    markers=True
                )
                fig.update_traces(line_color='#FF6B6B')
                st.plotly_chart(fig, use_container_width=True, key="monthly_ai_gmv")

            # 结论分析
            st.markdown("<h2 class='sub-header'>分析结论</h2>", unsafe_allow_html=True)

            st.markdown("""
            ### 1. AI推荐显著提升转化率
            - 拼多多通过AI推荐将点击转化率提升至28%，远高于行业平均的15%
            - 转化率提升效果稳定，且呈现持续改善趋势

            ### 2. GMV增长贡献显著
            - 预计到2025年，AI将贡献35%的GMV增量
            - AI驱动的GMV增长呈现加速趋势

            ### 3. 个性化推荐效果
            - AI系统能精准捕捉用户偏好
            - 推荐算法持续优化，带来更高的用户满意度

            ### 4. 发展趋势
            - AI在电商领域的应用将进一步深化
            - 个性化推荐将成为电商平台核心竞争力
            """)

            # 添加页脚
            st.markdown("""
            <div style='text-align: center; color: #666; padding: 20px;'>
                数据来源：行业研究报告与模拟数据 | 更新时间：2024年
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("无法加载数据，请确保data/pdd_data.csv文件存在")

if __name__ == "__main__":
    main()
