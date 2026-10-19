import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class DetectedIssue(Base):
    __tablename__ = "detected_issues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notice_id = Column(UUID(as_uuid=True), ForeignKey("review_notices.id"), nullable=False)
    drawing_id = Column(UUID(as_uuid=True), ForeignKey("drawings.id"), nullable=True)
    issue_number = Column(Integer, nullable=False)
    issue_description = Column(Text, nullable=False)
    standard_reference = Column(String(255), nullable=True)
    discipline = Column(String(50), default="architecture")
    severity = Column(String(20), default="major")
    bounding_box = Column(JSONB, default=lambda: {"x_min": 0, "y_min": 0, "x_max": 0, "y_max": 0})
    status = Column(String(50), default="open")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    notice = relationship("ReviewNotice", back_populates="issues")
    drawing = relationship("Drawing", back_populates="issues")
    action_items = relationship("ActionPlanItem", back_populates="issue", cascade="all, delete-orphan")


class ActionPlanItem(Base):
    __tablename__ = "action_plan_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(UUID(as_uuid=True), ForeignKey("detected_issues.id"), nullable=False)
    step_order = Column(Integer, nullable=False)
    action_title = Column(String(255), nullable=False)
    technical_guidance = Column(Text, nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    issue = relationship("DetectedIssue", back_populates="action_items")


class AuditDiffReport(Base):
    __tablename__ = "audit_diff_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dossier_id = Column(UUID(as_uuid=True), ForeignKey("dossiers.id"), nullable=False)
    source_version = Column(Integer, nullable=False)
    target_version = Column(Integer, nullable=False)
    total_issues = Column(Integer, default=0)
    resolved_issues = Column(Integer, default=0)
    unresolved_issues = Column(Integer, default=0)
    unauthorized_changes = Column(Integer, default=0)
    diff_summary_json = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
