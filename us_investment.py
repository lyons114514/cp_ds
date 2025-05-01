import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #3498db;
        margin-top: 2rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .highlight {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
    .metric-container {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        background: rgba(52, 152, 219, 0.1);
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #3498db;
    }
    .metric-label {
        font-size: 1rem;
        color: #7f8c8d;
    }
    .metric-card {
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #7f8c8d;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("<h1 class='main-header'>美国研发投入与经济增长分析</h1>", unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    try:
        # 由于CSV文件前几行包含标题信息，需要跳过
        df = pd.read_csv("data/nsf25326-tab001.csv", skiprows=3)
        # 更改列名，使其更简洁
        df.columns = ['Year', 'GDP_Current', 'GDP_Constant', 'Deflator', 'RD_Current', 'RD_Constant', 
                      'RD_GDP_Total', 'RD_Perf_Business', 'RD_Perf_Federal', 'RD_Perf_HigherEd', 'RD_Perf_Other',
                      'RD_Fund_Business', 'RD_Fund_Federal', 'RD_Fund_Other']
        
        # 清理数据
        df = df.dropna(subset=['Year'])  # 删除没有年份的行
        df['Year'] = df['Year'].str.replace('[a-zA-Z]', '', regex=True).astype(int)  # 去除年份后的字母（如e, f）
        
        # 清理和转换货币列中的逗号
        for col in df.columns:
            if col != 'Year' and col != 'Deflator':
                df[col] = df[col].astype(str).str.replace(',', '').astype(float)
        
        return df
    except Exception as e:
        st.error(f"加载数据出错: {e}")
        return None

def main():
    # 将原有的主要代码移到main函数中
    df = load_data()
    if df is not None:
        # 创建侧边栏
        st.sidebar.title("分析控制面板")
        
        # 时间范围选择
        min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
        selected_years = st.sidebar.slider(
            "选择年份范围:",
            min_year, max_year, (min_year, max_year)
        )
        
        # 选择数据类型
        data_type = st.sidebar.radio(
            "选择数据类型:",
            ["当前美元", "2017年不变美元"]
        )
        
        # 按照选择筛选数据
        filtered_df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
        
        # 展示数据概览
        st.markdown("<h2 class='sub-header'>数据概览</h2>", unsafe_allow_html=True)
        
        # 计算关键指标
        latest_year = filtered_df['Year'].max()
        latest_data = filtered_df[filtered_df['Year'] == latest_year]
        
        avg_rdgdp = filtered_df['RD_GDP_Total'].mean()
        latest_rdgdp = latest_data['RD_GDP_Total'].values[0]
        
        if data_type == "当前美元":
            latest_rd = latest_data['RD_Current'].values[0]
            latest_gdp = latest_data['GDP_Current'].values[0]
            rd_growth_pct = ((latest_data['RD_Current'].values[0] / filtered_df[filtered_df['Year'] == latest_year - 10]['RD_Current'].values[0]) - 1) * 100 if latest_year - 10 >= min_year else None
        else:
            latest_rd = latest_data['RD_Constant'].values[0]
            latest_gdp = latest_data['GDP_Constant'].values[0]
            rd_growth_pct = ((latest_data['RD_Constant'].values[0] / filtered_df[filtered_df['Year'] == latest_year - 10]['RD_Constant'].values[0]) - 1) * 100 if latest_year - 10 >= min_year else None
        
        # 显示关键指标
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background-color: rgba(52, 152, 219, 0.1);">
                <div class="metric-value">{latest_rdgdp:.2f}%</div>
                <div class="metric-label">研发投入占GDP比例 ({latest_year}年)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background-color: rgba(46, 204, 113, 0.1);">
                <div class="metric-value">${latest_rd:.1f}十亿</div>
                <div class="metric-label">研发投入总额 ({latest_year}年)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if rd_growth_pct is not None:
                st.markdown(f"""
                <div class="metric-card" style="background-color: rgba(230, 126, 34, 0.1);">
                    <div class="metric-value">{rd_growth_pct:.1f}%</div>
                    <div class="metric-label">十年研发投入增长率</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card" style="background-color: rgba(230, 126, 34, 0.1);">
                    <div class="metric-value">N/A</div>
                    <div class="metric-label">十年研发投入增长率</div>
                </div>
                """, unsafe_allow_html=True)
        
        # 创建展示选项卡
        tab1, tab2, tab3, tab4 = st.tabs(["📈 总体趋势", "🔄 研发与GDP关系", "🏢 执行部门分析", "💰 资金来源分析"])
        
        with tab1:
            st.markdown("<h3 class='sub-header'>美国GDP和研发投入趋势</h3>", unsafe_allow_html=True)
            
            chart_type = st.radio(
                "选择图表类型:",
                ["折线图", "柱状图", "面积图"],
                horizontal=True
            )
            
            # 准备绘图数据
            if data_type == "当前美元":
                gdp_col = 'GDP_Current'
                rd_col = 'RD_Current'
                y_title = "十亿美元 (当前值)"
            else:
                gdp_col = 'GDP_Constant'
                rd_col = 'RD_Constant'
                y_title = "十亿美元 (2017年不变值)"
            
            # 创建双Y轴图表
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            if chart_type == "折线图":
                # GDP折线
                fig.add_trace(
                    go.Scatter(
                        x=filtered_df['Year'],
                        y=filtered_df[gdp_col],
                        name="GDP",
                        line=dict(color="#3498db", width=3)
                    ),
                    secondary_y=False,
                )
                
                # 研发投入折线
                fig.add_trace(
                    go.Scatter(
                        x=filtered_df['Year'],
                        y=filtered_df[rd_col],
                        name="研发投入",
                        line=dict(color="#2ecc71", width=3)
                    ),
                    secondary_y=True,
                )
            
            elif chart_type == "柱状图":
                # GDP柱状图
                fig.add_trace(
                    go.Bar(
                        x=filtered_df['Year'],
                        y=filtered_df[gdp_col],
                        name="GDP",
                        marker_color="#3498db",
                        opacity=0.7
                    ),
                    secondary_y=False,
                )
                
                # 研发投入柱状图
                fig.add_trace(
                    go.Bar(
                        x=filtered_df['Year'],
                        y=filtered_df[rd_col],
                        name="研发投入",
                        marker_color="#2ecc71",
                        opacity=0.7
                    ),
                    secondary_y=True,
                )
            
            else:  # 面积图
                # GDP面积图
                fig.add_trace(
                    go.Scatter(
                        x=filtered_df['Year'],
                        y=filtered_df[gdp_col],
                        name="GDP",
                        fill='tozeroy',
                        line=dict(color="#3498db", width=1),
                        fillcolor="rgba(52, 152, 219, 0.3)"
                    ),
                    secondary_y=False,
                )
                
                # 研发投入面积图
                fig.add_trace(
                    go.Scatter(
                        x=filtered_df['Year'],
                        y=filtered_df[rd_col],
                        name="研发投入",
                        fill='tozeroy',
                        line=dict(color="#2ecc71", width=1),
                        fillcolor="rgba(46, 204, 113, 0.3)"
                    ),
                    secondary_y=True,
                )
            
            # 设置图表布局
            fig.update_layout(
                title_text="美国GDP和研发投入趋势 ({}-{})".format(selected_years[0], selected_years[1]),
                height=500,
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                font=dict(size=12),
                plot_bgcolor='rgba(240,240,240,0.8)'
            )
            
            # 设置Y轴标题
            fig.update_yaxes(title_text=f"GDP ({y_title})", secondary_y=False)
            fig.update_yaxes(title_text=f"研发投入 ({y_title})", secondary_y=True)
            fig.update_xaxes(title_text="年份")
            
            # 显示图表
            st.plotly_chart(fig, use_container_width=True, key="investment_trend")
            
            # 研发投入年增长率
            st.markdown("<h3 class='sub-header'>研发投入年增长率</h3>", unsafe_allow_html=True)
            
            # 计算研发投入年增长率
            filtered_df['RD_Growth'] = filtered_df[rd_col].pct_change() * 100
            
            # 增长率柱状图
            fig = px.bar(
                filtered_df[filtered_df['Year'] > selected_years[0]],  # 跳过第一年（没有增长率）
                x='Year',
                y='RD_Growth',
                title=f"研发投入年增长率 ({selected_years[0]+1}-{selected_years[1]})",
                labels={'Year': '年份', 'RD_Growth': '年增长率 (%)'},
                color='RD_Growth',
                color_continuous_scale='RdBu',
                color_continuous_midpoint=0
            )
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(240,240,240,0.8)'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="rd_growth")
        
        with tab2:
            st.markdown("<h3 class='sub-header'>研发投入占GDP比例变化</h3>", unsafe_allow_html=True)
            
            # 创建研发占GDP比例折线图
            fig = px.line(
                filtered_df,
                x='Year',
                y='RD_GDP_Total',
                title=f"研发投入占GDP比例 ({selected_years[0]}-{selected_years[1]})",
                labels={'Year': '年份', 'RD_GDP_Total': '研发投入占GDP比例 (%)'},
                markers=True,
                line_shape='spline'
            )
            
            fig.update_traces(line=dict(color="#e74c3c", width=3))
            fig.update_layout(
                height=500,
                plot_bgcolor='rgba(240,240,240,0.8)'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="rd_gdp_ratio")
            
            # 创建研发与GDP散点图(相关性)
            st.markdown("<h3 class='sub-header'>研发投入与GDP相关性</h3>", unsafe_allow_html=True)
            
            fig = px.scatter(
                filtered_df,
                x=gdp_col,
                y=rd_col,
                title=f"研发投入与GDP相关性 ({selected_years[0]}-{selected_years[1]})",
                labels={gdp_col: f'GDP ({y_title})', rd_col: f'研发投入 ({y_title})'},
                trendline='ols',
                trendline_color_override="#e74c3c",
                hover_name='Year'
            )
            
            fig.update_traces(marker=dict(size=10, color="#3498db"))
            fig.update_layout(
                height=500,
                plot_bgcolor='rgba(240,240,240,0.8)'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="rd_gdp_correlation")
        
        with tab3:
            st.markdown("<h3 class='sub-header'>研发执行部门分析</h3>", unsafe_allow_html=True)
            
            # 创建执行部门研发占GDP比例堆叠面积图
            fig = go.Figure()
            
            # 添加各执行部门的面积
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'], 
                y=filtered_df['RD_Perf_Business'],
                name='企业',
                stackgroup='one',
                line=dict(width=0.5, color='rgb(52, 152, 219)'),
                fillcolor='rgba(52, 152, 219, 0.8)'
            ))
            
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'], 
                y=filtered_df['RD_Perf_Federal'],
                name='联邦政府',
                stackgroup='one',
                line=dict(width=0.5, color='rgb(230, 126, 34)'),
                fillcolor='rgba(230, 126, 34, 0.8)'
            ))
            
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'], 
                y=filtered_df['RD_Perf_HigherEd'],
                name='高等教育',
                stackgroup='one',
                line=dict(width=0.5, color='rgb(46, 204, 113)'),
                fillcolor='rgba(46, 204, 113, 0.8)'
            ))
            
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'], 
                y=filtered_df['RD_Perf_Other'],
                name='其他非营利',
                stackgroup='one',
                line=dict(width=0.5, color='rgb(155, 89, 182)'),
                fillcolor='rgba(155, 89, 182, 0.8)'
            ))
            
            fig.update_layout(
                title=f'研发执行部门占GDP比例 ({selected_years[0]}-{selected_years[1]})',
                xaxis_title='年份',
                yaxis_title='占GDP比例 (%)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=500,
                plot_bgcolor='rgba(240,240,240,0.8)'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="sector_distribution")
            
            # 各部门执行占比变化
            st.markdown("<h3 class='sub-header'>研发执行部门占比变化</h3>", unsafe_allow_html=True)
            
            # 选择特定年份进行对比
            available_years = sorted(filtered_df['Year'].unique())
            
            # 如果有足够多的年份，选择有代表性的几个时间点
            if len(available_years) >= 4:
                default_idx = [0, len(available_years)//3, 2*len(available_years)//3, -1]
                default_years = [available_years[i] for i in default_idx]
            else:
                default_years = available_years
            
            selected_comp_years = st.multiselect(
                "选择要比较的年份:",
                available_years,
                default=default_years
            )
            
            if selected_comp_years:
                # 准备饼图数据
                comp_df = filtered_df[filtered_df['Year'].isin(selected_comp_years)]
                
                # 创建多个饼图
                pie_cols = st.columns(len(selected_comp_years))
                
                for i, year in enumerate(sorted(selected_comp_years)):
                    year_data = comp_df[comp_df['Year'] == year]
                    
                    if not year_data.empty:
                        values = [
                            year_data['RD_Perf_Business'].values[0],
                            year_data['RD_Perf_Federal'].values[0],
                            year_data['RD_Perf_HigherEd'].values[0],
                            year_data['RD_Perf_Other'].values[0]
                        ]
                        
                        labels = ['企业', '联邦政府', '高等教育', '其他非营利']
                        
                        fig = go.Figure(data=[go.Pie(
                            labels=labels,
                            values=values,
                            hole=.3,
                            marker_colors=['rgb(52, 152, 219)', 'rgb(230, 126, 34)', 
                                           'rgb(46, 204, 113)', 'rgb(155, 89, 182)']
                        )])
                        
                        fig.update_layout(
                            title_text=f"{year}年研发执行部门占比",
                            height=350,
                            margin=dict(t=40, b=20, l=20, r=20)
                        )
                        
                        with pie_cols[i % len(pie_cols)]:
                            st.plotly_chart(fig, use_container_width=True, key=f"sector_distribution_{year}")
            else:
                st.warning("请选择至少一个年份进行对比。")
        
        with tab4:
            st.markdown("<h3 class='sub-header'>研发资金来源分析</h3>", unsafe_allow_html=True)
            
            # 创建资金来源研发占GDP比例堆叠面积图
            fig = go.Figure()
            
            # 添加各资金来源的面积
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'], 
                y=filtered_df['RD_Fund_Business'],
                name='企业',
                stackgroup='one',
                line=dict(width=0.5, color='rgb(41, 128, 185)'),
                fillcolor='rgba(41, 128, 185, 0.8)'
            ))
            
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'], 
                y=filtered_df['RD_Fund_Federal'],
                name='联邦政府',
                stackgroup='one',
                line=dict(width=0.5, color='rgb(192, 57, 43)'),
                fillcolor='rgba(192, 57, 43, 0.8)'
            ))
            
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'], 
                y=filtered_df['RD_Fund_Other'],
                name='其他(州政府/非营利)',
                stackgroup='one',
                line=dict(width=0.5, color='rgb(142, 68, 173)'),
                fillcolor='rgba(142, 68, 173, 0.8)'
            ))
            
            fig.update_layout(
                title=f'研发资金来源占GDP比例 ({selected_years[0]}-{selected_years[1]})',
                xaxis_title='年份',
                yaxis_title='占GDP比例 (%)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=500,
                plot_bgcolor='rgba(240,240,240,0.8)'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="fund_distribution")
            
            # 联邦与企业资金占比对比
            st.markdown("<h3 class='sub-header'>联邦与企业研发资金占比对比</h3>", unsafe_allow_html=True)
            
            # 创建联邦与企业资金占比对比折线图
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'],
                y=filtered_df['RD_Fund_Business'] / filtered_df['RD_GDP_Total'] * 100,
                name='企业资金占比',
                mode='lines+markers',
                line=dict(color='rgb(41, 128, 185)', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'],
                y=filtered_df['RD_Fund_Federal'] / filtered_df['RD_GDP_Total'] * 100,
                name='联邦资金占比',
                mode='lines+markers',
                line=dict(color='rgb(192, 57, 43)', width=3)
            ))
            
            fig.update_layout(
                title=f'联邦与企业研发资金在总研发投入中的占比 ({selected_years[0]}-{selected_years[1]})',
                xaxis_title='年份',
                yaxis_title='占总研发投入的百分比 (%)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=500,
                plot_bgcolor='rgba(240,240,240,0.8)'
            )
            
            st.plotly_chart(fig, use_container_width=True, key="fund_ratio")
        
        # 添加数据表展示
        st.markdown("<h2 class='sub-header'>原始数据</h2>", unsafe_allow_html=True)
        
        show_full_data = st.checkbox("显示完整数据表")
        
        if show_full_data:
            st.dataframe(filtered_df, use_container_width=True)
        
        # 添加页脚
        st.markdown("""
        <div class="footer">
            <p>数据来源: 美国国家科学基金会（NSF） | 信息更新至2023年</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("无法加载数据文件，请确保nsf25326-tab001.csv文件在正确的位置。")

if __name__ == "__main__":
    main()
