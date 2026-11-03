from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.app.database.session import get_db
from backend.app.schemas.scan import ScanCreate, ScanResponse
from backend.app.services.scan_service import ScanService
from backend.app.models.all_models import Scan

router = APIRouter(prefix="/scans", tags=["scans"])

@router.post("/", response_model=ScanResponse, status_code=201)
async def create_scan(payload: ScanCreate, db: AsyncSession = Depends(get_db)):
    service = ScanService(db)
    return await service.start_scan(payload)

@router.get("/", response_model=List[ScanResponse])
async def list_scans(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(Scan))
    return result.scalars().all()
