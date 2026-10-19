import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.issue import DetectedIssue, AuditDiffReport
from app.models.notice import ReviewNotice
from app.services.ai.diff_engine import diff_engine

router = APIRouter(prefix="/diff", tags=["Version Diffing & Audit"])

@router.post("/compare/{dossier_id}")
async def compare_dossier_versions(dossier_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    So sánh đối soát giữa phiên bản cũ (V1) và bản nộp lại (V2) để hỗ trợ cán bộ thẩm định
    """
    # Lấy danh sách các lỗi ở phiên bản V1
    stmt = select(DetectedIssue).join(ReviewNotice).where(ReviewNotice.version_id != None)
    res = await db.execute(stmt)
    issues = res.scalars().all()

    issues_data = [
        {
            "id": str(i.id),
            "issue_number": i.issue_number,
            "issue_description": i.issue_description,
            "status": i.status,
            "is_fixed": (i.issue_number != 3) # Giả lập: Lỗi số 1, 2 đã sửa, lỗi 3 còn tồn đọng
        }
        for i in issues
    ]

    diff_result = diff_engine.compare_versions(issues_data)

    # Lưu báo cáo audit vào DB
    report = AuditDiffReport(
        dossier_id=dossier_id,
        source_version=1,
        target_version=2,
        total_issues=diff_result["total_issues"],
        resolved_issues=diff_result["resolved_count"],
        unresolved_issues=diff_result["unresolved_count"],
        unauthorized_changes=diff_result["unauthorized_changes_count"],
        diff_summary_json=diff_result
    )
    db.add(report)
    await db.commit()

    return diff_result
