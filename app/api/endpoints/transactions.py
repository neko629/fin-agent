from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.finance_service import FinanceService

router = APIRouter()
finance_service = FinanceService()

@router.post("/upload")
async def upload_transactions(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    """上传CSV文件并处理交易数据"""
    if not (file.filename.endswith('csv') or file.filename.endswith('xlsx') or file.filename.endswith('xls')):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()
    try:
        result = await finance_service.process_file_upload(content, file.filename, session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))