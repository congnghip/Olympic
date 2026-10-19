import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class ReviewNotice(Base):
    __tablename__ = "review_notices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_id = Column(UUID(as_uuid=True), ForeignKey("dossier_versions.id"), nullable=False)
    notice_code = Column(String(100), nullable=False)
    issuing_authority = Column(String(255), default="Sở Xây dựng / Phòng Quản lý Đô thị")
    s3_key = Column(String(500), nullable=False)
    raw_extracted_text = Column(Text, nullable=True)
    issued_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    version = relationship("DossierVersion", back_populates="notices")
    issues = relationship("DetectedIssue", back_populates="notice", cascade="all, delete-orphan")
