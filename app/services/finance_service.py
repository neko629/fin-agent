import pandas as pd
import io
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction

class FinanceService:
    async def process_file_upload(self, file_content: bytes, filename: str, session: AsyncSession):
        """处理上传的CSV文件，解析交易数据并存入数据库"""
        try:
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                # engine='openpyxl' 是读取 Excel 的标准引擎
                df = pd.read_excel(io.BytesIO(file_content))
            else:
                # CSV 读取：先全部按字符串读进来，避免 Pandas 瞎猜导致错乱
                try:
                    df = pd.read_csv(io.BytesIO(file_content), encoding='utf-8',
                                     dtype=str)
                except UnicodeDecodeError:
                    df = pd.read_csv(io.BytesIO(file_content), encoding='gbk', dtype=str)
        except Exception as e:
            raise ValueError(f"文件读取失败: {str(e)}")

        column_map = {
            "交易时间": "transaction_date",
            "商品说明": "raw_description",
            "金额": "amount",
            "备注": "tags"
        }

        df = df.rename(
            columns=lambda x: next((v for k, v in column_map.items() if k in x), x))

        if df['amount'].dtype == 'object':
            df['amount'] = df['amount'].astype(str).str.replace('¥', '').str.replace(',','').astype(float)
        print(df['transaction_date'])
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])

        df['raw_description'] = df['raw_description'].fillna("Unknown")
        df['source_file'] = filename

        transactions = []

        for _, row in df.iterrows():
            txn = Transaction(
                transaction_date = row['transaction_date'],
                amount=row['amount'],
                raw_description=row['raw_description'],
                source_file=filename,
                currency='CNY'
            )
            transactions.append(txn)

        session.add_all(transactions)
        await session.commit()

        return {"total_processed": len(transactions), "file": filename}


