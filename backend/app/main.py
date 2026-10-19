from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.mcp.server import mcp_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Hệ điều hành Chuyển đổi số DX-OS Open-Core phục vụ Môi trường Dữ liệu Chung (CDE) và Thẩm định Tự động Hồ sơ Xây dựng.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cấu hình CORS cho phép Frontend truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn các routers
app.include_router(api_router, prefix="/api")
app.include_router(mcp_router)

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "system": "DX-OS Open-Core Construction Platform",
        "version": "1.0.0",
        "tier": "Tier 1 (PaaS) & Tier 2 (HPDI Services)",
        "docs": "/docs",
        "mcp_tools": "/mcp/tools"
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}
