import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 读取数据
def load_data():
    # 跳过前3行说明文字
    df = pd.read_csv("data/nsf25326-tab001.csv", skiprows=3)
    # 清理列名
    df.columns = ['Year', 'GDP_Current', 'GDP_Constant', 'Deflator', 
                  'RD_Current', 'RD_Constant', 'RD_GDP_Total',
                  'RD_Perf_Business', 'RD_Perf_Federal', 'RD_Perf_HigherEd', 'RD_Perf_Other',
                  'RD_Fund_Business', 'RD_Fund_Federal', 'RD_Fund_Other']
    
    # 清理数据
    # 首先删除包含NaN的行
    df = df.dropna(subset=['Year'])
    # 然后清理Year列并转换为整数
    df['Year'] = df['Year'].str.replace('[a-zA-Z]', '', regex=True).astype(int)
    
    # 清理数值列中的逗号并转换为浮点数
    for col in df.columns:
        if col != 'Year' and col != 'Deflator':
            df[col] = df[col].astype(str).str.replace(',', '').astype(float)
    
    return df

# 加载数据
df = load_data()

# 1. 创建GDP和研发投入趋势图
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(
    go.Scatter(x=df['Year'], y=df['GDP_Constant'], name="GDP (2017不变美元)"),
    secondary_y=False,
)

fig1.add_trace(
    go.Scatter(x=df['Year'], y=df['RD_Constant'], name="研发投入 (2017不变美元)"),
    secondary_y=True,
)

fig1.update_layout(
    title="美国GDP与研发投入趋势 (1953-2023)",
    xaxis_title="年份",
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.8)')
)
fig1.update_yaxes(title_text="GDP (十亿美元)", secondary_y=False)
fig1.update_yaxes(title_text="研发投入 (十亿美元)", secondary_y=True)

# 2. 创建研发投入占GDP比例趋势图
fig2 = px.line(df, x='Year', y='RD_GDP_Total', 
               title='研发投入占GDP比例变化 (1953-2023)',
               labels={'Year': '年份', 'RD_GDP_Total': '研发投入占GDP比例 (%)'},
               line_shape='spline')
fig2.update_traces(line_color='#E41A1C', line_width=2)

# 3. 创建研发执行部门占比堆叠面积图
fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=df['Year'], y=df['RD_Perf_Business'],
    name='企业', stackgroup='one',
    line=dict(width=0.5), fillcolor='rgba(141, 211, 199, 0.8)'
))

fig3.add_trace(go.Scatter(
    x=df['Year'], y=df['RD_Perf_Federal'],
    name='联邦政府', stackgroup='one',
    line=dict(width=0.5), fillcolor='rgba(251, 180, 174, 0.8)'
))

fig3.add_trace(go.Scatter(
    x=df['Year'], y=df['RD_Perf_HigherEd'],
    name='高等教育', stackgroup='one',
    line=dict(width=0.5), fillcolor='rgba(190, 186, 218, 0.8)'
))

fig3.add_trace(go.Scatter(
    x=df['Year'], y=df['RD_Perf_Other'],
    name='其他', stackgroup='one',
    line=dict(width=0.5), fillcolor='rgba(251, 128, 114, 0.8)'
))

fig3.update_layout(
    title='研发执行部门占比变化 (1953-2023)',
    xaxis_title='年份',
    yaxis_title='占比 (%)',
    legend=dict(x=0.01, y=0.99)
)

# 4. 创建研发资金来源占比堆叠面积图
fig4 = go.Figure()

fig4.add_trace(go.Scatter(
    x=df['Year'], y=df['RD_Fund_Business'],
    name='企业', stackgroup='one',
    line=dict(width=0.5), fillcolor='rgba(141, 211, 199, 0.8)'
))

fig4.add_trace(go.Scatter(
    x=df['Year'], y=df['RD_Fund_Federal'],
    name='联邦政府', stackgroup='one',
    line=dict(width=0.5), fillcolor='rgba(251, 180, 174, 0.8)'
))

fig4.add_trace(go.Scatter(
    x=df['Year'], y=df['RD_Fund_Other'],
    name='其他', stackgroup='one',
    line=dict(width=0.5), fillcolor='rgba(251, 128, 114, 0.8)'
))

fig4.update_layout(
    title='研发资金来源占比变化 (1953-2023)',
    xaxis_title='年份',
    yaxis_title='占比 (%)',
    legend=dict(x=0.01, y=0.99)
)

# 5. 创建最近十年研发投入增长率柱状图
recent_df = df.tail(11)  # 获取最近11年数据以计算10年增长率
recent_df['RD_Growth'] = recent_df['RD_Constant'].pct_change() * 100

fig5 = px.bar(recent_df[1:],  # 跳过第一年（没有增长率）
              x='Year', y='RD_Growth',
              title='最近十年研发投入年增长率',
              labels={'Year': '年份', 'RD_Growth': '增长率 (%)'},
              color='RD_Growth',
              color_continuous_scale='RdBu',
              color_continuous_midpoint=0)

# 保存图表为HTML文件
fig1.write_html("gdp_rd_trend.html")
fig2.write_html("rd_gdp_ratio.html")
fig3.write_html("rd_performer.html")
fig4.write_html("rd_funding.html")
fig5.write_html("rd_growth.html")

# 显示所有图表
fig1.show()
fig2.show()
fig3.show()
fig4.show()
fig5.show()

# 输出一些关键统计数据
latest_year = df['Year'].max()
latest_data = df[df['Year'] == latest_year].iloc[0]

print(f"\n关键统计数据 ({latest_year}年):")
print(f"GDP (2017不变美元): {latest_data['GDP_Constant']:.1f} 十亿美元")
print(f"研发投入 (2017不变美元): {latest_data['RD_Constant']:.1f} 十亿美元")
print(f"研发投入占GDP比例: {latest_data['RD_GDP_Total']:.2f}%")
print(f"企业执行研发占比: {latest_data['RD_Perf_Business']:.2f}%")
print(f"企业资助研发占比: {latest_data['RD_Fund_Business']:.2f}%")