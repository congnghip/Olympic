import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Dossier(Base):
    __tablename__ = "dossiers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dossier_code = Column(String(50), unique=True, nullable=False)
    project_name = Column(String(255), nullable=False)
    construction_type = Column(String(100), default="Nhà ở riêng lẻ")
    location = Column(Text, nullable=False)
    applicant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    assigned_appraiser_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    current_status = Column(String(50), default="draft")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    versions = relationship("DossierVersion", back_populates="dossier", cascade="all, delete-orphan")


class DossierVersion(Base):
    __tablename__ = "dossier_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dossier_id = Column(UUID(as_uuid=True), ForeignKey("dossiers.id"), nullable=False)
    version_number = Column(Integer, nullable=False, default=1)
    submission_note = Column(Text, nullable=True)
    workflow_instance_id = Column(String(255), nullable=True)
    submitted_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    dossier = relationship("Dossier", back_populates="versions")
    drawings = relationship("Drawing", back_populates="version", cascade="all, delete-orphan")
    notices = relationship("ReviewNotice", back_populates="version", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('dossier_id', 'version_number', name='uq_dossier_version'),
    )
