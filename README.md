# 🤖 FinAgent: 隐私优先的 AI 个人财务助理

FinAgent 是一个基于本地大语言模型（LLM）的智能财务分析系统。它能够安全地处理你的账单数据，通过自然语言对话帮你洞察消费习惯，同时确保所有敏感数据不出本地环境。

## 🌟 核心特性

-   **隐私至上**：集成本地 Ollama (Qwen 2.5:7b) 模型，财务数据完全本地化处理。
-   **智能查询**：利用 AI 自动生成 SQL 语句查询 SQLite 数据库，精准回答各类财务问题。
-   **一键导入**：支持支付宝、微信等账单（CSV/Excel）的快速清洗与入库。
-   **直观 UI**：提供基于 Streamlit 的友好交互界面，支持实时聊天和数据看板。
-   **PII 保护**：内置中间件识别并脱敏个人隐私信息。

## 🛠️ 技术栈

-   **语言/框架**：Python 3.13+, FastAPI
-   **大模型框架**：LangChain, LangGraph, Ollama
-   **数据库**：SQLModel (SQLite) + aiosqlite (异步支持)
-   **前端界面**：Streamlit
-   **包管理**：Poetry
-   **容器化**：Docker & Docker Compose

## 🚀 快速开始

### 1. 环境准备

确保已安装以下软件：
- [Ollama](https://ollama.com/)
- Python 3.13+
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker (可选)

### 2. 配置 Ollama

下载并运行 Qwen 模型：
```bash
ollama pull qwen2.5:7b
ollama serve
```

### 3. 安装依赖

```bash
# 克隆项目
git clone https://github.com/your-repo/fin-agent.git
cd fin-agent

# 安装依赖
poetry install
```

### 4. 运行项目

#### 方式一：直接运行 (推荐开发环境)

1.  **启动后端 API**:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```
2.  **启动前端 UI**:
    ```bash
    poetry run streamlit run app/streamlit_app.py
    ```

#### 方式二：使用 Docker Compose

```bash
docker-compose up --build
```

> **注意**：如果使用 Docker，请确保 `docker-compose.yml` 中的 `OLLAMA_BASE_URL` 指向宿主机的 Ollama 接口（通常为 `http://host.docker.internal:11434`）。

## 💡 使用示例

导入账单后，你可以这样问它：

-   "上个月我主要把钱花在哪了？"
-   "帮我统计一下所有在星巴克的总消费。"
-   "我有多少笔超过 500 元的大额支出？"
-   "生成一份我本月的消费摘要。"

## 📂 项目结构

```text
fin-agent/
├── app/
│   ├── agents/          # AI 代理逻辑 (LangGraph)
│   ├── api/             # FastAPI 路由与接口
│   ├── core/            # 配置与数据库初始化
│   ├── models/          # 数据模型 (SQLModel)
│   ├── services/        # 业务逻辑 (账单清洗等)
│   ├── main.py          # 后端入口
│   └── streamlit_app.py # 前端界面
├── data/                # SQLite 数据库存放地
├── pyproject.toml       # 项目依赖配置
└── docker-compose.yml   # 容器化部署配置
```

## 📄 开源协议

本项目采用 MIT 协议。
