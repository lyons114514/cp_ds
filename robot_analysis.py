import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
def load_data():
    # 读取工业机器人装机数量数据
    robot_installation = pd.read_csv('data/工业机器人/工业机器人装机数量.csv')
    
    # 读取机器人应用领域数据
    robot_application = pd.read_csv('data/工业机器人/机器人应用领域.csv')
    
    # 读取中国工业机器人部署与密度数据
    china_deployment = pd.read_csv('data/工业机器人/中国工业机器人部署与密度_年度数据.csv')
    
    # 读取中国工业机器人社会经济影响数据
    china_impact = pd.read_csv('data/工业机器人/中国工业机器人社会经济影响_年度数据.csv')
    
    # 读取中国工业机器人应用领域分布数据
    china_distribution = pd.read_csv('data/工业机器人/中国工业机器人应用领域分布_年度数据.csv')
    
    # 读取中国vs全球机器人数据
    china_vs_global = pd.read_csv('data/工业机器人/中国vs全球机器人.csv')
    
    return (robot_installation, robot_application, china_deployment, 
            china_impact, china_distribution, china_vs_global)

def analyze_china_correlations(china_deployment, china_impact):
    """分析中国工业机器人发展与社会经济指标的相关性"""
    # 合并数据
    merged_data = pd.merge(china_deployment, china_impact, on='Year')
    
    # 打印列名，用于调试
    print("可用的列名：", merged_data.columns.tolist())
    
    # 选择关键指标进行相关性分析
    key_metrics = [
        '年安装量(千台)', 
        '机器人密度(每万名工人)', 
        '机器人国产化率(按销量,%)',
        '制造业生产率指数(2015=100)', 
        '机器人相关新增岗位(万个)', 
        '机器人产业投资额(亿元人民币)'
    ]
    
    # 验证所有指标是否存在
    for metric in key_metrics:
        if metric not in merged_data.columns:
            print(f"警告：列 '{metric}' 不存在于数据中")
    
    # 只使用存在的列进行相关性分析
    available_metrics = [metric for metric in key_metrics if metric in merged_data.columns]
    correlation_matrix = merged_data[available_metrics].corr()
    
    # 绘制相关性热力图
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('中国工业机器人发展与社会经济指标相关性分析')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png')
    plt.close()
    
    return correlation_matrix

def analyze_global_trends(robot_installation):
    """分析全球主要国家工业机器人装机趋势"""
    # 数据透视
    pivot_data = robot_installation.pivot(index='Year', 
                                        columns='Geographic area',
                                        values='Number of industrial robots installed (in thousands)')
    
    # 计算增长率
    growth_rates = pivot_data.pct_change().mean()
    
    # 计算各国装机量与时间的相关性
    correlations = {}
    for country in pivot_data.columns:
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            range(len(pivot_data)), pivot_data[country])
        correlations[country] = r_value
    
    return growth_rates, correlations

def analyze_industry_impact(robot_application):
    """分析不同行业机器人应用的影响"""
    # 计算各行业机器人应用占比
    industry_total = robot_application.groupby('Year')['Number of industrial robots installed (in thousands)'].sum()
    industry_shares = robot_application.pivot_table(
        index='Year',
        columns='Sector',
        values='Number of industrial robots installed (in thousands)',
        aggfunc='sum'
    ).div(industry_total, axis=0) * 100
    
    return industry_shares

def main():
    # 加载数据
    (robot_installation, robot_application, china_deployment, 
     china_impact, china_distribution, china_vs_global) = load_data()
    
    # 1. 分析中国工业机器人发展与社会经济指标的相关性
    correlation_matrix = analyze_china_correlations(china_deployment, china_impact)
    print("\n中国工业机器人发展与社会经济指标相关性分析结果：")
    print(correlation_matrix)
    
    # 2. 分析全球主要国家工业机器人装机趋势
    growth_rates, correlations = analyze_global_trends(robot_installation)
    print("\n各国工业机器人装机量年均增长率：")
    print(growth_rates)
    print("\n各国装机量趋势相关性：")
    print(correlations)
    
    # 3. 分析行业应用影响
    industry_shares = analyze_industry_impact(robot_application)
    print("\n各行业机器人应用占比趋势：")
    print(industry_shares)

if __name__ == "__main__":
    main() 