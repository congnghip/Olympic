# Tài Liệu Đặc Tả API (API Reference)

Hệ thống cung cấp hai nhóm cổng API phục vụ giao diện bản đồ điều phối thời gian thực (Port 8502) và điều phối giải thuật tối ưu hóa lõi (Port 8000).

---

## 1. Nhóm API Bản Đồ Điều Phối & Sự Cố (Port 8502)

### `GET /api/waste/presets`
* **Mô tả:** Lấy danh mục kịch bản đô thị mẫu (Quận 1, Quận 3) kèm tọa độ điểm tập kết (Depot), danh sách bô rác và kịch bản sự cố.
* **Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Q.1 Trung Tâm & Phố Đi Bộ",
    "theme_color": "#10b981",
    "depot": {"id": 0, "name": "Trạm tập kết Bến Nghé", "lat": 10.7745, "lon": 106.7042},
    "bins": [
      {
        "id": 1,
        "name": "Hộ dân ngõ 42 Nguyễn Huệ (Hẻm sâu)",
        "lat": 10.7735,
        "lon": 106.7032,
        "fill_level": 90,
        "demand": 45,
        "has_smell": true,
        "collection_type": "home"
      }
    ],
    "incidents": [...]
  }
]
```

### `POST /api/waste/solve`
* **Mô tả:** Tối ưu hóa phân bổ tuyến đường cho đội xe gom rác bằng giải thuật Clarke-Wright Savings kết hợp heuristic ưu tiên rác bốc mùi.
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
* **Response (200 OK):**
```json
{
  "status": "success",
  "execution_time_ms": 32.5,
  "total_distance_km": 14.8,
  "co2_saved_kg": 4.22,
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

### `POST /api/waste/compare`
* **Mô tả:** Chạy đồng thời và so sánh hiệu năng giữa bộ giải cải tiến, Google OR-Tools và Baseline.
* **Response (200 OK):** Trả về bảng đối chiếu thời gian chạy (ms), tổng quãng đường (km), và lượng phát thải $\text{CO}_2$ cắt giảm.

### `POST /api/waste/resolve-incident`
* **Mô tả:** Tái định tuyến thời gian thực khi phát sinh sự cố rào chắn công trình hoặc xe hỏng hóc giữa tuyến.
* **Request:**
```json
{
  "incident": {
    "type": "roadblock",
    "blocked_segment": {
      "start_lat": 10.7735, "start_lon": 106.7032,
      "end_lat": 10.7725, "end_lon": 106.6980
    }
  },
  "current_truck_state": {"id": 1, "lat": 10.7730, "lon": 106.7020},
  "all_trucks": [...]
}
```

### `POST /api/waste/driver-report`
* **Mô tả:** Tiếp nhận báo cáo bằng giọng nói/văn bản của tài xế và phân loại sự cố để kích hoạt hành vi nghiệp vụ (ví dụ: chế độ đi bộ thu gom ngõ hẻm).

---

## 2. Nhóm API Giải Thuật Lõi VRP (Port 8000)

* **`POST /api/solve`:** Thực thi giải bài toán VRP chuẩn định dạng Solomon thông qua trình bao bọc gọi bộ giải C++.
* **`POST /api/generate-instance`:** Sinh dữ liệu bài toán ngẫu nhiên phục vụ kiểm thử tải.
* **`GET /docs`:** Giao diện tài liệu tương tác trực tiếp Swagger UI.
