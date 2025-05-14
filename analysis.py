import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
nsf_data = pd.read_csv('data/nsf25326-tab001.csv', skiprows=3)
ai_models = pd.read_csv('data/专利教育/历年知名AI模型数量_地区对比.csv')
patents = pd.read_csv('data/专利教育/全球AI专利占比_按地区.csv')

# 数据预处理
nsf_data = nsf_data[nsf_data.iloc[:, 0].notna()]  # 移除空行
nsf_data.columns = ['Year', 'GDP_Current', 'GDP_Constant', 'Deflator', 'RD_Current', 'RD_Constant', 
                   'Total', 'Business', 'Federal', 'Higher_edu', 'Other', 'Business_fund', 'Federal_fund', 'Other_fund']
nsf_data['Year'] = nsf_data['Year'].str.replace('e', '').str.replace('f', '').astype(int)
nsf_data = nsf_data[nsf_data['Year'] >= 2010]
nsf_data['Total'] = pd.to_numeric(nsf_data['Total'], errors='coerce')

# 合并数据
us_data = pd.DataFrame()
us_data['Year'] = nsf_data['Year']
us_data['RD_GDP_Ratio'] = nsf_data['Total']

# 处理AI模型数据
ai_models_us = ai_models[ai_models['地区'] == '美国'].copy()
ai_models_us['年份'] = pd.to_numeric(ai_models_us['年份'], errors='coerce')
ai_models_us['知名AI模型数量'] = pd.to_numeric(ai_models_us['知名AI模型数量'], errors='coerce')

# 处理专利数据
patents_us = patents[patents['地区'] == '美国'].copy()
patents_us['年份'] = pd.to_numeric(patents_us['年份'], errors='coerce')
patents_us['AI专利占比(占全球总数百分比)'] = pd.to_numeric(patents_us['AI专利占比(占全球总数百分比)'], errors='coerce')

# 合并数据
us_data = us_data.merge(ai_models_us[['年份', '知名AI模型数量']], 
                       left_on='Year', right_on='年份', how='left')
us_data = us_data.merge(patents_us[['年份', 'AI专利占比(占全球总数百分比)']], 
                       left_on='Year', right_on='年份', how='left')

us_data = us_data.rename(columns={
    'RD_GDP_Ratio': 'R&D投入占GDP比例',
    '知名AI模型数量': 'AI模型数量',
    'AI专利占比(占全球总数百分比)': 'AI专利占比'
})

# 删除重复的年份列并处理缺失值
us_data = us_data.drop(['年份_x', '年份_y'], axis=1, errors='ignore')
us_data = us_data.dropna()

# 打印数据概览
print("数据概览：")
print(us_data)

# 斯皮尔曼相关性分析
correlation_matrix = us_data[['R&D投入占GDP比例', 'AI模型数量', 'AI专利占比']].corr(method='spearman')

# 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('美国科技创新指标斯皮尔曼相关性热力图')
plt.tight_layout()
plt.show()
plt.close()

# ARIMA时间序列预测
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
plt.figure(figsize=(15, 10))
for column in ['R&D投入占GDP比例', 'AI模型数量', 'AI专利占比']:
    plt.plot(us_data['Year'], us_data[column], marker='o', label=f'{column}实际值')
    plt.plot(predictions['Year'], predictions[f'{column}_预测'], 
             linestyle='--', marker='s', label=f'{column}预测值')

plt.title('美国科技创新指标时间序列预测')
plt.xlabel('年份')
plt.ylabel('指标值')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
plt.close()

# 输出分析结果
print("\n相关性分析结果：")
print(correlation_matrix)
print("\n未来三年预测结果：")
print(predictions)

# 计算并输出详细的相关性分析结果
print("\n详细的相关性分析：")
for var1 in ['R&D投入占GDP比例', 'AI模型数量', 'AI专利占比']:
    for var2 in ['R&D投入占GDP比例', 'AI模型数量', 'AI专利占比']:
        if var1 != var2:
            correlation, p_value = stats.spearmanr(us_data[var1], us_data[var2])
            print(f"{var1} 与 {var2} 的斯皮尔曼相关系数: {correlation:.3f}")
            print(f"p值: {p_value:.3f}") 
print(predictions) 