import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def load_sales_data():
    # 各地区年度销量数据
    sales_data = pd.DataFrame({
        '年份': [2019, 2020, 2021, 2022, 2023],
        '中国': [120.6, 136.7, 352.1, 688.7, 949.0],
        '欧洲': [56.4, 137.3, 225.9, 282.9, 310.0],
        '美国': [32.6, 29.6, 66.3, 100.7, 140.0],
        '其他地区': [29.4, 31.4, 65.7, 97.7, 121.0]
    })
    return sales_data

def load_market_share_2023():
    # 2023年市场份额数据
    market_share = pd.DataFrame({
        '地区': ['中国', '欧洲', '美国', '其他地区'],
        '份额': [62.4, 20.4, 9.2, 8.0]
    })
    return market_share

def load_feature_penetration():
    # 智能座舱功能渗透率数据
    feature_data = pd.DataFrame({
        '功能': ['语音交互', '人脸识别', '手势控制', 'AR-HUD', '疲劳检测'],
        '2021年': [44, 24, 14, 8, 19],
        '2022年': [63, 36, 22, 14, 28],
        '2023年': [85, 53, 33, 28, 43]
    })
    return feature_data

def load_region_data():
    # 各地区数据采集能力数据
    region_data = pd.DataFrame({
        '地区': ['中国', '北美', '欧洲', '其他'],
        '数据量': [889, 328, 288, 148],
        '场景数': [12327, 11960, 10875, 6869]
    })
    return region_data

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
    .sub-header {
        font-size: 1.8rem;
        color: #1976D2;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .insight-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 页面标题
    st.markdown("<h1 class='main-header'>新能源汽车市场分析</h1>", unsafe_allow_html=True)

    # 创建五个标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 销量趋势分析",
        "🥧 市场份额分布",
        "🚘 智能座舱分析",
        "🌍 区域数据分析",
    
    ])

    # Tab 1: 销量趋势分析
    with tab1:
        st.markdown("<h2 class='sub-header'>全球新能源汽车销量趋势</h2>", unsafe_allow_html=True)
        
        sales_data = load_sales_data()
        
        # 创建堆叠面积图
        fig = go.Figure()
        
        regions = ['中国', '欧洲', '美国', '其他地区']
        colors = ['rgb(33, 150, 243)', 'rgb(255, 167, 38)', 'rgb(76, 175, 80)', 'rgb(244, 67, 54)']
        
        for region, color in zip(regions, colors):
            fig.add_trace(go.Scatter(
                x=sales_data['年份'],
                y=sales_data[region],
                name=region,
                stackgroup='one',
                fillcolor=color,
                line=dict(color=color)
            ))
        
        fig.update_layout(
            title="2019-2023年全球新能源汽车销量趋势",
            xaxis_title="年份",
            yaxis_title="销量（万辆）",
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 计算年度增长率
        total_sales = sales_data[regions].sum(axis=1)
        growth_rates = (total_sales.pct_change() * 100).round(1)
        
        st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
        st.markdown("**市场增长分析：**")
        st.markdown(f"""
        * 2023年全球总销量达到{total_sales.iloc[-1]:.1f}万辆
        * 2023年中国市场销量{sales_data['中国'].iloc[-1]:.1f}万辆，同比增长{((sales_data['中国'].iloc[-1]/sales_data['中国'].iloc[-2]-1)*100):.1f}%
        * 欧洲市场保持稳定增长，2023年达到{sales_data['欧洲'].iloc[-1]:.1f}万辆
        * 美国市场增速加快，2023年销量突破{sales_data['美国'].iloc[-1]:.1f}万辆
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # Tab 2: 市场份额分布
    with tab2:
        st.markdown("<h2 class='sub-header'>2023年全球市场份额分布</h2>", unsafe_allow_html=True)
        
        market_share = load_market_share_2023()
        
        # 创建饼图
        fig = px.pie(
            market_share,
            values='份额',
            names='地区',
            title='2023年全球新能源汽车市场份额分布',
            color_discrete_sequence=['rgb(33, 150, 243)', 'rgb(255, 167, 38)', 'rgb(76, 175, 80)', 'rgb(244, 67, 54)']
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
        st.markdown("**市场格局分析：**")
        st.markdown("""
        * 中国市场占据全球62.4%的份额，处于绝对领先地位
        * 欧洲市场份额为20.4%，是全球第二大市场
        * 美国市场占比9.2%，发展潜力巨大
        * 其他地区合计占比8.0%，市场空间待开发
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # Tab 3: 智能座舱分析
    with tab3:
        st.markdown("<h2 class='sub-header'>智能座舱功能渗透率趋势</h2>", unsafe_allow_html=True)
        
        feature_data = load_feature_penetration()
        
        # 创建分组柱状图
        fig = go.Figure()
        
        years = ['2021年', '2022年', '2023年']
        colors = ['rgb(33, 150, 243)', 'rgb(255, 167, 38)', 'rgb(76, 175, 80)']
        
        for year, color in zip(years, colors):
            fig.add_trace(go.Bar(
                name=year,
                x=feature_data['功能'],
                y=feature_data[year],
                marker_color=color
            ))
        
        fig.update_layout(
            title="智能座舱主要功能渗透率变化",
            xaxis_title="功能类型",
            yaxis_title="渗透率（%）",
            barmode='group',
            yaxis_range=[0, 100]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
        st.markdown("**功能渗透分析：**")
        st.markdown("""
        * 语音交互渗透率最高，2023年达到85%，是最成熟的智能座舱功能
        * 人脸识别技术快速普及，渗透率从24%提升至53%
        * AR-HUD虽然基数较低，但增长最快，2023年达到28%
        * 疲劳检测等安全相关功能稳步提升，2023年达到43%
        """)
        st.markdown("</div>", unsafe_allow_html=True)


    with tab4:
        st.markdown("<h2 class='sub-header'>区域数据分析</h2>", unsafe_allow_html=True)
        
        region_data = load_region_data()
        
        # 创建复合图表
        fig = go.Figure()
        
        # 添加柱状图（数据量）
        fig.add_trace(go.Bar(
            x=region_data['地区'],
            y=region_data['数据量'],
            name='数据量(TB)',
            marker_color='lightblue'
        ))
        
        # 添加折线图（场景数）
        fig.add_trace(go.Scatter(
            x=region_data['地区'],
            y=region_data['场景数'],
            name='场景数',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='red', width=2),
            marker=dict(size=8)
        ))
        
        # 更新布局
        fig.update_layout(
            title="各地区自动驾驶数据采集能力对比",
            xaxis_title="地区",
            yaxis_title="数据量 (TB)",
            yaxis2=dict(
                title="场景数",
                overlaying='y',
                side='right'
            ),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=1.1,
                xanchor="left",
                x=0
            ),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
        st.markdown("**数据采集能力分析：**")
        st.markdown(f"""
        * 中国在数据量方面遥遥领先，达到{region_data.loc[region_data['地区']=='中国', '数据量'].values[0]} TB，是第二名北美（{region_data.loc[region_data['地区']=='北美', '数据量'].values[0]} TB）的近3倍
        * 欧洲在场景数量上表现突出，有{region_data.loc[region_data['地区']=='欧洲', '场景数'].values[0]:,}个场景，这表明其在多样化测试环境方面具有优势
        * 其他地区虽然数据量相对较少（{region_data.loc[region_data['地区']=='其他', '数据量'].values[0]} TB），但场景数达到{region_data.loc[region_data['地区']=='其他', '场景数'].values[0]:,}个，显示出良好的场景多样性
        * 北美地区在数据量和场景数方面都保持稳定表现，数据量为{region_data.loc[region_data['地区']=='北美', '数据量'].values[0]} TB，场景数{region_data.loc[region_data['地区']=='北美', '场景数'].values[0]:,}个
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 添加数据表格展示
        st.markdown("<h3 class='sub-header'>详细数据</h3>", unsafe_allow_html=True)
        st.dataframe(
            region_data,
            column_config={
                "地区": st.column_config.TextColumn("地区"),
                "数据量": st.column_config.NumberColumn("数据量(TB)", format="%d"),
                "场景数": st.column_config.NumberColumn("场景数", format="%d")
            },
            hide_index=True
        )

  
    
  
if __name__ == "__main__":
    main()
