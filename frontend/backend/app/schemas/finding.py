from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class FindingStatus(str, Enum):
    OPEN = "open"
    FIXED = "fixed"
    IGNORED = "ignored"

class FindingBase(BaseModel):
    rule_id: str
    category: str
    severity: str
    confidence: float
    file_path: str
    line_number: int
    description: str
    evidence_reference: Optional[str] = None
    remediation: Optional[str] = None

class FindingCreate(FindingBase):
    scan_id: int

class FindingResponse(FindingBase):
    id: int
    scan_id: int
    status: FindingStatus
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
