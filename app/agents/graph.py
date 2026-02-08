from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from app.agents.tools import query_expenses_db
from app.agents.middlewares import pii_middleware

# 定义 llm
# 因为金钱数据敏感, 使用本地部署
llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)

# 绑定工具
tools = [query_expenses_db]
middlewares = [pii_middleware]
llm_with_tools = llm.bind_tools(tools)

system_prompt = """
你是一个专业的财务分析助手。你可以访问本地 SQLite 数据库中的 'transaction' 表。

表结构:
- transaction_date (DATETIME): 交易时间
- amount (FLOAT): 交易金额 (负数=支出, 正数=收入)
- raw_description (TEXT): 交易描述
- currency (TEXT): 币种

规则:
1. 必须优先使用 query_expenses_db 工具查询数据库，禁止猜测。
2. 这是一个 SQLite 数据库。
"""

# 定义 agent
finance_agent = create_agent(
    model=llm,
    tools=tools,
    middleware=middlewares,
    system_prompt=system_prompt
)