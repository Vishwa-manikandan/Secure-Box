from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class ScanStatus(str, Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class ScanBase(BaseModel):
    scan_type: str

class ScanCreate(ScanBase):
    project_id: int

class ScanResponse(ScanBase):
    id: int
    project_id: int
    status: ScanStatus
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    coverage: Optional[float]
    summary: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
