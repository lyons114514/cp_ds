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
        font-size: 1.3rem; /* Increased header size */
        color: #2196F3;
        margin-bottom: 1.5rem; /* Increased bottom margin */
        font-weight: bold;
        padding-top: 1rem; /* Added padding top */
    }
    .category-title {
        font-size: 1.1rem;
        color: #1976D2;
        margin-top: 1.2rem; /* Increased top margin */
        margin-bottom: 0.6rem; /* Increased bottom margin */
        font-weight: bold;
    }
    /* Style buttons for a cleaner look */
    .stButton>button {
        border: none;
        background-color: transparent;
        text-align: left;
        padding: 0.5rem 0; /* Adjust vertical padding */
        width: 100%;
        font-size: 1rem; /* Slightly larger font for items */
        color: #333; /* Darker text color */
    }
    .stButton>button:hover {
        background-color: #f0f2f6; /* Light hover effect */
        color: #1976D2;
    }
    .stButton>button:focus {
        outline: none !important;
        box-shadow: none !important;
        color: #0D47A1; /* Darker blue on click/focus */
        background-color: #e3f2fd; /* Lighter blue background on click/focus */
    }
    /* Ensure sidebar content has some padding */
    .st-emotion-cache-10oheav {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 页面映射配置
MENU_STRUCTURE = {
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

# 初始化session state，默认打开 GPU 模块
if 'current_module' not in st.session_state:
    st.session_state.current_module = "gpu"

# 在侧边栏添加标题
st.sidebar.markdown("<div class='sidebar-header'>AI应用分析平台</div>", unsafe_allow_html=True)

def handle_page_selection(category, page, module):
    st.session_state.current_category = category
    st.session_state.current_page = page
    st.session_state.current_module = module

# 直接列出所有页面按钮
for category, content in MENU_STRUCTURE.items():
    if content["items"]:
        for page, module_name in content["items"].items():
            st.sidebar.button(
                page, 
                key=f"btn_{category}_{page}", 
                on_click=handle_page_selection, 
                args=(category, page, module_name)
            )

    # 加载选中的模块
    if st.session_state.current_module:
        try:
            st.session_state.is_sub_module = True
            if st.session_state.current_module not in sys.modules:
                module = importlib.import_module(st.session_state.current_module)
            else:
                module = sys.modules[st.session_state.current_module]
                importlib.reload(module)
            if hasattr(module, 'main'):
                module.main()
        except Exception as e:
            st.error(f"加载模块 {st.session_state.current_module} 时发生错误: {str(e)}") 