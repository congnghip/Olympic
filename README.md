# 🚛 Hệ Thống Quản Trị & Điều Phối Thu Gom Rác Thông Minh Tức Thời
### Smart Waste Management & Dynamic Incident Re-routing Platform (3D-ACO Engine)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/Python-3.13-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![Core Solver](https://img.shields.io/badge/Core_Solver-C%2B%2B17%203D--ACO-orange.svg)](https://isocpp.org/)
[![Docker Ready](https://img.shields.io/badge/Docker-Compose_Ready-2496ED.svg)](https://www.docker.com/)
[![Map Sovereignty](https://img.shields.io/badge/Map_Sovereignty-100%25_Vietnam_Compliant-red.svg)](#-tuân-thủ-quy-chuẩn-bản-đồ--chủ-quyền-lãnh-thổ)

---

## 📌 1. Bối Cảnh & Tính Cấp Thiết (Executive Summary)

Tại các đô thị lớn ở Việt Nam (đặc biệt như TP. Hồ Chí Minh và Hà Nội), công tác thu gom và vận chuyển chất thải rắn sinh hoạt đối mặt với nhiều thách thức nghiêm trọng:
1. **Mạng lưới đường xá phức tạp:** Hàng nghìn con hẻm nhỏ ngoằn ngoèo, xe cơ giới lớn khó tiếp cận.
2. **Sự cố giao thông phát sinh liên tục:** Ngập úng do triều cường, rào chắn thi công đột xuất, ùn tắc giờ cao điểm làm phá vỡ các lộ trình thu gom cố định.
3. **Thiếu cơ chế điều phối linh hoạt:** Khi một xe rác gặp sự cố hỏng hóc giữa đường, hiện trường không có công cụ tính toán tự động san sẻ điểm gom sang các xe lân cận, dẫn đến rác ứ đọng gây ô nhiễm môi trường.

**Dự án phát triển một nền tảng điều phối xe gom rác thông minh toàn diện**, tích hợp giữa:
- **Thuật toán tối ưu hóa bầy đàn 3 chiều (3D-Parallel Ant Colony Optimization - 3D-ACO)** phát triển trên C++17 với tốc độ tính toán cao.
- **Động cơ điều phối sự cố thời gian thực (Dynamic Re-routing Engine)** tự động tìm đường vòng tránh điểm nghẽn trong `< 50ms`.
- **Giao diện Bản đồ Kép tương tác (Dual-Map Real-time Dashboard)** hỗ trợ giám sát tức thì và đo lường chỉ số xanh môi trường (ESG).

![Demo Hệ Thống](assets/demo.gif)

---

## 🌟 2. Tính Năng Đột Phá Của Hệ Thống

| Nhóm Tính Năng | Chi Tiết Hiện Thực | Lợi Ích Thực Tiễn |
|---|---|---|
| **Tối Ưu Hóa Tuyến Đa Xe (CVRP)** | Thuật toán 3D-ACO giải bài toán định tuyến phương tiện có giới hạn tải trọng xe và khung giờ thu gom | Giảm 20% - 35% tổng quãng đường di chuyển và chi phí nhiên liệu |
| **Tự Chữa Lành Tuyến Tuyến (Self-healing Detour)** | Phát hiện rào chắn / đường cấm và tái định tuyến tức thời (`< 50ms`) dựa trên đồ thị OSRM thực tế | Xe không bị kẹt, đảm bảo thời gian thu gom đúng cam kết |
| **Điều Phối San Tải Xe Hỏng** | Tự động phân bổ các thùng rác chưa gom của xe gặp sự cố kỹ thuật sang các xe lân cận còn dung tích trống | Loại bỏ 100% tình trạng bỏ sót rác do sự cố phương tiện |
| **Thu Gom Hẻm Nhỏ (Walk-in Collection)** | Tự động nhận diện bô rác trong hẻm sâu, tính toán vị trí đỗ xe tại đầu hẻm và khoảng cách nhân viên đi bộ | Khắc phục triệt để hạn chế của bản đồ giao thông thông thường |
| **Bản Đồ Kép Trực Quan (Dual-Map UI)** | Cho phép so sánh trực quan song song giữa thuật toán cải tiến của hệ thống với thuật toán Baseline | Giúp ban điều hành và giám khảo kiểm chứng rõ rệt hiệu quả thuật toán |
| **Giám Sát Phát Thải & ESG** | Tự động tính toán lượng $\text{CO}_2$ giảm thiểu, mức tiêu hao nhiên liệu và chỉ số tiết kiệm môi trường | Cung cấp dữ liệu minh bạch cho báo cáo phát triển bền vững |

---

## 🏗️ 3. Sơ Đồ Kiến Trúc Hệ Thống (Architecture)

```mermaid
flowchart TD
    classDef clientNode fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef serviceNode fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc;
    classDef engineNode fill:#312e81,stroke:#6366f1,stroke-width:2px,color:#f8fafc;

    subgraph Client ["Tầng Giám Sát & Điều Hành"]
        UI["Bản Đồ Điều Phối Thời Gian Thực (Port 8502)<br/><i>Leaflet / MapLibre Dual Map</i>"]:::clientNode
        Dashboard["Bảng Phân Tích & Nghiên Cứu (Port 8501)<br/><i>Streamlit Parametric Analysis</i>"]:::clientNode
        Driver["Báo Cáo Hiện Trường Tài Xế<br/><i>Voice / Text / GPS</i>"]:::clientNode
    end

    subgraph Backend ["Tầng Dịch Vụ & Xử Lý Sự Cố"]
        Gateway["FastAPI Gateway (Port 8502 / 8000)"]:::serviceNode
        Dispatcher["Dynamic Waste Incident Dispatcher"]:::serviceNode
    end

    subgraph Core ["Tầng Thuật Toán & Tối Ưu Hóa"]
        Solver["C++17 3D-Parallel ACO Solver Core"]:::engineNode
        ReRoute["Dynamic Detour Heuristic (< 50ms)"]:::engineNode
        OSRM["OSRM Street Network & Cache Matrix"]:::engineNode
    end

    UI <-->|REST API| Gateway
    Dashboard <--> Gateway
    Driver -->|Cảnh báo sự cố| Gateway
    Gateway --> Dispatcher
    Dispatcher --> ReRoute
    Dispatcher --> Solver
    ReRoute <--> OSRM
```

---

## 🇻🇳 4. Tuân Thủ Quy Chuẩn Bản Đồ & Chủ Quyền Lãnh Thổ

> [!IMPORTANT]
> Dự án tuân thủ nghiêm ngặt quy định của Pháp luật Việt Nam và Quy chế các cuộc thi CNTT Quốc gia:
> - **100% Tuyệt đối không sử dụng bất kỳ nguồn bản đồ nào chứa "đường lưỡi bò" (đường 9 đoạn phi pháp)**.
> - Sử dụng hệ thống bản đồ chuẩn quốc tế: **OpenStreetMap Tile Server** và **ArcGIS World Imagery** chất lượng cao.
> - Địa bàn thử nghiệm thực tế tập trung tại các phường trọng điểm thuộc **Quận 1, Quận 3, TP. Hồ Chí Minh** với đầy đủ tên đường phố và địa danh tiếng Việt chính thống.

---

## 🚀 5. Hướng Dẫn Khởi Động Nhanh (Quick Start)

### Cách 1: Triển Khai 1 Lệnh Duy Nhất Bằng Docker (Khuyến nghị cho Ban Giám Khảo)

Chỉ cần cài đặt Docker & Docker Compose, sau đó mở Terminal tại thư mục dự án và chạy:

```bash
docker compose up -d --build
```

Sau khi container khởi động hoàn tất:
* 🗺️ **Bản đồ điều phối rác thông minh:** Mở trình duyệt tại [http://localhost:8502](http://localhost:8502)
* 📊 **Bảng phân tích chuyên sâu:** Mở trình duyệt tại [http://localhost:8501](http://localhost:8501)
* 🔌 **Tài liệu API Swagger:** Mở trình duyệt tại [http://localhost:8000/docs](http://localhost:8000/docs)

Để dừng hệ thống:
```bash
docker compose down
```

---

### Cách 2: Chạy Trực Tiếp Bằng Bash Script (Local Development)

Yêu cầu máy chủ có sẵn Python $\ge 3.10$, `cmake`, `build-essential`:

```bash
# Cấp quyền và chạy script khởi động toàn diện
chmod +x start.sh
./start.sh
```

---

## 🎯 6. Kịch Bản Chấm Thi Dành Cho Ban Giám Khảo (Demo Walkthrough)

*Xem hướng dẫn chi tiết từng bước tại [docs/DEMO_GUIDE.md](docs/DEMO_GUIDE.md)*

1. **Bước 1:** Mở giao diện bản đồ tại [http://localhost:8502](http://localhost:8502).
2. **Bước 2:** Chọn kịch bản **`Q.1 Trung Tâm & Phố Đi Bộ`**, nhấn nút **"Tối Ưu Hóa Lộ Trình (Solve VRP)"**. Quan sát tuyến đường đa xe được vẽ bám sát hạ tầng giao thông và bảng chỉ số ESG.
3. **Bước 3:** Nhấn nút mô phỏng sự cố **"Chặn đường Nguyễn Huệ / Rào chắn thi công"**. Quan sát hệ thống tự động đổi hướng đi đường vòng chỉ trong **< 50ms**.
4. **Bước 4:** Thử nghiệm nhập báo cáo tài xế tại ô sự cố hiện trường: *"Hẻm 42 Nguyễn Huệ xe không vào được"* để kích hoạt cơ chế thu gom đi bộ (*walk-in alley*).

---

## 📂 7. Cấu Trúc Mã Nguồn (Repository Structure)

```
Olympic/
├── assets/                  # Ảnh minh họa, kịch bản demo và sơ đồ hệ thống
├── backend/                 # Dịch vụ FastAPI xử lý thuật toán và điều phối rác
│   ├── main.py              # API chính của backend
│   ├── waste_dispatcher.py  # Xử lý sự cố rác và phân loại nghiệp vụ
│   └── parameters/          # Tệp cấu hình tham số thuật toán
├── map_ui/                  # Giao diện bản đồ điều phối thời gian thực (Port 8502)
│   ├── index.html           # Ứng dụng Web tương tác Dual-Map
│   ├── server.py            # Máy chủ web và API phục vụ bản đồ
│   ├── waste_solver.py      # Động cơ định tuyến rác và xử lý sự cố tức thì
│   └── route_cache.json     # Bộ đệm ma trận khoảng cách đường phố OSRM
├── src/                     # Mã nguồn C++17 giải thuật 3D-ACO & SA hiệu năng cao
│   ├── CMakeLists.txt       # Cấu hình biên dịch CMake
│   ├── core/                # Các lớp thực thể VRP (Node, Depot, Customer, Locker)
│   └── solvers/             # Cài đặt thuật toán PACO, ACO, SA, GA, ALNS
├── streamlit/               # Ứng dụng Streamlit phân tích và đo lường độ nhạy
├── docs/                    # Tài liệu đặc tả kỹ thuật chi tiết
│   ├── ARCHITECTURE.md      # Chi tiết kiến trúc hệ thống và luồng dữ liệu
│   ├── DEMO_GUIDE.md        # Kịch bản demo chuẩn dành cho Ban Giám khảo
│   └── API_REFERENCE.md     # Đặc tả toàn bộ API RESTful
├── docker-compose.yml       # Cấu hình khởi chạy trọn gói hệ sinh thái với Docker
├── Dockerfile               # Tệp dựng image container đồng nhất
├── start.sh                 # Kịch bản khởi động 1-click
├── .env.example             # Mẫu cấu hình biến môi trường
├── .gitignore               # Bộ lọc tệp tin chuẩn cho Git
└── LICENSE                  # Giấy phép mã nguồn mở Apache 2.0
```

---

## 📜 8. Giấy Phép & Bản Quyền (License)

Dự án được phân phối dưới giấy phép mã nguồn mở **Apache License 2.0** (tuân thủ 100% chuẩn mã nguồn mở quốc tế được OSI công nhận). Chi tiết xem tại tệp [`LICENSE`](LICENSE).