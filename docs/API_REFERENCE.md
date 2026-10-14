# Tài Liệu Đặc Tả Giao Diện Lập Trình (API Reference)

Hệ thống cung cấp hệ thống giao diện lập trình RESTful API đạt chuẩn OpenAPI 3.0, hỗ trợ tích hợp với hệ thống giám sát xe GPS (như Traccar) và các cổng thông tin đô thị thông minh.

---

## 📡 Danh Sách Các Endpoint Chính

### 1. Phân Hệ Điều Phối Gom Rác & Sự Cố (Port 8502)

#### `GET /api/waste/presets`
* **Mô tả:** Lấy danh sách các kịch bản mẫu đô thị (Quận 1, Quận 3, Thủ Đức...) kèm tọa độ điểm gom và trạm trung chuyển.
* **Response (JSON):**
```json
[
  {
    "id": 1,
    "name": "Q.1 Trung Tâm & Phố Đi Bộ",
    "depot": {"id": 0, "name": "Trạm tập kết Bến Nghé", "lat": 10.7745, "lon": 106.7042},
    "bins": [
      {
        "id": 1,
        "name": "Hộ dân ngõ 42 Nguyễn Huệ",
        "lat": 10.7735,
        "lon": 106.7032,
        "fill_level": 90,
        "demand": 45,
        "has_smell": true
      }
    ]
  }
]
```

#### `POST /api/waste/solve`
* **Mô tả:** Tính toán lộ trình tối ưu cho toàn bộ đội xe gom rác dựa trên trạng thái điểm gom hiện tại.
* **Request Body:**
```json
{
  "depot": {"lat": 10.7745, "lon": 106.7042},
  "bins": [...],
  "trucks_count": 3,
  "truck_capacity": 150,
  "solver_choice": "paco"
}
```
* **Response (JSON):**
```json
{
  "status": "success",
  "execution_time_ms": 32.5,
  "total_distance_km": 14.8,
  "co2_saved_kg": 4.2,
  "routes": [
    {
      "truck_id": 1,
      "route_points": [...],
      "path_coordinates": [[10.7745, 106.7042], ...],
      "load": 135
    }
  ]
}
```

#### `POST /api/waste/incident`
* **Mô tả:** Kích hoạt sự cố động (đường bị rào chắn hoặc xe hỏng) và tính toán lại lộ trình tức thì.
* **Request Body:**
```json
{
  "incident_type": "roadblock",
  "blocked_segment": {
    "start_lat": 10.7735, "start_lon": 106.7032,
    "end_lat": 10.7725, "end_lon": 106.6980
  },
  "current_truck": {"id": 1, "lat": 10.7730, "lon": 106.7020}
}
```

#### `POST /api/waste/driver-report`
* **Mô tả:** Tiếp nhận báo cáo giọng nói/văn bản từ tài xế hiện trường và xử lý thông qua mô hình phân loại thông minh.
* **Request Body:**
```json
{
  "truck_id": 1,
  "driver_report": "Hẻm 42 bị phong tỏa thi công cáp quang",
  "gps": {"lat": 10.7735, "lon": 106.7032, "speed": 0}
}
```

---

### 2. Phân Hệ Thuật Toán Lõi VRP (Port 8000)

* `GET /docs`: Swagger UI tương tác trực tiếp.
* `POST /api/solve`: Endpoint giải bài toán VRP định dạng chuẩn Solomon / Li & Lim bằng C++ 3D-ACO.
* `POST /api/generate-instance`: Sinh dữ liệu thử nghiệm ngẫu nhiên phục vụ đánh giá độ phức tạp thuật toán.
