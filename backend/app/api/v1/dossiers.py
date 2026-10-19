import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.dossier import Dossier, DossierVersion
from app.models.drawing import Drawing
from app.schemas.dossier import DossierCreate, DossierResponse, DrawingResponse
from app.services.storage import storage_service
from app.services.workflow import workflow_service

router = APIRouter(prefix="/dossiers", tags=["Dossiers & Drawings"])

@router.get("", response_model=List[DossierResponse])
async def list_dossiers(db: AsyncSession = Depends(get_db)):
    """Lấy danh sách toàn bộ hồ sơ xây dựng trong CDE"""
    stmt = select(Dossier).options(
        selectinload(Dossier.versions).selectinload(DossierVersion.drawings)
    ).order_by(Dossier.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("", response_model=DossierResponse)
async def create_dossier(payload: DossierCreate, db: AsyncSession = Depends(get_db)):
    """Tạo mới hồ sơ đề nghị thẩm định xây dựng"""
    # Sinh mã hồ sơ ngẫu nhiên: HS-2026-XXXX
    short_id = uuid.uuid4().hex[:4].upper()
    dossier_code = f"HS-2026-{short_id}"

    new_dossier = Dossier(
        dossier_code=dossier_code,
        project_name=payload.project_name,
        construction_type=payload.construction_type,
        location=payload.location,
        current_status="draft"
    )
    db.add(new_dossier)
    await db.flush()

    # Tự động tạo Version 1
    v1 = DossierVersion(
        dossier_id=new_dossier.id,
        version_number=1,
        submission_note="Khởi tạo hồ sơ lần 1"
    )
    db.add(v1)
    await db.commit()

    stmt = select(Dossier).options(
        selectinload(Dossier.versions).selectinload(DossierVersion.drawings)
    ).where(Dossier.id == new_dossier.id)
    res = await db.execute(stmt)
    return res.scalar_one()

@router.post("/{dossier_id}/drawings", response_model=DrawingResponse)
async def upload_drawing(
    dossier_id: uuid.UUID,
    drawing_number: str = Form(...),
    title: str = Form(...),
    discipline: str = Form("architecture"),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Tải lên bản vẽ kỹ thuật (PDF) vào MinIO S3 và liên kết vào hồ sơ"""
    # Lấy phiên bản mới nhất của hồ sơ
    stmt = select(DossierVersion).where(DossierVersion.dossier_id == dossier_id).order_by(DossierVersion.version_number.desc())
    res = await db.execute(stmt)
    latest_version = res.scalars().first()

    if not latest_version:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên bản hồ sơ")

    file_bytes = await file.read()
    s3_filename = f"dossiers/{dossier_id}/v{latest_version.version_number}/{drawing_number}_{file.filename}"
    s3_key = storage_service.upload_file(s3_filename, file_bytes, content_type=file.content_type or "application/pdf")

    drawing = Drawing(
        version_id=latest_version.id,
        drawing_number=drawing_number,
        title=title,
        discipline=discipline,
        s3_key=s3_key,
        file_type="pdf",
        page_number=1,
        metadata_info={"original_filename": file.filename, "size_bytes": len(file_bytes)}
    )
    db.add(drawing)
    await db.commit()
    await db.refresh(drawing)
    return drawing
