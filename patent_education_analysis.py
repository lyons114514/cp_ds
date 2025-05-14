import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体，确保图表能正确显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
education_funding = pd.read_csv('data/专利教育/china_education_funding.csv')
ai_models = pd.read_csv('data/专利教育/历年知名AI模型数量_地区对比.csv')
ai_patents = pd.read_csv('data/专利教育/全球AI专利占比_按地区.csv')

# 数据预处理 - 教育经费
education_funding_melted = pd.melt(education_funding, 
                                 id_vars=['指标'], 
                                 var_name='年份', 
                                 value_name='经费')
education_funding_melted['年份'] = education_funding_melted['年份'].str.replace('年', '').astype(int)
education_funding_melted['经费'] = education_funding_melted['经费'].astype(float)

# 数据预处理 - AI模型数量
ai_models_china = ai_models[ai_models['地区'] == '中国']

def get_correlation_strength(correlation):
    """根据相关系数判断相关强度"""
    abs_corr = abs(correlation)
    if abs_corr >= 0.8:
        return '强相关'
    elif abs_corr >= 0.5:
        return '中等相关'
    elif abs_corr >= 0.3:
        return '弱相关'
    else:
        return '极弱相关或无相关'

def format_number(number):
    """格式化大数字，添加千位分隔符"""
    return "{:,}".format(int(number)) # 确保输入为整数进行格式化

def plot_heatmap(data, columns, title, filename):
    """绘制并保存相关性热力图"""
    plt.figure(figsize=(10, 8))
    corr_matrix = data[columns].corr(method='spearman')
    sns.heatmap(corr_matrix, 
                annot=True, 
                cmap='coolwarm', 
                vmin=-1, 
                vmax=1,
                center=0,
                fmt='.3f')
    plt.title(title)
    plt.show()
    plt.close()
    print(f"\n图表已保存为: {filename}")

# 回归分析
def regression_analysis():
    merged_data = pd.merge(education_funding_melted, 
                          ai_models_china,
                          left_on='年份',
                          right_on='年份',
                          how='inner')
    
    X = merged_data['经费'].values
    y = merged_data['知名AI模型数量'].values
    
    # 线性回归
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='实际数据')
    plt.plot(X, slope * X + intercept, color='red', label='回归线')
    plt.title('教育经费与AI模型数量回归分析')
    plt.xlabel('教育经费(万元)')
    plt.ylabel('AI模型数量')
    plt.legend()
    plt.show()
    plt.close()
    print("\n图表已保存为: regression_analysis.png")
    
    print("\n4. 回归分析结果：")
    print(f"   - 斜率: {slope:.2e}")
    print(f"   - 截距: {intercept:.2f}")
    print(f"   - R平方: {r_value**2:.3f}")
    print(f"   - P值: {p_value:.3f}")
    print(f"   - 标准误差: {std_err:.2e}")

def analyze_correlations():
    print("\n=== 教育经费与AI发展相关性分析报告 ===\n")
    
    # --- 教育经费与AI模型数量 --- 
    merged_models = pd.merge(education_funding_melted, 
                             ai_models_china,
                             left_on='年份',
                             right_on='年份',
                             how='inner')
    
    spearman_corr_model, p_value_model = stats.spearmanr(merged_models['经费'], 
                                                         merged_models['知名AI模型数量'])
    
    print("1. 教育经费与AI模型数量相关性：")
    print(f"   - 相关系数: {spearman_corr_model:.3f}")
    print(f"   - 相关强度: {get_correlation_strength(spearman_corr_model)}")
    print(f"   - P值: {p_value_model:.3f}")
    print(f"   - 统计显著性: {'显著' if p_value_model < 0.05 else '不显著'}")
    
    # 绘制模型相关性热力图
    plot_heatmap(merged_models, 
                 ['经费', '知名AI模型数量'], 
                 '教育经费与AI模型数量斯皮尔曼相关性', 
                 'spearman_models_correlation.png')

    # --- 教育经费与AI专利占比 --- 
    china_patents = ai_patents[ai_patents['地区'] == '中国']
    if not china_patents.empty:
        merged_patents = pd.merge(education_funding_melted,
                                china_patents,
                                left_on='年份',
                                right_on='年份',
                                how='inner')
        if not merged_patents.empty:
            patent_column_name = 'AI专利占比(占全球总数百分比)'
            spearman_corr_patent, p_value_patent = stats.spearmanr(merged_patents['经费'],
                                                                  merged_patents[patent_column_name])
            
            print("\n2. 教育经费与AI专利占比相关性：")
            print(f"   - 相关系数: {spearman_corr_patent:.3f}")
            print(f"   - 相关强度: {get_correlation_strength(spearman_corr_patent)}")
            print(f"   - P值: {p_value_patent:.3f}")
            print(f"   - 统计显著性: {'显著' if p_value_patent < 0.05 else '不显著'}")

            # 绘制专利相关性热力图
            plot_heatmap(merged_patents, 
                         ['经费', patent_column_name], 
                         '教育经费与AI专利占比斯皮尔曼相关性', 
                         'spearman_patents_correlation.png')
            
            # --- 年度对比数据 --- 
            print("\n3. 关键年份数据对比：")
            merged_all = pd.merge(merged_models, china_patents[['年份', patent_column_name]], on='年份', how='inner')
            merged_all = merged_all.sort_values('年份')
            
            print("\n   年份    教育经费(万元)    AI模型数量    AI专利占比(%)")
            print("   " + "-" * 60)
            for _, row in merged_all.iterrows():
                year = str(row['年份'])
                funding = format_number(row['经费'])
                models = str(int(row['知名AI模型数量']))
                patents = f"{row[patent_column_name]:.1f}"
                
                print(f"   {year:4s}    {funding:>15s}    {models:>10s}    {patents:>12s}")
            print("")

if __name__ == '__main__':
    analyze_correlations()
    regression_analysis()