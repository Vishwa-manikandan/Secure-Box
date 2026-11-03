from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Dict, Any
from backend.app.models.all_models import Scan, Finding

class HistoryService:
    """Handles historical security intelligence and trend analysis."""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_project_trends(self, project_id: int) -> Dict[str, Any]:
        """Analyze security trends over multiple scans for a project."""
        result = await self.db.execute(
            select(Scan)
            .where(Scan.project_id == project_id)
            .order_by(Scan.created_at.asc())
        )
        scans = result.scalars().all()
        
        if not scans:
            return {"trend": "stable", "data": []}
            
        history = []
        for scan in scans:
            # Count findings for this scan
            findings_res = await self.db.execute(
                select(func.count(Finding.id)).where(Finding.scan_id == scan.id)
            )
            count = findings_res.scalar()
            history.append({"date": scan.created_at, "count": count})
            
        return {
            "project_id": project_id,
            "scan_count": len(scans),
            "trend_data": history,
            "current_status": "improving" if history[-1]["count"] < history[0]["count"] else "declining"
        }

    async def compare_scans(self, scan_id_1: int, scan_id_2: int) -> Dict[str, Any]:
        """Compare two scans to detect regressions and resolutions."""
        # Get findings for both scans
        res1 = await self.db.execute(select(Finding).where(Finding.scan_id == scan_id_1))
        f1 = {f"{f.file_path}:{f.line_number}:{f.rule_id}" for f in res1.scalars().all()}
        
        res2 = await self.db.execute(select(Finding).where(Finding.scan_id == scan_id_2))
        f2 = {f"{f.file_path}:{f.line_number}:{f.rule_id}" for f in res2.scalars().all()}
        
        return {
            "resolved": list(f1 - f2),
            "new": list(f2 - f1),
            "persisted": list(f1 & f2)
        }
