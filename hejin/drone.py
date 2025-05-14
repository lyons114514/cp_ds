# %% [markdown]
# # 中国无人机产业领导力与AI赋能分析 (Jupyter Notebook - Matplotlib/Seaborn 版本)
#
# 本 Notebook 分析了中国无人机产业的市场格局、AI 技术渗透、应用拓展及产业链优势。此版本使用 Matplotlib 和 Seaborn 进行可视化。
#
# ## 1. 导入库与准备

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# --- 配置 ---
# 设置绘图风格和中文字体
try:
    sns.set_theme(style="whitegrid") # 尝试新版 Seaborn API
except AttributeError:
    sns.set_style("whitegrid") # 使用旧版 API 作为备选

try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
    plt.rcParams['axes.unicode_minus'] = False
except Exception as e:
    print(f"设置中文字体失败: {e}. 中文可能无法正常显示。")

# %% [markdown]
# ## 2. 数据加载

# %%
def load_drone_data(file_path='data/drone_data.csv'):
    """加载无人机数据，以年份为索引。"""
    data_file = Path(file_path)
    if not data_file.exists():
        print(f"错误：找不到数据文件 - {data_file}")
        return None
    try:
        try:
            data = pd.read_csv(data_file, index_col='Year', encoding='utf-8')
        except UnicodeDecodeError:
            data = pd.read_csv(data_file, index_col='Year', encoding='gbk')
        print(f"成功从 '{data_file}' 加载数据。")
        data.index = pd.to_numeric(data.index, errors='coerce')
        data = data.dropna(axis=0, how='all')
        data = data[data.index.notna()]
        data.index = data.index.astype(int)
        data = data.sort_index()
        print("数据信息:\n", data.info())
        # 将所有列尝试转为数值，非数值转为 NaN
        for col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        return data
    except Exception as e:
        print(f"加载数据时出错: {e}")
        return None

# 加载数据
df = load_drone_data()

if df is None:
    print("数据加载失败，无法继续分析。")
else:
    latest_year = df.index.max()
    latest_data = df.loc[latest_year]
    print(f"\n最新数据年份: {latest_year}")
    print("最新年份数据概览:\n", latest_data)

# %% [markdown]
# ## 3. 关键指标展示

# %%
if df is not None:
    print(f"\n--- 关键指标 ({latest_year}年) ---")
    print(f"- 中国无人机全球市场份额 (估计): {latest_data.get('DJI_Share_Total', 'N/A'):.1f}%")
    print(f"- 全球无人机市场规模: ${latest_data.get('Global_Market_Total', 'N/A'):.1f} B")
    print(f"- AI技术在无人机中渗透率: {latest_data.get('AI_Adoption_Rate', 'N/A'):.1f}%")
    print(f"- AI驱动的主要新兴应用领域数量: >5")

# %% [markdown]
# ---
# ## 4. 市场格局与领导力分析

# %% [markdown]
# ### 全球无人机市场增长趋势

# %%
if df is not None:
    plt.figure(figsize=(10, 6))
    # 使用 Matplotlib 的 stackplot 绘制堆叠面积图
    plt.stackplot(df.index, df['Global_Market_Consumer'].fillna(0), df['Global_Market_Industrial'].fillna(0),
                  labels=['消费级市场', '行业级市场'],
                  alpha=0.7, colors=sns.color_palette("pastel", 2))
    plt.plot(df.index, df['Global_Market_Consumer'], marker='.', label='_nolegend_', color=sns.color_palette("pastel", 2)[0]) # 添加标记点
    plt.plot(df.index, df['Global_Market_Industrial'], marker='.', label='_nolegend_', color=sns.color_palette("pastel", 2)[1]) # 添加标记点

    plt.title("全球无人机市场规模 (消费级 vs 行业级, 十亿美元)")
    plt.xlabel("年份")
    plt.ylabel("市场规模 (十亿美元)")
    plt.legend(loc='upper left')
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# %% [markdown]
# *   **行业级市场**成为增长主要驱动力，年复合增长率超过 **30%**。
# *   消费级市场趋于稳定，但仍保持一定规模。

# %% [markdown]
# ### 中国无人机市场份额主导地位

# %%
if df is not None:
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['DJI_Share_Consumer'], marker='o', linestyle='-', label='消费级市场份额')
    plt.plot(df.index, df['DJI_Share_Industrial'], marker='s', linestyle='-', label='行业级市场份额')
    plt.plot(df.index, df['DJI_Share_Total'], marker='^', linestyle='--', label='整体市场份额', color='red')

    plt.title("中国(以大疆为代表)在全球无人机市场份额 (%)")
    plt.xlabel("年份")
    plt.ylabel("市场份额 (%)")
    plt.ylim(40, 90) # 根据数据调整范围
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# %% [markdown]
# *   中国企业在**消费级市场**占据绝对优势，份额稳定在 **{latest_data.get('DJI_Share_Consumer', 'N/A'):.1f}%** 左右。
# *   在**行业级市场**，尽管竞争加剧，中国企业凭借技术和成本优势，仍保持 **{latest_data.get('DJI_Share_Industrial', 'N/A'):.1f}%** 以上的主导地位。
# *   整体市场份额维持在 **{latest_data.get('DJI_Share_Total', 'N/A'):.1f}%** 以上，显示出强大的综合竞争力。

# %% [markdown]
# ---
# ## 5. AI赋能与应用拓展分析

# %% [markdown]
# ### AI技术在无人机领域的渗透加速

# %%
if df is not None and 'AI_Adoption_Rate' in df.columns:
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['AI_Adoption_Rate'], marker='o', linestyle='-')
    plt.title("AI技术在无人机中的渗透率 (%)")
    plt.xlabel("年份")
    plt.ylabel("渗透率 (%)")
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
else:
    print("警告：缺少 'AI_Adoption_Rate' 数据列。")

# %% [markdown]
# *   AI技术（计算机视觉、自主导航、路径规划、智能避障等）渗透率从 {df.index.min() if df is not None else 'N/A'} 年的约 **{df['AI_Adoption_Rate'].iloc[0]:.1f if df is not None and 'AI_Adoption_Rate' in df.columns else 'N/A'}%** 快速增长至 {latest_year if df is not None else 'N/A'} 年的 **{latest_data.get('AI_Adoption_Rate', 'N/A'):.1f}%**。
# *   AI是推动无人机从简单航拍工具向智能化作业平台转变的核心动力。

# %% [markdown]
# ### AI驱动的应用领域市场增长

# %%
if df is not None:
    app_cols = ['App_Market_Agriculture', 'App_Market_Surveying', 'App_Market_Security', 'App_Market_Logistics', 'App_Market_Filming']
    app_cols_exist = [col for col in app_cols if col in df.columns]

    if app_cols_exist:
        app_labels_map = {'App_Market_Agriculture': '精准农业', 'App_Market_Surveying': '测绘勘探',
                          'App_Market_Security': '安防巡逻', 'App_Market_Logistics': '物流配送', 'App_Market_Filming': '影视航拍'}
        plot_labels = [app_labels_map.get(col, col) for col in app_cols_exist]

        plt.figure(figsize=(12, 7))
        # 使用 fill_between 模拟面积图效果或直接用 plot
        # 为了简单起见，这里用普通折线图
        for i, col in enumerate(app_cols_exist):
             plt.plot(df.index, df[col], marker='.', label=plot_labels[i])

        # 或者用堆叠面积图
        # plt.stackplot(df.index, [df[col].fillna(0) for col in app_cols_exist], labels=plot_labels, alpha=0.7)

        plt.title("主要AI赋能应用领域市场规模 (十亿美元)")
        plt.xlabel("年份")
        plt.ylabel("市场规模 (十亿美元)")
        plt.legend(loc='upper left')
        plt.grid(True, axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()
    else:
        print("警告：缺少部分或全部应用领域市场数据列，无法绘制图表。")

# %% [markdown]
# *   **精准农业**: 市场规模预计达到 **${latest_data.get('App_Market_Agriculture', 'N/A'):.1f} B**，AI实现变量喷洒、作物监测等。
# *   **测绘勘探**: 市场规模预计达到 **${latest_data.get('App_Market_Surveying', 'N/A'):.1f} B**，AI提升数据处理和建模效率。
# *   **安防巡逻**: 市场规模预计达到 **${latest_data.get('App_Market_Security', 'N/A'):.1f} B**，AI实现自主巡逻、异常识别。
# *   **物流配送**: 市场潜力巨大，预计达到 **${latest_data.get('App_Market_Logistics', 'N/A'):.1f} B**，AI解决"最后一公里"配送难题。
# *   **影视航拍**: 市场规模 **${latest_data.get('App_Market_Filming', 'N/A'):.1f} B**，AI带来更智能的跟随拍摄、轨迹规划。

# %% [markdown]
# ### AI赋能的量化效益提升

# %%
if df is not None:
    print("\n--- AI 赋能效益可视化 ---")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10)) # 创建 2x2 子图网格
    axes = axes.flatten() # 展平以便索引

    # 1. 精准农业
    agri_cols = ['Agri_Pesticide_Reduction', 'Agri_Yield_Increase']
    if all(col in df.columns for col in agri_cols):
        ax = axes[0]
        ax.plot(df.index, df['Agri_Pesticide_Reduction'], marker='.', label='农药减施率')
        ax.plot(df.index, df['Agri_Yield_Increase'], marker='.', label='产量提升率')
        ax.set_title("精准农业效益 (%)")
        ax.set_xlabel("年份")
        ax.set_ylabel("百分比 (%)")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        print(f"* 精准农业: 农药减施率可达 {latest_data.get('Agri_Pesticide_Reduction', 'N/A'):.1f}%，产量提升率可达 {latest_data.get('Agri_Yield_Increase', 'N/A'):.1f}%。")
    else:
        axes[0].set_title("精准农业效益 (数据缺失)")
        axes[0].text(0.5, 0.5, '数据缺失', ha='center', va='center', fontsize=12, alpha=0.5)
        print("警告: 缺少精准农业效益数据列。")

    # 2. 测绘勘探
    survey_col = 'Survey_Time_Reduction'
    if survey_col in df.columns:
        ax = axes[1]
        ax.plot(df.index, df[survey_col], marker='.')
        ax.set_title("测绘勘探效益: 作业时间缩短率 (%)")
        ax.set_xlabel("年份")
        ax.set_ylabel("时间缩短率 (%)")
        ax.grid(True, linestyle='--', alpha=0.6)
        print(f"* 测绘勘探: 作业时间缩短率 {latest_data.get(survey_col, 'N/A'):.1f}%。")
    else:
        axes[1].set_title("测绘勘探效益 (数据缺失)")
        axes[1].text(0.5, 0.5, '数据缺失', ha='center', va='center', fontsize=12, alpha=0.5)
        print("警告: 缺少测绘勘探效益数据列。")

    # 3. 安防巡逻
    security_col = 'Security_Cost_Saving'
    if security_col in df.columns:
        ax = axes[2]
        ax.plot(df.index, df[security_col], marker='.')
        ax.set_title("安防巡逻效益: 人力成本节约率 (%)")
        ax.set_xlabel("年份")
        ax.set_ylabel("成本节约率 (%)")
        ax.grid(True, linestyle='--', alpha=0.6)
        print(f"* 安防巡逻: 人力成本节约率高达 {latest_data.get(security_col, 'N/A'):.1f}%。")
    else:
        axes[2].set_title("安防巡逻效益 (数据缺失)")
        axes[2].text(0.5, 0.5, '数据缺失', ha='center', va='center', fontsize=12, alpha=0.5)
        print("警告: 缺少安防巡逻效益数据列。")

    # 4. 物流配送
    logistics_col = 'Logistics_Cost_Reduction'
    if logistics_col in df.columns:
        ax = axes[3]
        ax.plot(df.index, df[logistics_col], marker='.')
        ax.set_title("物流配送效益: 单次成本降低率 (%)")
        ax.set_xlabel("年份")
        ax.set_ylabel("成本降低率 (%)")
        ax.grid(True, linestyle='--', alpha=0.6)
        print(f"* 物流配送: 单次成本降低率 {latest_data.get(logistics_col, 'N/A'):.1f}%。")
    else:
        axes[3].set_title("物流配送效益 (数据缺失)")
        axes[3].text(0.5, 0.5, '数据缺失', ha='center', va='center', fontsize=12, alpha=0.5)
        print("警告: 缺少物流配送效益数据列。")

    plt.tight_layout()
    plt.show()

# %% [markdown]
# ---
# ## 6. 产业链优势分析

# %% [markdown]
# ### 中国无人机完整产业链布局
#
# (文字描述，省略图片)
#
# 中国无人机产业形成了从**核心零部件**到**整机制造**再到**软件算法**和**应用服务**的完整闭环。
#
# **核心优势环节：**
#
# 1.  **硬件制造与集成:** 规模化、低成本生产能力；核心部件自研/国产化。
# 2.  **飞控与导航算法:** 稳定可靠的飞控系统；高精度定位；自主飞行能力。
# 3.  **AI视觉技术:** 目标识别与跟踪；环境感知与三维重建；图像分析与处理。
# 4.  **应用软件与平台:** 易用的操控软件；行业解决方案；云服务与数据管理。
#
# **产业链协同效应：** 快速响应、技术迭代、生态丰富、成本优势。

# %% [markdown]
# ---
# ## 7. 结论与展望

# %% [markdown]
# ### 核心结论

# %%
if df is not None:
    print("\n--- 核心结论 ---")
    print(f"1. 市场领导地位稳固: 中国在全球无人机市场占据 {latest_data.get('DJI_Share_Total', 'N/A'):.1f}% 以上的主导份额。")
    print(f"2. AI是核心驱动力: AI技术渗透率快速提升至 {latest_data.get('AI_Adoption_Rate', 'N/A'):.1f}%，赋能智能化应用。")
    print(f"3. 全产业链优势: 拥有从硬件、算法到服务的完整产业链，形成技术和成本优势 (例如，精准农业农药减施 {latest_data.get('Agri_Pesticide_Reduction', 'N/A'):.1f}%)。")
    print("4. 应用场景持续拓展: 从传统航拍拓展到物流、应急等复杂自主作业场景。")

# %% [markdown]
# ### 未来展望
# *   **智能化水平持续提升:** 更高级别的自主飞行、感知与决策。
# *   **行业应用深度融合:** 无人机成为各行业数字化转型工具。
# *   **空域管理与法规完善:** 智能空域管理与法规体系将更重要。
# *   **集群作业与协同:** AI驱动的无人机集群技术应用更广泛。
# *   **与其他技术融合:** 与5G、物联网、云计算等进一步融合。

# %%
print("\n分析完成。")