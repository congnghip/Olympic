from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    x_min: float = 0.0
    y_min: float = 0.0
    x_max: float = 0.0
    y_max: float = 0.0

class ActionPlanItemSchema(BaseModel):
    id: Optional[UUID] = None
    step_order: int
    action_title: str
    technical_guidance: str
    is_completed: bool = False

    class Config:
        from_attributes = True

class DetectedIssueResponse(BaseModel):
    id: UUID
    notice_id: UUID
    drawing_id: Optional[UUID] = None
    drawing_number: Optional[str] = None
    issue_number: int
    issue_description: str
    standard_reference: Optional[str] = None
    discipline: str
    severity: str
    bounding_box: Dict[str, Any]
    status: str
    action_items: List[ActionPlanItemSchema] = []

    class Config:
        from_attributes = True

class ReviewNoticeResponse(BaseModel):
    id: UUID
    version_id: UUID
    notice_code: str
    issuing_authority: str
    s3_key: str
    issued_at: datetime
    issues: List[DetectedIssueResponse] = []

    class Config:
        from_attributes = True

class AIAppraisalTriggerRequest(BaseModel):
    notice_id: UUID
    dossier_id: UUID
    version_number: int = 1

class AIAppraisalResult(BaseModel):
    status: str
    message: str
    total_issues_found: int
    issues: List[DetectedIssueResponse]
