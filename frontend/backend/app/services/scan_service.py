import asyncio
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models.all_models import Scan, ScanStatus, Finding, FindingStatus, Project
from backend.app.schemas.scan import ScanCreate
from backend.app.services.scanner.orchestrator import RepoScanner

logger = logging.getLogger("securebox.scan_service")

class ScanService:
    """Orchestrates the scanning lifecycle, integrating the RepoScanner."""
    
    def __init__(self, db: AsyncSession, api_key: str = None):
        self.db = db
        self.api_key = api_key

    async def start_scan(self, scan_data: ScanCreate) -> Scan:
        # 1. Create Scan record
        project_result = await self.db.execute(select(Project).where(Project.id == scan_data.project_id))
        project_obj = project_result.scalar_one()
        
        new_scan = Scan(
            project_id=scan_data.project_id,
            scan_type="repository_full",
            status=ScanStatus.RUNNING,
            started_at=datetime.now(),
            summary="Scan initialized..."
        )
        self.db.add(new_scan)
        await self.db.commit()
        await self.db.refresh(new_scan)
        
        # 2. Run scan in background
        asyncio.create_task(self._execute_scan(new_scan.id, project_obj.repository_path))
        
        return new_scan

    async def _execute_scan(self, scan_id: int, repo_path: str):
        try:
            scanner = RepoScanner(repo_path, api_key=self.api_key)
            result = await scanner.run_full_scan()
            
            # In a background task, we need a new session
            # (Simplification: in production use a session factory)
            async with self.db.begin():
                scan_result = await self.db.execute(select(Scan).where(Scan.id == scan_id))
                scan_obj = scan_result.scalar_one()
                
                scan_obj.status = ScanStatus.COMPLETED
                scan_obj.completed_at = datetime.now()
                scan_obj.coverage = result["coverage"]["coverage_percent"] / 100.0
                scan_obj.summary = f"Analyzed {result['coverage']['files_analyzed']} files using {', '.join(result['engines'])}."
                
                # Save findings
                for f_data in result["findings"]:
                    finding = Finding(
                        scan_id=scan_id,
                        **f_data
                    )
                    self.db.add(finding)
                
                await self.db.commit()
                
        except Exception as e:
            logger.error(f"Background scan failed for scan_id {scan_id}: {str(e)}", exc_info=True)
            # Update status to failed
            async with self.db.begin():
                scan_result = await self.db.execute(select(Scan).where(Scan.id == scan_id))
                scan_obj = scan_result.scalar_one()
                scan_obj.status = ScanStatus.FAILED
                scan_obj.summary = f"Scan failed: {str(e)}"
                await self.db.commit()
