from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    source_type: str
    repository_path: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    repository_path: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
