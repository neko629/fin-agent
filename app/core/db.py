from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 创建异步数据库引擎, echo 参数用于打印SQL日志, future=True启用SQLAlchemy 2.0行为
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# 创建异步会话工厂
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """
    初始化数据库连接和创建表
    """
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    """Dependency Injection 用于 FastAPI"""
    async with async_session() as session:
        yield session
