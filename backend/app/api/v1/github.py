from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.integrations.github.client import GitHubClient

router = APIRouter(prefix="/github", tags=["github"])
@router.get("/repos")
async def list_repos(token: str, db: AsyncSession = Depends(get_db)):
    return await GitHubClient(token).list_repositories()
