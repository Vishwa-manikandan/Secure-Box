from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.schemas.scan import ScanCreate, ScanResponse
from backend.app.services.scan_service import ScanService

router = APIRouter(prefix="/scans", tags=["scans"])
@router.post("/", response_model=ScanResponse)
async def create_scan(payload: ScanCreate, db: AsyncSession = Depends(get_db)):
    return await ScanService(db).start_scan(payload)
