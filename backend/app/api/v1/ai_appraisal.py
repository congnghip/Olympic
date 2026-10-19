import uuid
import asyncio
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.notice import ReviewNotice
from app.models.drawing import Drawing
from app.models.issue import DetectedIssue, ActionPlanItem
from app.models.dossier import Dossier, DossierVersion
from app.schemas.issue import AIAppraisalTriggerRequest, AIAppraisalResult, DetectedIssueResponse
from app.services.ai.docling_parser import docling_parser
from app.services.ai.drawing_grounding import drawing_grounding
from app.services.ai.action_plan_builder import action_plan_builder
from app.services.workflow import workflow_service

router = APIRouter(prefix="/ai", tags=["AI Agent Appraisal"])

@router.post("/analyze", response_model=AIAppraisalResult)
async def run_ai_appraisal(payload: AIAppraisalTriggerRequest, db: AsyncSession = Depends(get_db)):
    """
    KÍCH HOẠT TÁC TỬ AI THẨM ĐỊNH (Core AI Pipeline):
    1. Bóc tách công văn bằng Docling Parser.
    2. Định vị lỗi lên từng bản vẽ (Bounding box grounding).
    3. Sinh kế hoạch hành động sửa chữa (Action Plan items).
    4. Cập nhật trạng thái hồ sơ trong hệ thống.
    """
    # 1. Tìm công văn
    stmt_notice = select(ReviewNotice).where(ReviewNotice.id == payload.notice_id)
    res_notice = await db.execute(stmt_notice)
    notice = res_notice.scalar_one_or_none()
    if not notice:
        raise HTTPException(status_code=404, detail="Không tìm thấy công văn thẩm định")

    # 2. Tìm danh sách bản vẽ của phiên bản này
    stmt_drawings = select(Drawing).where(Drawing.version_id == notice.version_id)
    res_drawings = await db.execute(stmt_drawings)
    drawings = res_drawings.scalars().all()

    # Giả lập độ trễ tính toán nhẹ
    await asyncio.sleep(0.5)

    # 3. Bóc tách công văn thành danh sách lỗi
    raw_text = notice.raw_extracted_text or ""
    extracted_issues = docling_parser.parse_notice_text(raw_text)

    saved_issues = []
    # 4. Duyệt từng lỗi: Định vị bản vẽ & Sinh Action Plan
    for item in extracted_issues:
        # Grounding: Tìm bản vẽ & tính bounding box
        grounding_res = drawing_grounding.map_issue_to_drawing(item, drawings)
        
        issue_model = DetectedIssue(
            notice_id=notice.id,
            drawing_id=grounding_res["drawing_id"],
            issue_number=item["issue_number"],
            issue_description=item["issue_description"],
            standard_reference=item.get("standard_reference"),
            discipline=item.get("discipline", "architecture"),
            severity=item.get("severity", "major"),
            bounding_box=grounding_res["bounding_box"],
            status="open"
        )
        db.add(issue_model)
        await db.flush()

        # Action Plan: Sinh các bước sửa
        plan_steps = action_plan_builder.generate_plan_for_issue(item)
        for step in plan_steps:
            plan_model = ActionPlanItem(
                issue_id=issue_model.id,
                step_order=step["step_order"],
                action_title=step["action_title"],
                technical_guidance=step["technical_guidance"],
                is_completed=False
            )
            db.add(plan_model)

        saved_issues.append(issue_model)

    # 5. Cập nhật trạng thái hồ sơ sang 'revision_required'
    stmt_dossier = select(Dossier).where(Dossier.id == payload.dossier_id)
    res_dossier = await db.execute(stmt_dossier)
    dossier = res_dossier.scalar_one_or_none()
    if dossier:
        dossier.current_status = "revision_required"

    await db.commit()

    # Truy vấn lại dữ liệu hoàn chỉnh để trả về
    stmt_final = select(DetectedIssue).options(
        selectinload(DetectedIssue.action_items)
    ).where(DetectedIssue.notice_id == notice.id).order_by(DetectedIssue.issue_number)
    res_final = await db.execute(stmt_final)
    final_issues = res_final.scalars().all()

    return {
        "status": "success",
        "message": f"AI đã hoàn thành phân tích: Phát hiện {len(final_issues)} vấn đề và sinh Kế hoạch sửa đổi chi tiết.",
        "total_issues_found": len(final_issues),
        "issues": final_issues
    }

@router.get("/issues/{notice_id}", response_model=List[DetectedIssueResponse])
async def get_issues_by_notice(notice_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Lấy danh sách lỗi và kế hoạch sửa đổi của một công văn"""
    stmt = select(DetectedIssue).options(
        selectinload(DetectedIssue.action_items)
    ).where(DetectedIssue.notice_id == notice_id).order_by(DetectedIssue.issue_number)
    res = await db.execute(stmt)
    return res.scalars().all()
