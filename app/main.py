from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.db import init_db
from app.core.config import settings
from app.api.endpoints import transactions, chat

#生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("System Starting... Initializing Database...")
    await init_db()
    yield
    print("System Shutting Down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
@app.get("/")
async def root():
    return {
        "message": "FinAgent Core is running",
        "tech_stack": "FastAPI + SQLModel + AsyncIO"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)