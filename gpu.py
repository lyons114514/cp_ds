import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #000000;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        font-family: 'SimHei', sans-serif;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #000000;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.3rem;
        font-family: 'SimHei', sans-serif;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        height: 100%;
    }
    .highlight {
        background-color: #e8f4f8;
        padding: 0.8rem;
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
        border-radius: 4px;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #7f8c8d;
        font-size: 0.8rem;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        align-items: stretch;
        margin-bottom: 0.8rem;
        gap: 8px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: bold;
        color: #3498db;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #7f8c8d;
    }
    .metric-card {
        flex: 1;
        border-radius: 6px;
        padding: 0.6rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    /* 选项卡样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        padding-top: 12px;
        white-space: pre-wrap;
        font-size: 17px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(52, 152, 219, 0.1);
        border-radius: 5px 5px 0 0;
    }
    /* 筛选区域样式 */
    .filter-section {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    /* 表格样式 */
    .dataframe-container {
        padding: 0.5rem;
        border-radius: 8px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    /* 平衡列宽 */
    .equal-width {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("<h1 class='main-header'>GPU性能分析平台</h1>", unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data\gpu排行.csv")
        return df
    except Exception as e:
        st.error(f"加载数据出错: {e}")
        return None

def main():
    # 加载数据
    df = load_data()

    if df is not None:
        total_gpus = len(df)
        
        # === 定义筛选控件 (UI放在底部，但状态读取需要在过滤前) ===
        # (We define the widgets here conceptually for state reading, 
        # but render them at the bottom using st.container or similar if needed,
        # or just rely on Streamlit's rerun mechanism. Let's try the simpler way first.)

        # === 筛选逻辑 (放在使用 filtered_df 之前) ===
        st.sidebar.markdown("<h3 style='color: #3498db; font-size: 1.3rem; margin-bottom: 1rem;'>数据筛选</h3>", unsafe_allow_html=True) # Move title to sidebar

        # 提取制造商 (放在侧边栏)
        manufacturers = sorted(df['显卡名称'].apply(lambda x: x.split()[0] if ' ' in x else x).unique())
        selected_manufacturers = st.sidebar.multiselect(
            "选择制造商：",
            manufacturers,
            default=["NVIDIA"]
        )
        
        # 性能范围滑块 (放在侧边栏)
        min_token, max_token = float(df['显卡平均token'].min()), float(df['显卡平均token'].max())
        token_range = st.sidebar.slider(
            "性能范围 (token/s):",
            min_value=min_token, max_value=max_token, value=(min_token, max_token),
            step=0.1 # Add a step for better control if needed
        )
        
        # 显卡数量范围 (放在侧边栏)
        min_cards, max_cards = int(df['显卡数量'].min()), int(df['显卡数量'].max())
        card_count_range = st.sidebar.slider(
            "显卡数量范围:",
            min_value=min_cards, max_value=max_cards, 
            value=(min_cards, max_cards) # Default to full range
        )
        
        # 排名范围 (放在侧边栏)
        rank_range = st.sidebar.slider(
            "排名范围:",
            min_value=1, max_value=total_gpus, value=(1, 50)
        )

        # 应用筛选
        filtered_df = df.copy()
        if selected_manufacturers:
            mask = filtered_df['显卡名称'].apply(lambda x: any(m in x for m in selected_manufacturers))
            filtered_df = filtered_df[mask]
        filtered_df = filtered_df[
            (filtered_df['显卡平均token'] >= token_range[0]) & 
            (filtered_df['显卡平均token'] <= token_range[1])
        ]
        filtered_df = filtered_df[
            (filtered_df['显卡数量'] >= card_count_range[0]) & 
            (filtered_df['显卡数量'] <= card_count_range[1])
        ]
        filtered_df = filtered_df[
            (filtered_df['排名'] >= rank_range[0]) & 
            (filtered_df['排名'] <= rank_range[1])
        ]
       
        st.markdown("<h2 class='sub-header'>性能排行榜</h2>", unsafe_allow_html=True)
        
        # 显示数据表格（可排序）
        if not filtered_df.empty:
            st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
            st.dataframe(
                filtered_df[['显卡名称', '显卡数量', '每秒总token', '显卡平均token', '排名']],
                use_container_width=True,
                hide_index=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("没有符合筛选条件的数据，请尝试调整侧边栏的筛选选项。") # Updated warning message
        
        # 创建选项卡
        if len(filtered_df) > 0:
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📊 性能排行", 
                "🏢 厂商对比",
                "📈 系列分析", 
                "⚖️ 多维对比", 
                "🧠 AI框架",
                "📈 市场分析"
            ])
            
            with tab1:
                # 对数据进行排序
                performance_df = filtered_df.sort_values('显卡平均token', ascending=False).head(20)
                
                # 创建横向条形图
                fig = px.bar(
                    performance_df,
                    y='显卡名称',
                    x='显卡平均token',
                    orientation='h',
                    title='GPU性能排行 (每秒处理token数)',
                    labels={'显卡平均token': '每秒处理token数', '显卡名称': 'GPU型号'},
                    color='显卡平均token',
                    color_continuous_scale='Blues',
                    text='显卡平均token'
                )
                
                fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                fig.update_layout(
                    height=600,  # 调整高度，使图表更平衡
                    margin=dict(l=10, r=10, t=50, b=10),  # 调整边距
                    xaxis_title="每秒处理token数",
                    yaxis_title="GPU型号",
                    font=dict(size=12),
                    plot_bgcolor='rgba(240,240,240,0.6)',
                    yaxis={'categoryorder': 'total ascending'}
                )
                
                st.plotly_chart(fig, use_container_width=True, key="gpu_trend")
                
                # 显示性能分布
                st.markdown("<h3 style='font-size: 1.3rem; color: #3498db; margin-top: 1.5rem;'>性能分布</h3>", unsafe_allow_html=True)
                
                # 创建直方图
                fig = px.histogram(
                    filtered_df,
                    x='显卡平均token',
                    nbins=30,
                    title='GPU性能分布',
                    labels={'显卡平均token': '每秒处理token数', 'count': '显卡数量'},
                    color_discrete_sequence=['#3498db'],
                    opacity=0.7
                )
                
                fig.update_layout(
                    height=350,
                    margin=dict(l=10, r=10, t=50, b=10),
                    xaxis_title="每秒处理token数",
                    yaxis_title="显卡数量",
                    font=dict(size=12),
                    plot_bgcolor='rgba(240,240,240,0.6)'
                )
                
                st.plotly_chart(fig, use_container_width=True, key="gpu_distribution")
            
            with tab2:
                st.markdown("<h3 style='font-size: 1.3rem; color: #3498db;'>厂商性能对比</h3>", unsafe_allow_html=True)
                
                # 提取制造商
                filtered_df['制造商'] = filtered_df['显卡名称'].apply(lambda x: x.split()[0] if ' ' in x else x)
                
                # 按制造商分组计算平均性能
                manufacturer_perf = filtered_df.groupby('制造商')['显卡平均token'].mean().reset_index()
                manufacturer_perf = manufacturer_perf.sort_values('显卡平均token', ascending=False)
                
                # 统计各制造商的显卡数量
                manufacturer_count = filtered_df.groupby('制造商').size().reset_index(name='数量')
                
                # 使用两列布局
                col1, col2 = st.columns(2)
                
                with col1:
                    # 厂商平均性能
                    fig = px.bar(
                        manufacturer_perf,
                        x='制造商',
                        y='显卡平均token',
                        title='各厂商GPU平均性能对比',
                        labels={'显卡平均token': '平均每秒处理token数', '制造商': '制造商'},
                        color='显卡平均token',
                        color_continuous_scale='Teal',
                        text='显卡平均token'
                    )
                    
                    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                    fig.update_layout(
                        height=400,
                        margin=dict(l=10, r=10, t=50, b=10),
                        xaxis_title="制造商",
                        yaxis_title="平均每秒处理token数",
                        font=dict(size=12),
                        plot_bgcolor='rgba(240,240,240,0.6)'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="manufacturer_performance")
                
                with col2:
                    # 厂商占比饼图
                    fig = px.pie(
                        manufacturer_count,
                        values='数量',
                        names='制造商',
                        title='各厂商GPU数量占比',
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    
                    fig.update_layout(
                        height=400,
                        margin=dict(l=10, r=10, t=50, b=10),
                        font=dict(size=12)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="manufacturer_share")
                
                # 显示各厂商最强GPU
                st.markdown("<h3 style='font-size: 1.3rem; color: #3498db; margin-top: 1rem;'>各厂商性能最强GPU</h3>", unsafe_allow_html=True)
                
                top_by_manufacturer = filtered_df.loc[filtered_df.groupby('制造商')['显卡平均token'].idxmax()]
                top_by_manufacturer = top_by_manufacturer.sort_values('显卡平均token', ascending=False)
                
                # 使用多列布局展示各厂商最强GPU
                cols = st.columns(3)
                for i, (_, row) in enumerate(top_by_manufacturer.iterrows()):
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class="card" style="background-color: rgba(52, 152, 219, 0.05); margin-bottom: 0.8rem;">
                            <div style="font-weight: bold; color: #2c3e50;">{row['制造商']}</div>
                            <div style="font-size: 0.9rem;">{row['显卡名称']}</div>
                            <div style="font-size: 1.2rem; color: #3498db; font-weight: bold;">{row['显卡平均token']:.2f} token/s</div>
                            <div style="font-size: 0.8rem; color: #7f8c8d;">排名：{int(row['排名'])}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab3:
                st.markdown("<h3 class='sub-header'>显卡系列分析</h3>", unsafe_allow_html=True)
                
                # 提取NVIDIA系列信息（如GeForce、Tesla等）
                nvidia_df = filtered_df[filtered_df['显卡名称'].str.contains('NVIDIA')]
                
                # 提取系列名称
                def extract_series(name):
                    parts = name.split()
                    if len(parts) > 1:
                        if parts[1] == 'GeForce':
                            return 'GeForce'
                        elif parts[1] == 'Tesla':
                            return 'Tesla'
                        elif parts[1] == 'Quadro':
                            return 'Quadro'
                        elif parts[1] == 'TITAN':
                            return 'TITAN'
                        elif parts[1] == 'RTX' and 'Quadro' not in name:
                            return 'RTX Professional'
                        elif parts[1] == 'A' and len(parts[1]) <= 2:
                            return 'A Series'
                        elif parts[1] == 'H' and len(parts[1]) <= 2:
                            return 'H Series'
                        elif 'Jetson' in name:
                            return 'Jetson'
                        else:
                            return 'Other'
                    return 'Other'
                
                nvidia_df['系列'] = nvidia_df['显卡名称'].apply(extract_series)
                
                # 按系列分组计算平均性能
                series_perf = nvidia_df.groupby('系列')['显卡平均token'].mean().reset_index()
                series_perf = series_perf.sort_values('显卡平均token', ascending=False)
                
                # 统计各系列的显卡数量
                series_count = nvidia_df.groupby('系列').size().reset_index(name='数量')
                
                # NVIDIA系列平均性能
                fig = px.bar(
                    series_perf,
                    x='系列',
                    y='显卡平均token',
                    title='NVIDIA各系列GPU平均性能对比',
                    labels={'显卡平均token': '平均每秒处理token数', '系列': '系列'},
                    color='显卡平均token',
                    color_continuous_scale='Greens',
                    text='显卡平均token'
                )
                
                fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                fig.update_layout(
                    height=500,
                    xaxis_title="系列",
                    yaxis_title="平均每秒处理token数",
                    font=dict(size=12),
                    plot_bgcolor='rgba(240,240,240,0.8)'
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.plotly_chart(fig, use_container_width=True, key="series_performance")
                
                with col2:
                    # 系列占比饼图
                    fig = px.pie(
                        series_count,
                        values='数量',
                        names='系列',
                        title='NVIDIA各系列GPU数量占比',
                        color_discrete_sequence=px.colors.qualitative.Safe
                    )
                    
                    fig.update_layout(
                        height=500,
                        font=dict(size=12)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="series_share")
                
                # 提取GeForce系列的代数信息（如RTX 3000, RTX 4000等）
                geforce_df = nvidia_df[nvidia_df['显卡名称'].str.contains('GeForce')]
                
                # 提取代数信息
                def extract_generation(name):
                    if 'RTX 5' in name:
                        return 'RTX 5000'
                    elif 'RTX 4' in name:
                        return 'RTX 4000'
                    elif 'RTX 3' in name:
                        return 'RTX 3000'
                    elif 'RTX 2' in name:
                        return 'RTX 2000'
                    elif 'GTX 16' in name:
                        return 'GTX 1600'
                    elif 'GTX 10' in name:
                        return 'GTX 1000'
                    else:
                        return 'Other'
                
                if not geforce_df.empty:
                    geforce_df['代数'] = geforce_df['显卡名称'].apply(extract_generation)
                    
                    # 按代数分组计算平均性能
                    gen_perf = geforce_df.groupby('代数')['显卡平均token'].mean().reset_index()
                    gen_perf = gen_perf.sort_values('显卡平均token', ascending=False)
                    
                    # GeForce各代性能对比
                    fig = px.bar(
                        gen_perf,
                        x='代数',
                        y='显卡平均token',
                        title='GeForce各代GPU平均性能对比',
                        labels={'显卡平均token': '平均每秒处理token数', '代数': '代数'},
                        color='显卡平均token',
                        color_continuous_scale='Plasma',
                        text='显卡平均token'
                    )
                    
                    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                    fig.update_layout(
                        height=500,
                        xaxis_title="代数",
                        yaxis_title="平均每秒处理token数",
                        font=dict(size=12),
                        plot_bgcolor='rgba(240,240,240,0.8)'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="geforce_performance")
            
            with tab4:
                st.markdown("<h3 class='sub-header'>AI开发框架分析</h3>", unsafe_allow_html=True)
                
                # AI框架市场份额数据
                framework_data = {
                    'Framework': ['PyTorch', 'TensorFlow', 'MindSpore', 'PaddlePaddle', 'OneFlow', 'MXNet', 'MegEngine', 'Jittor', '其他'],
                    'Share': [34, 30, 11, 11, 3, 2, 2, 1, 6]
                }
                df_framework = pd.DataFrame(framework_data)
                
                # 创建饼图
                fig = px.pie(
                    df_framework,
                    values='Share',
                    names='Framework',
                    title='AI开发框架市场份额分布',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig.update_traces(textinfo='percent+label')
                fig.update_layout(
                    height=500,
                    font=dict(size=12),
                    title_x=0.5,
                    annotations=[dict(text='市场份额', x=0.5, y=0.5, font_size=20, showarrow=False)]
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.plotly_chart(fig, use_container_width=True, key="framework_share")
                
                with col2:
                    st.markdown("""
                    <div class="card">
                        <h4 style="color: #3498db;">AI框架市场分析</h4>
                        <ul>
                            <li>PyTorch和TensorFlow占据主导地位，合计64%市场份额</li>
                            <li>中国自研框架MindSpore和PaddlePaddle各占11%</li>
                            <li>新兴框架如OneFlow、MXNet等共占8%</li>
                            <li>其他小型框架占据6%市场份额</li>
                        </ul>
                        <p><strong>发展趋势：</strong></p>
                        <ul>
                            <li>开源框架持续主导市场</li>
                            <li>国产自研框架快速发展</li>
                            <li>专业化框架不断涌现</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab5:
                st.markdown("<h3 class='sub-header'>数据中心GPU市场分析</h3>", unsafe_allow_html=True)
                
                # 数据中心GPU市场份额数据
                market_data = {
                    'Year': ['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
                    'NVIDIA': [87.5, 91.9, 91.8, 96.6, 95.8, 97.3, 98.0, 94.0],
                    'AMD': [3.0, 7.8, 8.2, 3.4, 4.0, 2.6, 1.2, 4.2],
                    'Intel': [9.5, 0.3, 0.0, 0.0, 0.2, 0.1, 0.8, 1.8]
                }
                df_market = pd.DataFrame(market_data)
                
                # 创建折线图
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df_market['Year'],
                    y=df_market['NVIDIA'],
                    name='NVIDIA',
                    line=dict(color='#76b900', width=3),
                    mode='lines+markers'
                ))
                
                fig.add_trace(go.Scatter(
                    x=df_market['Year'],
                    y=df_market['AMD'],
                    name='AMD',
                    line=dict(color='#ed1c24', width=3),
                    mode='lines+markers'
                ))
                
                fig.add_trace(go.Scatter(
                    x=df_market['Year'],
                    y=df_market['Intel'],
                    name='Intel',
                    line=dict(color='#0071c5', width=3),
                    mode='lines+markers'
                ))
                
                fig.update_layout(
                    title='数据中心GPU市场份额趋势 (2017-2024)',
                    xaxis_title='年份',
                    yaxis_title='市场份额 (%)',
                    height=500,
                    hovermode='x unified',
                    yaxis=dict(range=[0, 100]),
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True, key="market_share_trend")
                
                # 市场分析说明
                st.markdown("""
                <div class="card">
                    <h4 style="color: #3498db;">市场格局分析</h4>
                    <ul>
                        <li><strong>NVIDIA主导地位：</strong>
                            <ul>
                                <li>市场份额持续保持在90%以上</li>
                                <li>2023年达到历史最高的98%</li>
                                <li>2024年预计仍将保持94%的高份额</li>
                            </ul>
                        </li>
                        <li><strong>AMD表现：</strong>
                            <ul>
                                <li>份额在1.2%-8.2%之间波动</li>
                                <li>2024年预计回升至4.2%</li>
                            </ul>
                        </li>
                        <li><strong>Intel发展：</strong>
                            <ul>
                                <li>正在重返数据中心GPU市场</li>
                                <li>2024年预计达到1.8%的份额</li>
                            </ul>
                        </li>
                    </ul>
                    <p><strong>市场趋势：</strong></p>
                    <ul>
                        <li>NVIDIA在AI计算领域优势明显</li>
                        <li>AMD和Intel正在加大投入追赶</li>
                        <li>市场竞争格局可能在未来发生变化</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with tab6:
                st.markdown("<h3 class='sub-header'>多维对比</h3>", unsafe_allow_html=True)
                
                # 多选特定显卡进行对比
                top_gpus = df.sort_values('显卡平均token', ascending=False).head(20)['显卡名称'].tolist()
                selected_gpus = st.multiselect(
                    "选择要比较的GPU:",
                    df['显卡名称'].tolist(),
                    default=top_gpus[:5]
                )
                
                if selected_gpus:
                    comparison_df = df[df['显卡名称'].isin(selected_gpus)]
                    comparison_df = comparison_df.sort_values('显卡平均token', ascending=False)
                    
                    # 创建雷达图
                    categories = ['性能', '排名', '显卡数量']
                    
                    fig = go.Figure()
                    
                    for _, row in comparison_df.iterrows():
                        # 归一化数据
                        performance = row['显卡平均token'] / df['显卡平均token'].max()
                        rank_inv = 1 - ((row['排名'] - 1) / (df['排名'].max() - 1))  # 排名越低，值越高
                        count = row['显卡数量'] / df['显卡数量'].max()
                        
                        fig.add_trace(go.Scatterpolar(
                            r=[performance, rank_inv, count],
                            theta=categories,
                            fill='toself',
                            name=row['显卡名称']
                        ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 1]
                            )
                        ),
                        title="GPU多维度比较",
                        height=600,
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="multi_comparison")
                    
                    # 创建并排条形图
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=comparison_df['显卡名称'],
                        y=comparison_df['显卡平均token'],
                        name='每秒处理token数',
                        marker_color='#3498db',
                        text=comparison_df['显卡平均token'].apply(lambda x: f"{x:.2f}")
                    ))
                    
                    fig.update_traces(textposition='outside')
                    fig.update_layout(
                        title="性能直接对比",
                        xaxis_title="GPU型号",
                        yaxis_title="每秒处理token数",
                        height=500,
                        font=dict(size=12),
                        plot_bgcolor='rgba(240,240,240,0.8)',
                        xaxis={'categoryorder': 'total descending'}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="direct_comparison")
                    
                    # 显示详细对比表格
                    st.markdown("<h4 style='color: #3498db;'>详细对比</h4>", unsafe_allow_html=True)
                    st.dataframe(
                        comparison_df[['显卡名称', '显卡数量', '每秒总token', '显卡平均token', '排名']],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                else:
                    st.warning("请选择至少一个GPU进行比较。")
        
        # === 筛选UI移动到底部 (注释掉，因为已移到侧边栏) ===
        # st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
        # st.markdown("<h3 style='color: #3498db; font-size: 1.3rem; margin-bottom: 1rem;'>数据筛选</h3>", unsafe_allow_html=True)
        # selected_manufacturers = st.multiselect(...) # Render widgets here
        # token_range = st.slider(...)
        # card_count_range = st.slider(...)
        # rank_range = st.slider(...)
        # st.markdown("</div>", unsafe_allow_html=True)
        
        # 添加页脚
        st.markdown("""
        <div class="footer">
            <p>数据来源: GPU性能测试 | 分析时间: 2024年</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("无法加载GPU排行数据文件，请确保文件路径正确。")

if __name__ == "__main__":
    main()