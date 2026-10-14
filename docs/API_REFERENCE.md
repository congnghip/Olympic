# 🔌 Đặc Tả Giao Diện Lập Trình DX-OS Open-Core (API Reference)

Tất cả các dịch vụ Tầng 1 và Ứng dụng Tầng 2/3 giao tiếp thông qua hệ thống RESTful API đạt chuẩn OpenAPI 3.0 và WebSocket.

---

## 📡 1. Cổng Dịch Vụ Định Danh & Nền Tảng Lõi (Tầng 1 PaaS)

### `POST /api/auth/token`
* **Mô tả:** Cấp phát mã định danh JWT tập trung cho các tác nhân hệ thống (Điều phối viên, Tài xế, API Client).
* **Request:**
```json
{
  "username": "operator01",
  "password": "secure_password"
}
```
* **Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni...",
  "token_type": "bearer",
  "expires_in": 86400,
  "role": "OPERATOR"
}
```

---

## 📡 2. Cổng Điều Phối & Tối Ưu Lộ Trình WebGIS (Port 8502)

### `GET /api/waste/presets`
* **Mô tả:** Lấy danh mục kịch bản đô thị mẫu (Quận 1, Quận 3...) kèm tọa độ trạm trung chuyển (depot) và các bô rác.

### `POST /api/waste/solve`
* **Mô tả:** Thực thi thuật toán tối ưu đa xe 3D-ACO giải bài toán định tuyến.
* **Request:**
```json
{
  "depot": {"lat": 10.7745, "lon": 106.7042},
  "bins": [...],
  "trucks_count": 3,
  "truck_capacity": 150,
  "solver_choice": "paco"
}
```
* **Response:**
```json
{
  "status": "success",
  "execution_time_ms": 38.2,
  "total_distance_km": 14.8,
  "co2_saved_kg": 4.22,
  "routes": [...]
}
```

### `POST /api/waste/incident`
* **Mô tả:** Đón nhận sự cố rào chắn/xe hỏng và tính toán lại lộ trình tức thời (< 50ms).

### `POST /api/waste/driver-report`
* **Mô tả:** Tác tử Kev AI tiếp nhận báo cáo bằng giọng nói/văn bản của tài xế và phân loại ngữ nghĩa.
* **Request:**
```json
{
  "truck_id": 1,
  "driver_report": "Hẻm 42 Nguyễn Huệ đang sửa cống xe tải không vào được",
  "gps": {"lat": 10.7735, "lon": 106.7032}
}
```
* **Response:**
```json
{
  "incident_category": "access_blocked",
  "confidence": 0.96,
  "dispatcher_action": "enable_walk_in_alley",
  "message": "Đã chuyển sang chế độ đi bộ thu gom đầu hẻm"
}
```
