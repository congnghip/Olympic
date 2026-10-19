-- ==============================================================================
-- DX-OS OPEN-CORE: CDE & AI-POWERED CONSTRUCTION APPRAISAL PLATFORM
-- DATABASE INITIALIZATION SCHEMA (POSTGRESQL 16)
-- Conforming to SRS.md Entity-Relationship Diagram (ERD)
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. BẢNG NGƯỜI DÙNG (USERS - Tích hợp Keycloak SSO / Local RBAC)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keycloak_id VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('applicant', 'appraiser', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. BẢNG HỒ SƠ XÂY DỰNG (DOSSIERS)
CREATE TABLE IF NOT EXISTS dossiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dossier_code VARCHAR(50) UNIQUE NOT NULL, -- Ví dụ: HS-2026-0012
    project_name VARCHAR(255) NOT NULL,
    construction_type VARCHAR(100) DEFAULT 'Nhà ở riêng lẻ', -- Nhà ở riêng lẻ, Nhà xưởng, etc.
    location TEXT NOT NULL,
    applicant_id UUID REFERENCES users(id) ON DELETE SET NULL,
    assigned_appraiser_id UUID REFERENCES users(id) ON DELETE SET NULL,
    current_status VARCHAR(50) NOT NULL DEFAULT 'draft' 
        CHECK (current_status IN ('draft', 'submitted', 'ai_analyzing', 'under_review', 'revision_required', 'approved', 'rejected')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. BẢNG PHIÊN BẢN HỒ SƠ (DOSSIER VERSIONS - V1, V2, V3)
CREATE TABLE IF NOT EXISTS dossier_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dossier_id UUID NOT NULL REFERENCES dossiers(id) ON DELETE CASCADE,
    version_number INT NOT NULL DEFAULT 1,
    submission_note TEXT,
    workflow_instance_id VARCHAR(255), -- ID luồng trong Flowable BPMN
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (dossier_id, version_number)
);

-- 4. BẢNG BẢN VẼ THIẾT KẾ (DRAWINGS)
CREATE TABLE IF NOT EXISTS drawings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID NOT NULL REFERENCES dossier_versions(id) ON DELETE CASCADE,
    drawing_number VARCHAR(50) NOT NULL, -- KT-01, KC-02, PCCC-01
    title VARCHAR(255) NOT NULL,          -- Mặt bằng Tầng 1, Mặt đứng trục 1-4
    discipline VARCHAR(50) NOT NULL DEFAULT 'architecture' 
        CHECK (discipline IN ('architecture', 'structure', 'mep', 'fire_safety', 'civil')),
    s3_key VARCHAR(500) NOT NULL,         -- Đường dẫn lưu trữ trong MinIO
    file_type VARCHAR(20) NOT NULL DEFAULT 'pdf' CHECK (file_type IN ('pdf', 'dxf', 'dwg', 'ifc')),
    page_number INT DEFAULT 1,
    metadata JSONB DEFAULT '{}'::jsonb,   -- scale, dimensions, grid_axes, bounding_info
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. BẢNG CÔNG VĂN YÊU CẦU SỬA ĐỔI BỔ SUNG (REVIEW NOTICES)
CREATE TABLE IF NOT EXISTS review_notices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id UUID NOT NULL REFERENCES dossier_versions(id) ON DELETE CASCADE,
    notice_code VARCHAR(100) NOT NULL,    -- Công văn số 123/SXD-QLĐT
    issuing_authority VARCHAR(255) DEFAULT 'Sở Xây dựng / Phòng Quản lý Đô thị',
    s3_key VARCHAR(500) NOT NULL,         -- File PDF/Scan công văn lưu trong MinIO
    raw_extracted_text TEXT,              -- Kết quả OCR bóc tách từ Docling
    issued_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. BẢNG DANH SÁCH LỖI / VẤN ĐỀ ĐƯỢC AI BÓC TÁCH (DETECTED ISSUES)
CREATE TABLE IF NOT EXISTS detected_issues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    notice_id UUID NOT NULL REFERENCES review_notices(id) ON DELETE CASCADE,
    drawing_id UUID REFERENCES drawings(id) ON DELETE SET NULL, -- Ánh xạ đến bản vẽ cụ thể
    issue_number INT NOT NULL,            -- Thứ tự mục lỗi (Mục 1, Mục 2...)
    issue_description TEXT NOT NULL,      -- Chi tiết nội dung lỗi
    standard_reference VARCHAR(255),      -- Quy chuẩn đối chiếu: QCVN 06:2022 Mục 3.2.1
    discipline VARCHAR(50) DEFAULT 'architecture',
    severity VARCHAR(20) DEFAULT 'major' CHECK (severity IN ('critical', 'major', 'minor')),
    bounding_box JSONB DEFAULT '{"x_min": 0, "y_min": 0, "x_max": 0, "y_max": 0}'::jsonb, -- Tọa độ highlight trên bản vẽ
    status VARCHAR(50) DEFAULT 'open' CHECK (status IN ('open', 'resolved', 'ignored')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. BẢNG KẾ HOẠCH HÀNH ĐỘNG SỬA ĐỔI (ACTION PLAN ITEMS)
CREATE TABLE IF NOT EXISTS action_plan_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    issue_id UUID NOT NULL REFERENCES detected_issues(id) ON DELETE CASCADE,
    step_order INT NOT NULL,
    action_title VARCHAR(255) NOT NULL,
    technical_guidance TEXT NOT NULL,      -- Hướng dẫn kỹ thuật khắc phục
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. BẢNG NHẬT KÝ KIỂM TOÁN VÀ ĐỐI SOÁT PHIÊN BẢN (AUDIT & DIFF LOGS)
CREATE TABLE IF NOT EXISTS audit_diff_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dossier_id UUID NOT NULL REFERENCES dossiers(id) ON DELETE CASCADE,
    source_version INT NOT NULL,           -- V1
    target_version INT NOT NULL,           -- V2
    total_issues INT DEFAULT 0,
    resolved_issues INT DEFAULT 0,
    unresolved_issues INT DEFAULT 0,
    unauthorized_changes INT DEFAULT 0,    -- Cảnh báo thay đổi ngoài phạm vi yêu cầu
    diff_summary_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- TẠO DỮ LIỆU MẪU ĐẦU TIÊN (SEEDS)
INSERT INTO users (id, email, full_name, role) VALUES 
('00000000-0000-0000-0000-000000000001', 'kts.nguyen@arch.vn', 'KTS. Nguyễn Văn A', 'applicant'),
('00000000-0000-0000-0000-000000000002', 'canbo.tran@soxaydung.gov.vn', 'Chuyên viên Trần Văn B', 'appraiser'),
('00000000-0000-0000-0000-000000000003', 'admin@dxos.open', 'Quản trị viên Hệ thống', 'admin')
ON CONFLICT (email) DO NOTHING;
