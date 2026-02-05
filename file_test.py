import asyncio

from app.core.db import engine
from app.core.db import init_db
from app.services.finance_service import FinanceService
import pandas as pd
import io
from sqlalchemy.ext.asyncio import AsyncSession

async def main():
    file_path = '/mnt/c/Users/neko/Documents/tesbill.csv'

    # 读取文件内容转为 bytes
    with open(file_path, 'rb') as f:
        file_content = f.read()

    finance_service = FinanceService()
    async with AsyncSession(engine) as session:
        await init_db()
        await finance_service.process_file_upload(file_content, "tesbill.csv", session=session)

# 运行异步函数
asyncio.run(main())