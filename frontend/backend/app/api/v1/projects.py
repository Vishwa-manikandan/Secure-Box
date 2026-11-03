from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.app.database.session import get_db
from backend.app.repositories.project import ProjectRepository
from backend.app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate, 
    db: AsyncSession = Depends(get_db)
):
    repo = ProjectRepository(db)
    return await repo.create(payload)

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    limit: int = 100, 
    offset: int = 0, 
    db: AsyncSession = Depends(get_db)
):
    repo = ProjectRepository(db)
    return await repo.list(limit, offset)

@router.get("/{id}", response_model=ProjectResponse)
async def get_project(id: int, db: AsyncSession = Depends(get_db)):
    repo = ProjectRepository(db)
    project = await repo.get(id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.patch("/{id}", response_model=ProjectResponse)
async def update_project(
    id: int, 
    payload: ProjectUpdate, 
    db: AsyncSession = Depends(get_db)
):
    repo = ProjectRepository(db)
    project = await repo.update(id, payload)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(id: int, db: AsyncSession = Depends(get_db)):
    repo = ProjectRepository(db)
    if not await repo.delete(id):
        raise HTTPException(status_code=404, detail="Project not found")
    return None
