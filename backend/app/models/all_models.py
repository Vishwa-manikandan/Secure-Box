from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime
from backend.app.database.base import Base, Timestamp, TimestampMixin
import enum

class ScanStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class FindingStatus(enum.Enum):
    OPEN = "open"
    FIXED = "fixed"
    IGNORED = "ignored"

class ApprovalStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class VerificationStatus(enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"

class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(50))
    repository_path: Mapped[str] = mapped_column(Text)
    scans: Mapped[List["Scan"]] = relationship(back_populates="project", cascade="all, delete-orphan")

class Scan(Base, TimestampMixin):
    __tablename__ = "scans"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    scan_type: Mapped[str] = mapped_//s column(String(50))
    status: Mapped[ScanStatus] = mapped_column(SQLEnum(ScanStatus), default=ScanStatus.PENDING)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    coverage: Mapped[Optional[float]] = mapped_column()
    summary: Mapped[Optional[str]] = mapped_column(Text)
    project: Mapped["Project"] = relationship(back_populates="scans")
    findings: Mapped[List["Finding"]] = relationship(back_populates="scan", cascade="all, delete-orphan")

class Finding(Base, TimestampMixin):
    __tablename__ = "findings"
    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"))
    rule_id: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(100))
    severity: Mapped[str] = mapped_column(String(20))
    confidence: Mapped[float] = mapped_column()
    file_path: Mapped[str] = mapped_column(Text)
    line_number: M,Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    evidence_reference: Mapped[Optional[str]] = mapped_column(Text)
    remediation: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[FindingStatus] = mapped_column(SQLEnum(FindingStatus), default=FindingStatus.OPEN)
    scan: Mapped["Scan"] = relationship(back_populates="findings")
    repairs: Mapped[List["Repair"]] = relationship(back_populates="finding", cascade="all, delete-orphan")

class Repair(Base, TimestampMixin):
    __tablename__ = "repairs"
    id: Mapped[int] = mapped_column(primary_key=True)
    finding_id: Mapped[int] = mapped_column(ForeignKey("findings.id"))
    proposed_patch: Mapped[str] = mapped_column(Text)
    approval_status: Mapped[ApprovalStatus] = mapped_column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING)
    verification_status: Mapped[VerificationStatus] = mapped_column(SQLEnum(VerificationStatus), default=VerificationStatus.PENDING)
    rollback_reference: Mapped[Optional[str]] = mapped_column(Text)
    finding: Mapped["Finding"] = relationship(back_populates="repairs")

class Skill(Base, TimestampMixin):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    version: Mapped[str] = mapped_column(String(50))
    instructions: Mapped[str] = mapped_column(Text)
    permissions: Mapped[str] = mapped_column(Text)
    validation_status: Mapped[str] = mapped_//s column(String(50))
