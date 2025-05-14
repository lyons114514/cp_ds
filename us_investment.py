import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from scipy import stats

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #000000;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        font-family: 'SimHei', sans-serif;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #000000;
        margin-top: 2rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        font-family: 'SimHei', sans-serif;
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
        justify-content: space-around;
        align-items: center;
        text-align: center;
        padding: 0.5rem;
        border-radius: 10px;
        background: rgba(52, 152, 219, 0.05);
        margin-bottom: 0.8rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3498db;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
    }
    .metric-card {
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-right: 0.5rem;
        transition: transform 0.3s ease;
        width: 100%;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #7f8c8d;
        font-size: 0.8rem;
    }
    /* 增大选项卡样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-top: 10px;
        white-space: pre-wrap;
        font-size: 16px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(52, 152, 219, 0.2);
        border-radius: 5px 5px 0 0;
    }
    /* 控制面板样式 */
    .control-panel {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    .control-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #3498db;
        margin-bottom: 0.5rem;
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

# 在load_data函数后添加新的数据加载函数
@st.cache_data
def load_ai_data():
    try:
        ai_models = pd.read_csv('data/专利教育/历年知名AI模型数量_地区对比.csv')
        patents = pd.read_csv('data/专利教育/全球AI专利占比_按地区.csv')
        return ai_models, patents
    except Exception as e:
        st.error(f"加载AI数据出错: {e}")
        return None, None

def main():
    # 将原有的主要代码移到main函数中
    df = load_data()
    if df is not None:
        # 创建紧凑的数据概览
        st.markdown("<h2 class='sub-header'>数据概览</h2>", unsafe_allow_html=True)
        
        # 计算关键指标 (使用所有可用数据)
        latest_year = df['Year'].max()
        latest_data = df[df['Year'] == latest_year]
        
        latest_rdgdp = latest_data['RD_GDP_Total'].values[0]
        latest_rd_current = latest_data['RD_Current'].values[0]
        ten_year_ago = latest_year - 10
        rd_growth_pct = ((latest_data['RD_Current'].values[0] / df[df['Year'] == ten_year_ago]['RD_Current'].values[0]) - 1) * 100 if ten_year_ago in df['Year'].values else None
        
        # 使用一个容器显示所有指标
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-card" style="background-color: rgba(52, 152, 219, 0.1);">
                <div class="metric-value">{latest_rdgdp:.2f}%</div>
                <div class="metric-label">研发投入占GDP比例 ({latest_year}年)</div>
            </div>
            <div class="metric-card" style="background-color: rgba(46, 204, 113, 0.1);">
                <div class="metric-value">${latest_rd_current:.1f}十亿</div>
                <div class="metric-label">研发投入总额 ({latest_year}年)</div>
            </div>
            <div class="metric-card" style="background-color: rgba(230, 126, 34, 0.1);">
                <div class="metric-value">{f'{rd_growth_pct:.1f}%' if rd_growth_pct is not None else 'N/A'}</div>
                <div class="metric-label">十年研发投入增长率</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 创建展示选项卡 (调大)
        tabs = st.tabs(["📈 总体趋势", "🔄 研发与GDP关系", "🏢 执行部门分析", "💰 资金来源分析", "🤖 AI创新分析"])
        
        # 控制面板 (从侧边栏移至此处)
        st.markdown("<div class='control-panel'><div class='control-title'>分析控制面板</div>", unsafe_allow_html=True)
        
        # 时间范围选择
        min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
        selected_years = st.slider(
            "选择年份范围:",
            min_year, max_year, (min_year, max_year)
        )
        
        # 选择数据类型
        data_type = st.radio(
            "选择数据类型:",
            ["当前美元", "2017年不变美元"],
            horizontal=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 按照选择筛选数据
        filtered_df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
        
        with tabs[0]:  # 总体趋势
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
        
        with tabs[1]:  # 研发与GDP关系
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
        
        with tabs[2]:  # 执行部门分析
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
        
        with tabs[3]:  # 资金来源分析
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
        
        # 添加新的AI创新分析选项卡
        with tabs[4]:  # AI创新分析
            st.markdown("<h3 class='sub-header'>AI创新与研发投入分析</h3>", unsafe_allow_html=True)
            
            # 加载AI相关数据
            ai_models, patents = load_ai_data()
            
            if ai_models is not None and patents is not None:
                # 处理数据
                ai_models_us = ai_models[ai_models['地区'] == '美国'].copy()
                patents_us = patents[patents['地区'] == '美国'].copy()
                
                # 合并数据
                us_data = pd.DataFrame()
                us_data['Year'] = filtered_df['Year']
                us_data['R&D投入占GDP比例'] = filtered_df['RD_GDP_Total']
                
                # 处理AI模型数据
                ai_models_us['年份'] = pd.to_numeric(ai_models_us['年份'], errors='coerce')
                ai_models_us['知名AI模型数量'] = pd.to_numeric(ai_models_us['知名AI模型数量'], errors='coerce')
                
                # 处理专利数据
                patents_us['年份'] = pd.to_numeric(patents_us['年份'], errors='coerce')
                patents_us['AI专利占比(占全球总数百分比)'] = pd.to_numeric(patents_us['AI专利占比(占全球总数百分比)'], errors='coerce')
                
                # 合并AI数据
                us_data = us_data.merge(ai_models_us[['年份', '知名AI模型数量']], 
                                      left_on='Year', right_on='年份', how='left')
                us_data = us_data.merge(patents_us[['年份', 'AI专利占比(占全球总数百分比)']], 
                                      left_on='Year', right_on='年份', how='left')
                
                us_data = us_data.rename(columns={
                    '知名AI模型数量': 'AI模型数量',
                    'AI专利占比(占全球总数百分比)': 'AI专利占比'
                })
                
                # 删除重复的年份列并处理缺失值
                us_data = us_data.drop(['年份_x', '年份_y'], axis=1, errors='ignore')
                us_data = us_data.dropna()
                
                # 创建相关性热力图
                correlation_matrix = us_data[['R&D投入占GDP比例', 'AI模型数量', 'AI专利占比']].corr(method='spearman')
                
                fig = px.imshow(
                    correlation_matrix,
                    labels=dict(color="相关系数"),
                    x=correlation_matrix.columns,
                    y=correlation_matrix.columns,
                    color_continuous_scale="RdBu",
                    aspect="auto",
                    title="美国科技创新指标斯皮尔曼相关性热力图"
                )
                
                fig.update_traces(text=correlation_matrix.round(3), texttemplate="%{text}")
                fig.update_layout(height=500)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 时间序列预测
                st.markdown("<h3 class='sub-header'>时间序列预测分析</h3>", unsafe_allow_html=True)
                
                def fit_arima_and_forecast(data, column, periods=3):
                    model = ARIMA(data[column].values, order=(1,1,1))
                    results = model.fit()
                    forecast = results.forecast(steps=periods)
                    return forecast
                
                # 对各指标进行预测
                future_years = pd.DataFrame({'Year': range(2024, 2027)})
                predictions = pd.DataFrame()
                predictions['Year'] = future_years['Year']
                
                for column in ['R&D投入占GDP比例', 'AI模型数量', 'AI专利占比']:
                    forecast = fit_arima_and_forecast(us_data, column)
                    predictions[f'{column}_预测'] = forecast
                
                # 绘制时间序列预测图
                fig = go.Figure()
                
                # 添加历史数据和预测数据
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
                for i, column in enumerate(['R&D投入占GDP比例', 'AI模型数量', 'AI专利占比']):
                    # 历史数据
                    fig.add_trace(go.Scatter(
                        x=us_data['Year'],
                        y=us_data[column],
                        name=f'{column}实际值',
                        line=dict(color=colors[i])
                    ))
                    
                    # 预测数据
                    fig.add_trace(go.Scatter(
                        x=predictions['Year'],
                        y=predictions[f'{column}_预测'],
                        name=f'{column}预测值',
                        line=dict(color=colors[i], dash='dash')
                    ))
                
                fig.update_layout(
                    title='美国科技创新指标时间序列预测',
                    xaxis_title='年份',
                    yaxis_title='指标值',
                    height=600,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 显示预测结果表格
                st.markdown("<h3 class='sub-header'>未来三年预测结果</h3>", unsafe_allow_html=True)
                st.dataframe(predictions.round(3), use_container_width=True)
                
                # 显示详细的相关性分析
                st.markdown("<h3 class='sub-header'>详细相关性分析</h3>", unsafe_allow_html=True)
                
                for var1 in ['R&D投入占GDP比例', 'AI模型数量', 'AI专利占比']:
                    for var2 in ['R&D投入占GDP比例', 'AI模型数量', 'AI专利占比']:
                        if var1 != var2:
                            correlation, p_value = stats.spearmanr(us_data[var1], us_data[var2])
                            st.markdown(f"""
                            <div class="highlight">
                                <p><strong>{var1}</strong> 与 <strong>{var2}</strong> 的斯皮尔曼相关系数: {correlation:.3f}</p>
                                <p>p值: {p_value:.3f}</p>
                            </div>
                            """, unsafe_allow_html=True)
            
            else:
                st.error("无法加载AI相关数据文件，请确保数据文件在正确的位置。")
        
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
