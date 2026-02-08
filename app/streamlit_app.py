# ui.py
import streamlit as st
import requests
import pandas as pd

# 后端 API 地址
API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(page_title="FinAgent - 智能财务", layout="wide")

st.title("🤖 FinAgent: 你的私人财务分析师")

# --- 侧边栏: 数据上传 ---
with st.sidebar:
    st.header("📂 账单导入")
    uploaded_file = st.file_uploader("上传支付宝/微信账单 (CSV/Excel)",
                                     type=["csv", "xlsx"])

    if uploaded_file is not None:
        if st.button("开始分析"):
            with st.spinner("正在清洗并入库数据..."):
                try:
                    # 构造 multipart/form-data 请求
                    files = {
                        "file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(f"{API_BASE_URL}/transactions/upload",
                                             files=files)

                    if response.status_code == 200:
                        res_json = response.json()
                        st.success(
                            f"✅ 成功导入 {res_json.get('total_processed')} 条交易记录！")
                    else:
                        st.error(f"❌ 导入失败: {response.text}")
                except Exception as e:
                    st.error(f"系统错误: {e}")

    st.divider()
    st.markdown("### 💡 提示词示例")
    st.markdown("- *上个月我主要把钱花哪了？*")
    st.markdown("- *统计一下星巴克的总消费*")
    st.markdown("- *我有多少笔超过 500 元的大额支出？*")

# --- 主界面: 聊天对话 ---

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入
if prompt := st.chat_input("问我任何关于你财务状况的问题..."):
    # 1. 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 调用后端 API
    with st.chat_message("assistant"):
        with st.spinner("思考中 (正在查询数据库)..."):
            try:
                # 调用我们在 Step 1 写的 Chat API
                api_res = requests.post(
                    f"{API_BASE_URL}/chat/",
                    json={"message": prompt}
                )

                if api_res.status_code == 200:
                    ai_response = api_res.json()["response"]
                    st.markdown(ai_response)
                    # 存入历史
                    st.session_state.messages.append(
                        {"role": "assistant", "content": ai_response})
                else:
                    st.error(f"API Error: {api_res.text}")

            except Exception as e:
                st.error(f"Connection Error: {e}")