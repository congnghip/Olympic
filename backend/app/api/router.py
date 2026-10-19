from fastapi import APIRouter
from app.api.v1.dossiers import router as dossiers_router
from app.api.v1.notices import router as notices_router
from app.api.v1.ai_appraisal import router as ai_router
from app.api.v1.diff import router as diff_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(dossiers_router)
api_router.include_router(notices_router)
api_router.include_router(ai_router)
api_router.include_router(diff_router)
