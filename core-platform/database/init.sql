-- ====================================================================
-- DX-OS Open-Core: Database Schema (PostgreSQL + PostGIS Extension)
-- Tầng 1: Quản trị Dữ liệu Không gian & Giao dịch cấp Doanh nghiệp
-- ====================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- 1. Quản lý Đa thuê ước (Multi-tenancy)
CREATE TABLE IF NOT EXISTS dx_tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Định danh & Phân quyền tập trung (Identity & RBAC)
CREATE TABLE IF NOT EXISTS dx_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES dx_tenants(id),
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'OPERATOR', -- ADMIN, OPERATOR, DRIVER, FIELD_WORKER
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Trạm Trung Chuyển (Depots - Spatial GIS)
CREATE TABLE IF NOT EXISTS smart_depots (
    id SERIAL PRIMARY KEY,
    tenant_id UUID REFERENCES dx_tenants(id),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    location GEOMETRY(Point, 4326),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Điểm Tập Kết & Thùng Rác Thông Minh (Smart Waste Bins - IoT Sensors)
CREATE TABLE IF NOT EXISTS smart_waste_bins (
    id SERIAL PRIMARY KEY,
    tenant_id UUID REFERENCES dx_tenants(id),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    collection_type VARCHAR(50) DEFAULT 'home', -- home, centralized, flexible
    fill_level INT DEFAULT 0, -- 0 - 100%
    demand INT DEFAULT 10,
    has_smell BOOLEAN DEFAULT FALSE,
    location GEOMETRY(Point, 4326),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Nhật Ký Sự Cố Hiện Trường & Điều Phối Tuyến (Incident Events)
CREATE TABLE IF NOT EXISTS incident_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES dx_tenants(id),
    truck_id INT NOT NULL,
    incident_type VARCHAR(50) NOT NULL, -- roadblock, vehicle_breakdown, flood, invalid_waste
    severity VARCHAR(20) DEFAULT 'HIGH',
    status VARCHAR(20) DEFAULT 'RESOLVED',
    driver_report TEXT,
    resolved_detour_ms INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Định Vị GPS Vệ Tinh Phương Tiện (Vehicle Telemetry - Traccar IoT)
CREATE TABLE IF NOT EXISTS vehicle_telemetry (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id INT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    speed DOUBLE PRECISION DEFAULT 0.0,
    heading DOUBLE PRECISION DEFAULT 0.0,
    battery_level INT DEFAULT 100,
    alarm_status VARCHAR(50), -- normal, sos, speed_warning
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Sổ Cái Kiểm Toán Bất Biến (Immutable Audit Trail)
CREATE TABLE IF NOT EXISTS dx_audit_logs (
    id BIGSERIAL PRIMARY KEY,
    actor_id UUID,
    action VARCHAR(100) NOT NULL,
    entity_name VARCHAR(100) NOT NULL,
    entity_id VARCHAR(100),
    changes_json JSONB,
    ip_address VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
