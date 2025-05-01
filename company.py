import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 设置页面标题
st.set_page_config(page_title="全球独角兽公司分析", layout="wide")

# 读取数据
@st.cache_data
def load_data():
    df = pd.read_csv("data/主要国家独角兽公司数量.csv")
    # 将第一列设置为索引
    df = df.set_index('OUNT EXITED Locations')
    return df

df = load_data()

# 页面标题
st.title("🦄 全球独角兽公司分析仪表板")

# 侧边栏 - 年份选择
years = df.columns.astype(int).tolist()
selected_year = st.sidebar.selectbox("选择年份", years, index=len(years)-2)

# 主要指标
col1, col2, col3 = st.columns(3)
year_data = df[str(selected_year)].sort_values(ascending=False)

with col1:
    st.metric("总独角兽公司数量", f"{year_data.sum():,}")
    
with col2:
    top_country = year_data.index[0]
    st.metric("最多独角兽公司的国家", f"{top_country} ({year_data.iloc[0]:,})")
    
with col3:
    countries_with_unicorns = len(year_data[year_data > 0])
    st.metric("拥有独角兽公司的国家数量", countries_with_unicorns)

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    # 前10国家柱状图
    st.subheader(f"{selected_year}年各国独角兽公司数量（前10名）")
    top10_countries = year_data.nlargest(10)
    fig_bar = px.bar(
        x=top10_countries.index,
        y=top10_countries.values,
        labels={'x': '国家', 'y': '独角兽公司数量'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # 饼图展示份额
    st.subheader(f"{selected_year}年独角兽公司地理分布")
    top5_countries = year_data.nlargest(5)
    others = pd.Series({'其他': year_data[~year_data.index.isin(top5_countries.index)].sum()})
    pie_data = pd.concat([top5_countries, others])
    fig_pie = px.pie(
        values=pie_data.values,
        names=pie_data.index,
        hole=0.3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# 时间趋势分析
st.subheader("主要国家独角兽公司数量趋势（2015-2024）")
top5_countries = year_data.nlargest(5)
fig_line = go.Figure()

for country in top5_countries.index:
    fig_line.add_trace(go.Scatter(
        x=years,
        y=df.loc[country],
        name=country,
        mode='lines+markers'
    ))

fig_line.update_layout(
    xaxis_title="年份",
    yaxis_title="独角兽公司数量",
    legend_title="国家"
)
st.plotly_chart(fig_line, use_container_width=True)

# 数据表格展示
st.subheader("原始数据")
st.dataframe(df)



