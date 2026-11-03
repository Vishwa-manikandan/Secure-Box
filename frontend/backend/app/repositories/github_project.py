from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.models.all_models import Project
from backend.app.schemas.project import ProjectCreate

class GitHubProjectRepository:
    """Specialized repository for managing GitHub-synced projects."""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def sync_github_repo(self, owner: str, repo_name: str, branch: str = "main") -> Project:
        # Check if project already exists
        result = await self.session.execute(
            select(Project).where(Project.repository_path == f"https://github.com/{owner}/{repo_name}")
        )
        project = result.scalar_one_or_none()
        
        if not project:
            # Create new project
            project = Project(
                name=repo_name,
                source_type="github",
                repository_path=f"https://github.com/{owner}/{repo_name}"
            )
            self.session.add(project)
            await self.session.commit()
            await self.session.refresh(project)
            
        return project
