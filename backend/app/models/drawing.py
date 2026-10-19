import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class Drawing(Base):
    __tablename__ = "drawings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_id = Column(UUID(as_uuid=True), ForeignKey("dossier_versions.id"), nullable=False)
    drawing_number = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    discipline = Column(String(50), nullable=False, default="architecture")
    s3_key = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False, default="pdf")
    page_number = Column(Integer, default=1)
    metadata_info = Column("metadata", JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    version = relationship("DossierVersion", back_populates="drawings")
    issues = relationship("DetectedIssue", back_populates="drawing")
