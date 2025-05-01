import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2196F3;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px #ccc;
    }
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 5px solid #2196F3;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #2196F3;
    }
    .metric-label {
        font-size: 0.95rem;
        color: #555;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# 从CSV文件加载数据
@st.cache_data
def load_data():
    try:
        ai_capabilities = pd.read_csv('data/ai_capabilities.csv')
        market_share = pd.read_csv('data/market_share.csv')
        ai_adoption = pd.read_csv('data/ai_adoption.csv')
        return ai_capabilities, market_share, ai_adoption
    except FileNotFoundError:
        st.error("找不到必要的数据文件。请确保data目录下存在所需的CSV文件。")
        return None, None, None

# 加载数据
ai_capabilities, market_share, ai_adoption = load_data()

# 检查数据是否成功加载
if ai_capabilities is None or market_share is None or ai_adoption is None:
    st.stop()

# 页面标题
st.markdown("<h1 class='main-header'>服务机器人AI应用分析</h1>", unsafe_allow_html=True)

# 创建三个标签页
tab1, tab2, tab3 = st.tabs([
    "🎯 AI能力分析",
    "📊 市场分布",
    "🔄 AI普及率"
])

# Tab 1: AI能力分析
with tab1:
    st.subheader("AI技术在服务机器人中的应用成熟度与效果")
    
    # 创建双柱状图
    fig = go.Figure()
    
    # 添加技术成熟度柱状图
    fig.add_trace(go.Bar(
        x=ai_capabilities['应用领域'],
        y=ai_capabilities['技术成熟度'],
        name='技术成熟度',
        marker_color='lightblue'
    ))
    
    # 添加应用效果提升柱状图
    fig.add_trace(go.Bar(
        x=ai_capabilities['应用领域'],
        y=ai_capabilities['应用效果提升'],
        name='应用效果提升',
        marker_color='lightgreen'
    ))
    
    # 更新布局
    fig.update_layout(
        title="AI技术在服务机器人中的应用成熟度与效果",
        xaxis_title="应用领域",
        yaxis_title="百分比 (%)",
        barmode='group',
        yaxis_range=[0, 100]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    **主要发现：**
    * 环境感知和人机交互领域的AI技术最为成熟，技术成熟度分别达到{ai_capabilities['技术成熟度'].iloc[0]:.1f}%和{ai_capabilities['技术成熟度'].iloc[1]:.1f}%
    * 所有领域的应用效果提升都高于技术成熟度，表明AI技术带来了显著的性能提升
    * 场景理解虽然技术成熟度相对较低({ai_capabilities['技术成熟度'].iloc[-1]:.1f}%)，但仍带来了{ai_capabilities['应用效果提升'].iloc[-1]:.1f}%的效果提升
    """)

# Tab 2: 市场分布
with tab2:
    st.subheader("服务机器人应用场景市场份额分布")
    
    # 创建饼图
    fig_pie = px.pie(
        market_share,
        values='市场份额',
        names='应用场景',
        title='服务机器人应用场景市场份额分布 (2023)',
        hole=0.4
    )
    
    # 更新布局
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown(f"""
    **市场分布特点：**
    * 物流配送占据最大市场份额({market_share['市场份额'].iloc[0]:.1f}%)，显示出最广泛的商业化应用
    * 餐饮服务({market_share['市场份额'].iloc[1]:.1f}%)和医疗服务({market_share['市场份额'].iloc[2]:.1f}%)是第二、三大应用场景
    * 教育({market_share['市场份额'].iloc[3]:.1f}%)和商业服务({market_share['市场份额'].iloc[4]:.1f}%)显示出增长潜力
    """)

# Tab 3: AI普及率
with tab3:
    st.subheader("各应用场景AI功能普及率")
    
    # 创建水平条形图
    fig_bar = px.bar(
        ai_adoption.sort_values('AI功能普及率', ascending=True),
        x='AI功能普及率',
        y='应用场景',
        orientation='h',
        title='各场景AI功能普及率分析'
    )
    
    # 更新布局
    fig_bar.update_layout(
        xaxis_title="AI功能普及率 (%)",
        yaxis_title="应用场景",
        xaxis_range=[0, 100]
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown(f"""
    **AI普及率分析：**
    * 物流配送领域AI功能普及率最高，达到{ai_adoption['AI功能普及率'].max():.1f}%
    * 餐饮服务和医疗服务AI普及率分别为{ai_adoption['AI功能普及率'].iloc[1]:.1f}%和{ai_adoption['AI功能普及率'].iloc[2]:.1f}%
    * 即使是普及率最低的其他领域也达到了{ai_adoption['AI功能普及率'].min():.1f}%，显示AI技术已经广泛渗透到服务机器人领域
    """)

# 页脚
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>数据来源：中国机器人产业创新中心，中国电子学会 | 更新时间：2024年</div>", unsafe_allow_html=True)
