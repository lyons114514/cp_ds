import streamlit as st
import importlib
import sys
from pathlib import Path

# 设置页面配置
st.set_page_config(
    page_title="AI应用分析平台",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    .sidebar-header {
        font-size: 1.2rem;
        color: #2196F3;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .category-header {
        font-size: 1.1rem;
        color: #1976D2;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .sub-item {
        margin-left: 1rem;
    }
    .stExpander {
        border: none !important;
        box-shadow: none !important;
    }
    .streamlit-expanderHeader {
        font-size: 1.1rem !important;
        color: #1976D2 !important;
        font-weight: bold !important;
        background-color: transparent !important;
        border: none !important;
    }
    .streamlit-expanderContent {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# 页面映射配置
MENU_STRUCTURE = {
    "🏠 首页": {
        "module": None,
        "items": {}
    },
    "🌐 中美AI发展侧重点差异分析": {
        "module": None,
        "items": {
            "💰 投资分析": "us_investment",
            "🎮 GPU产业分析": "gpu",
            "📱 应用分析": "apply",
            "🛒 电商平台分析": "pdd"
        }
    },
    "🏭 中国AI相关重点发展产业分析": {
        "module": None,
        "items": {
            "🚗 自动驾驶分析": "car",
            "🚁 无人机产业分析": "drone",
            "🤖 服务机器人分析": "robot",
            "🏭 智能制造分析": "industry"
        }
    },
    "🏘️ 中国百姓生活与科技创新相关领域分析": {
        "module": None,
        "items": {
            "🍲 食品产业分析": "food",
            "🚦 智慧交通分析": "trafic",
            "🏘️ 智慧住宅分析": "housing"
        }
    }
}

# 初始化session state
if 'current_category' not in st.session_state:
    st.session_state.current_category = "🏠 首页"
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 首页"
if 'current_module' not in st.session_state:
    st.session_state.current_module = None

# 在侧边栏添加标题
st.sidebar.markdown("<div class='sidebar-header'>AI应用分析平台</div>", unsafe_allow_html=True)

def handle_home_selection():
    st.session_state.current_category = "🏠 首页"
    st.session_state.current_page = "🏠 首页"
    st.session_state.current_module = None

def handle_page_selection(category, page, module):
    st.session_state.current_category = category
    st.session_state.current_page = page
    st.session_state.current_module = module

# 首页选项
home_expander = st.sidebar.expander("🏠 首页", expanded=st.session_state.current_category == "🏠 首页")
with home_expander:
    if st.button("返回首页", key="home_button"):
        handle_home_selection()

# 为每个类别创建一个expander
for category, content in list(MENU_STRUCTURE.items())[1:]:  # 跳过首页
    with st.sidebar.expander(category, expanded=st.session_state.current_category == category):
        if content["items"]:
            for page, module in content["items"].items():
                if st.button(page, key=f"btn_{category}_{page}"):
                    handle_page_selection(category, page, module)

# 主页内容
if st.session_state.current_page == "🏠 首页":
    st.markdown("<h1 class='main-header'>欢迎使用AI应用分析平台</h1>", unsafe_allow_html=True)
    st.markdown("""
    ### 平台简介
    本平台整合了多个AI应用领域的分析模块，主要包括以下三大类：
    
    #### 🌐 中美AI发展侧重点差异分析
    - 💰 **投资分析**: 研究AI相关投资趋势
    - 🎮 **GPU产业分析**: 研究AI芯片市场趋势
    - 📱 **应用分析**: 研究AI在各类应用场景的表现
    - 🛒 **电商平台分析**: 分析AI在电商领域的应用
    
    #### 🏭 中国AI相关重点发展产业分析
    - 🚗 **自动驾驶分析**: 分析自动驾驶技术发展
    - 🚁 **无人机产业**: 分析AI在无人机领域的应用与发展
    - 🤖 **服务机器人**: 研究AI驱动的服务机器人发展
    - 🏭 **智能制造**: 探讨AI驱动的工业革新
    
    #### 🏘️ 中国百姓生活与科技创新相关领域分析
    - 🍲 **食品产业**: 探讨AI如何改变食品安全与效率
    - 🚦 **智慧交通**: 分析AI在交通领域的应用
    - 🏘️ **智慧住宅**: 分析AI在智能家居中的应用

    ### 使用说明
    1. 使用左侧边栏选择要查看的分析类别
    2. 在选择类别后，可以进一步选择具体的分析模块
    3. 每个模块都包含详细的数据分析和可视化图表
    4. 所有数据都会定期更新，确保分析的时效性
    
    ### 数据来源
    - 行业研究报告
    - 公开市场数据
    - 专业机构统计
    - 实地调研数据
    
    ### 更新时间
    最近更新：2024年3月
    """)
else:
    # 加载选中的模块
    if st.session_state.current_module:
        try:
            # 设置环境变量，告诉子模块不要设置页面配置
            st.session_state.is_sub_module = True
            
            # 动态导入模块
            if st.session_state.current_module not in sys.modules:
                module = importlib.import_module(st.session_state.current_module)
            else:
                module = sys.modules[st.session_state.current_module]
                importlib.reload(module)
            
            # 清除之前的streamlit元素
            st.empty()
            
            # 运行模块的main函数（如果存在）
            if hasattr(module, 'main'):
                module.main()
                
        except Exception as e:
            st.error(f"加载模块 {st.session_state.current_module} 时发生错误: {str(e)}") 