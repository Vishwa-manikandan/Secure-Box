import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import async_session_factory
from backend.app.services.scan_service import ScanService
from backend.app.schemas.scan import ScanCreate
from backend.app.repositories.project import ProjectRepository

@pytest.mark.asyncio
async def test_full_scan_lifecycle():
    async with async_session_factory() as session:
        # 1. Setup Project
        proj_repo = ProjectRepository(session)
        project = await proj_repo.create(ProjectCreate(
            name="Test Repo", 
            source_type="local", 
            repository_path="."
        ))
        
        # 2. Start Scan
        scan_service = ScanService(session)
        scan = await scan_service.start_scan(ScanCreate(
            project_id=project.id, 
            scan_type="repository_full"
        ))
        
        assert scan.status == "running"
        # In a real test, we would wait for the background task or use a synchronous runner
        assert scan.project_id == project.id
