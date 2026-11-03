from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from backend.app.database.session import get_db
from backend.app.integrations.github.client import GitHubClient
from backend.app.repositories.github_project import GitHubProjectRepository

router = APIRouter(prefix="/github", tags=["github"])

@router.get("/repos")
async def list_github_repos(
    token: str, 
    organization: str = None, 
    db: AsyncSession = Depends(get_db)
):
    """List repositories available for the provided GitHub token."""
    client = GitHubClient(token)
    repos = await client.list_repositories(organization)
    if not repos:
        raise HTTPException(status_code=401, detail="Invalid token or no repositories found")
    return repos

@router.post("/sync")
async def sync_repo(
    owner: str, 
    repo: str, 
    token: str, 
    db: AsyncSession = Depends(get_db)
):
    """Sync a GitHub repository into Securebox projects."""
    repo_service = GitHubProjectRepository(db)
    project = await repo_service.sync_github_repo(owner, repo)
    return {"project_id": project.id, "name": project.name}

@router.post("/scan-pr")
async def scan_pull_request(
    owner: str, 
    repo: str, 
    pr_number: int, 
    token: str, 
    db: AsyncSession = Depends(get_db)
):
    """Trigger a scan on a specific pull request."""
    # This would integrate with the ScanService implemented previously
    # 1. Fetch PR diff
    # 2. Run scan
    # 3. Post comment
    return {"status": "Scan initiated", "pr": pr_number}
