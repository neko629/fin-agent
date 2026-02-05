from datetime import datetime
from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel

class TransactionBase(SQLModel):
    """基础字段定义"""
    amount: Decimal = Field(default=0.0, max_digits=10, decimal_places=2, description="交易金额")
    currency: str = Field(default="CNY", max_length=3, description="货币类型")
    transaction_date: datetime = Field(description="交易时间")

    # --- 原始数据 (Raw Data) ---
    raw_description: str = Field(index=True,
                                 description="银行账单原始描述，如 '支付宝-饿了么-张三'")
    source_file: Optional[str] = Field(default=None,
                                       description="来源文件，如 '202601_boc.pdf'")

    # --- AI 增强字段 (AI Enrichment) ---
    # 这些字段不是从账单读出来的，而是 AI 分析填入的
    merchant_name: Optional[str] = Field(default=None, index=True,
                                         description="AI提取的商户名，如 'Starbucks'")
    category: Optional[str] = Field(default="Uncategorized", index=True,
                                    description="AI归纳的类别，如 '餐饮/咖啡'")
    tags: Optional[str] = Field(default=None,
                                description="逗号分隔的标签，如 '早餐,通勤,必需品'")

    # 订阅陷阱检测
    is_recurring: bool = Field(default=False, description="是否为周期性扣款")
    sentiment: Optional[str] = Field(default=None,
                                     description="消费情绪：Impulsive(冲动), Necessary(必要)")

class Transaction(TransactionBase, table=True):
    """
    数据库表定义 (Table=True)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class TransactionCreate(TransactionBase):
    """
    用于创建交易的 DTO (Data Transfer Object)
    """
    pass
