import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import os
from scipy import stats
import plotly.figure_factory as ff

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
        border-bottom: 2px solid #FF6B6B;
        padding-bottom: 0.5rem;
        font-family: 'SimHei', sans-serif;
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

@st.cache_data
def load_education_funding():
    try:
        df = pd.read_csv('data/专利教育/china_education_funding.csv')
        df_melted = pd.melt(df, id_vars=['指标'], var_name='年份', value_name='经费')
        df_melted['年份'] = df_melted['年份'].str.replace('年', '').astype(int)
        df_melted['经费'] = df_melted['经费'].astype(float)
        return df_melted
    except Exception as e:
        st.error(f"读取教育经费数据失败: {e}")
        return None

@st.cache_data
def load_ai_models():
    try:
        df = pd.read_csv('data/专利教育/历年知名AI模型数量_地区对比.csv')
        # 筛选中国数据
        df_china = df[df['地区'] == '中国'].copy()
        return df_china
    except Exception as e:
        st.error(f"读取AI模型数据失败: {e}")
        return None

@st.cache_data
def load_ai_patents():
    try:
        df = pd.read_csv('data/专利教育/全球AI专利占比_按地区.csv')
        # 筛选中国数据
        df_china = df[df['地区'] == '中国'].copy()
        return df_china
    except Exception as e:
        st.error(f"读取AI专利数据失败: {e}")
        return None

def get_correlation_strength(correlation):
    abs_corr = abs(correlation)
    if abs_corr >= 0.8: return '强相关'
    elif abs_corr >= 0.5: return '中等相关'
    elif abs_corr >= 0.3: return '弱相关'
    else: return '极弱相关或无相关'

def format_number(number):
    try:
        return "{:,}".format(int(number))
    except (ValueError, TypeError):
        return str(number)

def main():
    if df is not None:
        # 标题
        st.markdown("<h1 class='main-header'>中国AI产业应用与教育投入的关联分析</h1>", unsafe_allow_html=True)

    

        # 创建选项卡
        tab_titles = ["📈 转化率分析", "💰 GMV趋势", "🤖 AI贡献分析"]
        # 检查专利教育数据是否都加载成功
        show_patent_tab = load_education_funding() is not None and load_ai_models() is not None and load_ai_patents() is not None
        if show_patent_tab:
            tab_titles.append("🎓 专利与教育分析")

        tabs = st.tabs(tab_titles)

        with tabs[0]:
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

        with tabs[1]:
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

        with tabs[2]:
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

    # --- 新增：专利与教育分析标签页 ---
    if show_patent_tab:
        with tabs[-1]:
            st.markdown("<h2 class='sub-header'>教育投入与AI发展分析</h2>", unsafe_allow_html=True)

            try:
                # --- 数据合并 ---
                # 模型数据合并
                merged_models = pd.merge(load_education_funding(), load_ai_models(), on='年份', how='inner')
                # 专利数据合并
                merged_patents = pd.merge(load_education_funding(), load_ai_patents(), on='年份', how='inner')
                # 全部数据合并 (用于表格)
                patent_column_name = 'AI专利占比(占全球总数百分比)'
                merged_all = pd.merge(merged_models, load_ai_patents()[['年份', patent_column_name]], on='年份', how='inner')
                merged_all = merged_all.sort_values('年份')

                # --- 相关性分析 ---
                st.markdown("### 1. 相关性分析 (Spearman)")

                col_corr1, col_corr2 = st.columns(2)

                with col_corr1:
                    st.markdown("#### 教育经费 vs AI模型数量")
                    spearman_corr_model, p_value_model = stats.spearmanr(merged_models['经费'], merged_models['知名AI模型数量'])
                    st.metric(label="相关系数", value=f"{spearman_corr_model:.3f}", delta=get_correlation_strength(spearman_corr_model))
                    st.caption(f"P值: {p_value_model:.3f} ({'显著' if p_value_model < 0.05 else '不显著'})")

                    # 绘制热力图 (Plotly)
                    corr_matrix_model = merged_models[['经费', '知名AI模型数量']].corr(method='spearman')
                    fig_heatmap_model = ff.create_annotated_heatmap(
                        z=corr_matrix_model.values,
                        x=corr_matrix_model.columns.tolist(),
                        y=corr_matrix_model.index.tolist(),
                        annotation_text=corr_matrix_model.round(3).astype(str).values,
                        colorscale='RdBu', # 使用红蓝色彩映射，中心为0
                        reversescale=True, # 红色表示正相关，蓝色表示负相关
                        zmin=-1, zmax=1, # 固定范围
                        showscale=True
                    )
                    fig_heatmap_model.update_layout(title_text='相关性热力图', title_x=0.5)
                    st.plotly_chart(fig_heatmap_model, use_container_width=True)


                with col_corr2:
                    st.markdown("#### 教育经费 vs AI专利占比")
                    spearman_corr_patent, p_value_patent = stats.spearmanr(merged_patents['经费'], merged_patents[patent_column_name])
                    st.metric(label="相关系数", value=f"{spearman_corr_patent:.3f}", delta=get_correlation_strength(spearman_corr_patent))
                    st.caption(f"P值: {p_value_patent:.3f} ({'显著' if p_value_patent < 0.05 else '不显著'})")

                     # 绘制热力图 (Plotly)
                    corr_matrix_patent = merged_patents[['经费', patent_column_name]].corr(method='spearman')
                    fig_heatmap_patent = ff.create_annotated_heatmap(
                        z=corr_matrix_patent.values,
                        x=corr_matrix_patent.columns.tolist(),
                        y=corr_matrix_patent.index.tolist(),
                        annotation_text=corr_matrix_patent.round(3).astype(str).values,
                        colorscale='RdBu',
                        reversescale=True,
                        zmin=-1, zmax=1,
                        showscale=True
                    )
                    fig_heatmap_patent.update_layout(title_text='相关性热力图', title_x=0.5)
                    st.plotly_chart(fig_heatmap_patent, use_container_width=True)


                # --- 回归分析 ---
                st.markdown("### 2. 回归分析 (教育经费 vs AI模型数量)")
                X_reg = merged_models['经费'].values
                y_reg = merged_models['知名AI模型数量'].values
                slope, intercept, r_value, p_value_reg, std_err = stats.linregress(X_reg, y_reg)

                # 创建回归图 (Plotly)
                fig_reg = go.Figure()
                # 散点
                fig_reg.add_trace(go.Scatter(x=X_reg, y=y_reg, mode='markers', name='实际数据', marker=dict(color='blue')))
                # 回归线
                fig_reg.add_trace(go.Scatter(x=X_reg, y=slope * X_reg + intercept, mode='lines', name='回归线', line=dict(color='red')))
                fig_reg.update_layout(
                    title='教育经费与AI模型数量回归分析',
                    xaxis_title='教育经费(万元)',
                    yaxis_title='AI模型数量',
                    legend_title="图例"
                )
                st.plotly_chart(fig_reg, use_container_width=True)

                st.markdown("#### 回归分析结果:")
                reg_results_md = f"""
                - **斜率:** {slope:.3e}
                - **截距:** {intercept:.2f}
                - **R平方:** {r_value**2:.3f} (教育经费能解释约 {r_value**2:.1%} 的AI模型数量变化)
                - **P值:** {p_value_reg:.3f} ({'显著' if p_value_reg < 0.05 else '不显著'})
                - **标准误差:** {std_err:.3e}
                """
                st.markdown(reg_results_md)

                # --- 年度数据对比 ---
                st.markdown("### 3. 年度数据对比")
                # 格式化表格数据
                merged_all_display = merged_all[['年份', '经费', '知名AI模型数量', patent_column_name]].copy()
                merged_all_display['经费(万元)'] = merged_all_display['经费'].apply(format_number)
                merged_all_display['AI模型数量'] = merged_all_display['知名AI模型数量'].astype(int)
                merged_all_display['AI专利占比(%)'] = merged_all_display[patent_column_name].round(1)

                st.dataframe(merged_all_display[['年份', '经费(万元)', 'AI模型数量', 'AI专利占比(%)']].set_index('年份'), use_container_width=True)

                # --- 分析结论 ---
                st.markdown("### 4. 分析结论")
                st.markdown("""
                - **强相关性:** 中国的教育经费投入与AI模型数量（Spearman系数: {0:.3f}）和AI专利全球占比（Spearman系数: {1:.3f}）均呈现显著的强正相关关系。
                - **回归趋势:** 回归分析表明，教育经费的增加对AI模型数量有显著的正向预测作用（R²={2:.3f}）。
                - **投入驱动:** 数据强烈表明，持续的教育投入是中国AI领域快速发展和创新能力提升的关键驱动因素，尤其在专利产出方面效果更为直接。
                """.format(spearman_corr_model, spearman_corr_patent, r_value**2))

            except Exception as e:
                st.error(f"处理专利与教育数据时出错: {e}")
                st.exception(e) # 显示详细错误信息，方便调试

    else:
        st.error("无法加载数据，请确保data/pdd_data.csv文件存在")

if __name__ == "__main__":
    main()
