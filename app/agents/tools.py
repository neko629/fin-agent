from typing import Any
from langchain_core.tools import tool
from sqlalchemy import text

from app.core.db import engine

@tool
def query_expenses_db(sql_query: str) -> str:
    """
        执行 SQL 查询并返回结果。
        仅用于查询 'transaction' 表。
        表结构: transaction(id, transaction_date, amount, raw_description, category, merchant_name)
    """

    if "drop" in sql_query.lower() or "delete" in sql_query.lower() or "update" in sql_query.lower() or "insert" in sql_query.lower():
        return "仅允许执行 SELECT 查询。"

    try:
        from sqlalchemy import create_engine

        sync_url = str(engine.url).replace("+aiosqlite", "")
        sync_engine = create_engine(sync_url)

        with sync_engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()

            if not rows:
                return "查询返回空结果。"
            return str(rows)

    except Exception as e:
        return f"SQL 执行出错: {str(e)}"