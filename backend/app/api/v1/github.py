from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.integrations.github.client import GitHubClient
from backend.app.repositories.github_project import GitHubProjectRepository

router = APIRouter(prefix="/github", tags=["github"])

@router.get("/repos")
async def list_github_repos(token: str, organization: str = None, db: AsyncSession = Depends(get_db)):
    client = GitHubClient(token)
    return await client.list_repositories(organization)

@router.post("/sync")
async def sync_repo(owner: str, repo: str, token: str, db: AsyncSession = Depends(get_db)):
    repo_service = GitHubProjectRepository(db)
    project = await repo_service.sync_github_repo(owner, repo)
    return {"project_id": project.id, "name": project.name}
