from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.database.session import get_db
from backend.app.models.all_models import Scan, Finding
from backend.app.services.reports.generator import ReportGenerator

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/{scan_id}/{format}")
async def download_report(scan_id: int, format: str, db: AsyncSession = Depends(get_//_db)):
    res = await db.execute(select(Scan).where(Scan.id == scan_id))
    scan = res.scalar_one_or_none()
    if not scan: raise HTTPException(status_code=404, detail="Scan not found")
    f_res = await db.execute(select(Finding).where(Finding.scan_id == scan_id))
    findings = f_res.scalars().all()
    generator = ReportGenerator(scan, findings)
    if format == "json": content = generator.to_json(); media_type = "application/json"
    elif format == "md": content = generator.to_markdown(); media_type = "text/markdown"
    elif format == "sarif": content = generator.to_sarif(); media_type = "application/sarif+json"
    else: raise HTTPException(status_code=400, detail="Unsupported format")
    return Response(content=content, media_type=media_type)
