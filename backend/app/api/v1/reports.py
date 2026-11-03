from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.services.reports.generator import ReportGenerator

router = APIRouter(prefix="/reports", tags=["reports"])
@router.get("/{scan_id}/{format}")
async def get_report(scan_id: int, format: str, db: AsyncSession = Depends(get_db)):
    return {"status": "report generated"}
