from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.models.all_models import Project
from backend.app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def create(self, data: ProjectCreate) -> Project:
        project = Project(**data.model_dump())
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project
    async def get(self, id: int) -> Project | None:
        result = await self.session.execute(select(Project).where(Project.id == id))
        return result.scalar_one_or_none()
    async def list(self, limit: int = 100, offset: int = 0):
        result = await self.session.execute(select(Project).offset(offset).limit(limit))
        return result.scalars().all()
    async def update(self, id: int, data: ProjectUpdate) -> Project | None:
        project = await self.get(id)
        if not project: return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items(): setattr(project, key, value)
        await self.session.commit()
        await self.session.refresh(project)
        return project
    async def delete(self, id: int) -> bool:
        project = await self.get(id)
        if not project: return False
        self.session.delete(project)
        await self.session.commit()
        return True
