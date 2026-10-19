import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.dossier import DossierVersion
from app.models.notice import ReviewNotice
from app.schemas.issue import ReviewNoticeResponse
from app.services.storage import storage_service

router = APIRouter(prefix="/notices", tags=["Review Notices"])

@router.post("/upload", response_model=ReviewNoticeResponse)
async def upload_review_notice(
    dossier_id: uuid.UUID,
    notice_code: str = Form(...),
    issuing_authority: str = Form("Sở Xây dựng"),
    notice_text: str = Form(None),
    file: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Tiếp nhận công văn yêu cầu sửa đổi bổ sung từ cơ quan thẩm định.
    Lưu file PDF vào MinIO và lưu nội dung text vào CSDL.
    """
    stmt = select(DossierVersion).where(DossierVersion.dossier_id == dossier_id).order_by(DossierVersion.version_number.desc())
    res = await db.execute(stmt)
    latest_version = res.scalars().first()

    if not latest_version:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên bản hồ sơ")

    s3_key = "notices/manual-text-notice.pdf"
    if file:
        file_bytes = await file.read()
        s3_filename = f"dossiers/{dossier_id}/notices/{notice_code}_{file.filename}"
        s3_key = storage_service.upload_file(s3_filename, file_bytes, content_type=file.content_type or "application/pdf")

    notice = ReviewNotice(
        version_id=latest_version.id,
        notice_code=notice_code,
        issuing_authority=issuing_authority,
        s3_key=s3_key,
        raw_extracted_text=notice_text or ""
    )
    db.add(notice)
    await db.commit()

    stmt_full = select(ReviewNotice).options(selectinload(ReviewNotice.issues)).where(ReviewNotice.id == notice.id)
    res_full = await db.execute(stmt_full)
    return res_full.scalar_one()
