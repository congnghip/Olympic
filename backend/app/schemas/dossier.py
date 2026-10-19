from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

# DRAWING SCHEMAS
class DrawingBase(BaseModel):
    drawing_number: str
    title: str
    discipline: str = "architecture"
    page_number: int = 1
    metadata_info: Optional[Dict[str, Any]] = None

class DrawingCreate(DrawingBase):
    s3_key: str
    file_type: str = "pdf"

class DrawingResponse(DrawingBase):
    id: UUID
    version_id: UUID
    s3_key: str
    file_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# DOSSIER SCHEMAS
class DossierBase(BaseModel):
    project_name: str
    construction_type: str = "Nhà ở riêng lẻ"
    location: str

class DossierCreate(DossierBase):
    applicant_email: Optional[str] = None

class DossierVersionResponse(BaseModel):
    id: UUID
    dossier_id: UUID
    version_number: int
    submission_note: Optional[str] = None
    workflow_instance_id: Optional[str] = None
    submitted_at: datetime
    drawings: List[DrawingResponse] = []

    class Config:
        from_attributes = True

class DossierResponse(DossierBase):
    id: UUID
    dossier_code: str
    current_status: str
    created_at: datetime
    updated_at: datetime
    versions: List[DossierVersionResponse] = []

    class Config:
        from_attributes = True
