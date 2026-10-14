# 🏛️ DX-OS Open-Core: Hệ Điều Hành Chuyển Đổi Số Lõi Mở
### Ứng Dụng Thực Chứng Trong Quản Trị Đô Thị Thông Minh & Điều Phối Tuyến Thu Gom Rác
> **BÀI THI OLYMPIC TIN HỌC SINH VIÊN VIỆT NAM 2026 — KHỐI PHẦN MỀM NGUỒN MỞ (VFOSSA)**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![OLP 2026 Standard](https://img.shields.io/badge/Competition-OLP%202026%20PMNM%20Standard-brightgreen.svg)](docs/ARCHITECTURE.md)
[![Architecture: 3--Tier DX--OS](https://img.shields.io/badge/Architecture-3--Tier%20DX--OS-purple.svg)](docs/ARCHITECTURE.md)
[![Model: HPDI Framework](https://img.shields.io/badge/Model-H--P--D--I%20Evolution-orange.svg)](docs/HPDI_SPECIFICATION.md)
[![Docker Ready](https://img.shields.io/badge/Docker-1--Click%20Deploy-2496ED.svg)](docker-compose.yml)
[![Map Sovereignty](https://img.shields.io/badge/Map_Sovereignty-100%25_Vietnam_Compliant-red.svg)](#-4-tuân-thủ-quy-chuẩn-bản-đồ--chủ-quyền-lãnh-thổ)

---

## 📌 1. Giới Thiệu & Đặt Vấn Đề (Executive Summary)

Dự án được xây dựng bám sát 100% yêu cầu của **Đề thi Phần mềm nguồn mở - OLP 2026: "Xây dựng Hệ điều hành Chuyển đổi số bằng Công nghệ Lõi nguồn mở (DX-OS Open-Core)"** do Hội Tin học Việt Nam và Câu lạc bộ Phần mềm Tự do Nguồn mở Việt Nam (VFOSSA) chủ trì:

1. **Khắc phục triệt để hai thái cực sai lầm trong chuyển đổi số:** Loại bỏ tư duy mua sắm phần mềm rời rạc tạo ra các "ốc đảo dữ liệu", đồng thời tránh bẫy phụ thuộc vào hệ thống nguyên khối (monolithic) đóng gây mất chủ quyền số.
2. **Hiện thực hóa Mô hình Tháp 3 Tầng DX-OS:** Phân tách rạch ròi giữa **Tầng 1 - Nền tảng Dịch vụ Lõi số (Headless PaaS)** chạy ngầm, **Tầng 2 - Không gian Năng lực số (Khung H-P-D-I)**, và **Tầng 3 - Ứng dụng Kinh doanh số (Business Applications)**.
3. **Bài toán thực chứng đột phá (Showcase Use Case):** Triển khai ứng dụng **Quản trị Vận tải & Điều phối Đội xe Thu gom Rác Đô thị Thông minh (Smart City Waste TMS)**, giải quyết bài toán giao thông ngõ hẻm phức tạp, rào chắn thi công đột xuất và tối ưu hóa chỉ số xanh môi trường (ESG).

![Demo Hệ Thống](assets/demo.gif)

---

## 🏗️ 2. Sơ Đồ Kiến Trúc Tháp 3 Tầng (3-Tier DX-OS)

```mermaid
flowchart TD
    classDef t1 fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef t2 fill:#1e1b4b,stroke:#8b5cf6,stroke-width:2px,color:#f8fafc;
    classDef t3 fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#f8fafc;

    subgraph Tier3 ["TẦNG 3: NỀN TẢNG KINH DOANH SỐ (Business Applications)"]
        TMS["Quản Lý Vận Tải Giao Nhận & Thu Gom (Smart Waste TMS)"]:::t3
        SmartCity["Hạ Tầng Đô Thị Thông Minh (Smart City IoT Integration)"]:::t3
    end

    subgraph Tier2 ["TẦNG 2: KHÔNG GIAN NĂNG LỰC SỐ (Khung H - P - D - I)"]
        H_Space["<b>[H] Human:</b> Web Mobile Tracker cho Tài xế, SOS, Voice/Text Report"]:::t2
        P_Space["<b>[P] Process:</b> Chuẩn hóa Quy trình Thu gom (SOP), Tự động San tải Xe hỏng"]:::t2
        D_Space["<b>[D] Data:</b> Trung tâm WebGIS (Dual-Map), Bản sao số, Chỉ số Xanh ESG & CO2"]:::t2
        I_Space["<b>[I] Intelligence:</b> Kev AI NLP Agent + C++17 3D-ACO Solver (< 50ms)"]:::t2
    end

    subgraph Tier1 ["TẦNG 1: NỀN TẢNG DỊCH VỤ LÕI SỐ (Headless Open-Core PaaS)"]
        Gateway["Cổng API Gateway & Kiểm soát Biên mạng (Zero-Trust Nginx Proxy)"]:::t1
        Auth["Định danh & Phân quyền Tập trung (SSO / JWT / RBAC Engine)"]:::t1
        SpatialDB["Quản trị Dữ liệu Không gian & Giao dịch (PostgreSQL + PostGIS)"]:::t1
        Workflow["Động cơ Luồng Công việc & Tự động hóa Sự kiện (Async Event Bus)"]:::t1
        Cache["Bộ Đệm Dữ liệu Giao thông Tốc độ Cao (OSRM Routing Matrix Cache)"]:::t1
    end

    TMS <--> Tier2
    SmartCity <--> Tier2
    Tier2 <--> Gateway
    Gateway --> Auth
    Gateway --> SpatialDB
    Gateway --> Workflow
    Gateway --> Cache
```

---

## 🧬 3. Ánh Xạ Chuỗi Tiến Hóa Quản Trị Số H - P - D - I

| Không Gian Số | Đặc Tả Kỹ Thuật Theo Đề Bài OLP 2026 | Hiện Thực Trong Sản Phẩm Dự Thi |
|:---:|---|---|
| **[H] Human** <br/>*(Con người số)* | Khởi tạo môi trường số kết nối nhân lực, cung cấp công cụ cộng tác, ứng dụng di động tác nghiệp hiện trường | **Web Mobile Tracker:** Ứng dụng chạy trực tiếp trên trình duyệt mọi điện thoại; tự động đồng bộ GPS vệ tinh; gửi báo cáo hiện trường bằng giọng nói/văn bản; nút SOS khẩn cấp. |
| **[P] Process** <br/>*(Quy trình số)* | Chuẩn hóa luồng quy trình nghiệp vụ (SOP), thiết lập rào chắn kỹ thuật ngăn ngừa sai sót, tự động hóa xử lý ngoại lệ | **SOP Thu gom & Tự động Phản ứng Sự cố:** Phát hiện đường cấm/ngập nước $\rightarrow$ tự động tìm đường vòng trong `< 50ms`; xe hỏng động cơ $\rightarrow$ tự động san sẻ tải sang các xe lân cận. |
| **[D] Data** <br/>*(Dữ liệu số)* | Quản trị dựa trên dữ liệu thực chứng; Trung tâm điều hành thông minh (IOC); Cổng thông tin địa lý WebGIS; Đo lường ESG | **Trung tâm Điều hành WebGIS Bản Đồ Kép (Dual-Map):** Hiển thị bản sao số (Digital Twin) đội xe và bô rác thời gian thực; bảng đo lường số kg $\text{CO}_2$ cắt giảm và quãng đường tiết kiệm. |
| **[I] Intelligence** <br/>*(Trí tuệ số)* | Tác tử thông minh (AI Agents), xử lý ngôn ngữ tự nhiên, tự động hóa suy luận và ra quyết định thích ứng liên tục | **Kev AI NLP Agent + C++17 3D-ACO Solver:** Tự động đọc hiểu báo cáo hiện trường của tài xế để chuyển chế độ "đi bộ vào hẻm sâu"; thuật toán bầy đàn song song giải định tuyến siêu tốc. |

---

## 🇻🇳 4. Tuân Thủ Quy Chuẩn Bản Đồ & Chủ Quyền Lãnh Thổ

> [!IMPORTANT]
> Dự án tuân thủ nghiêm ngặt quy định pháp luật Việt Nam và Quy chế cuộc thi Olympic:
> - **100% Tuyệt đối không sử dụng bất kỳ nguồn bản đồ nào chứa "đường lưỡi bò" (đường 9 đoạn phi pháp)**.
> - Tích hợp lớp bản đồ chuẩn quốc tế: **OpenStreetMap Tile Server** và **ArcGIS World Imagery** chất lượng cao.
> - Dữ liệu thực nghiệm tập trung tại các phường thuộc **Quận 1, Quận 3, TP. Hồ Chí Minh** với đầy đủ tên đường phố và địa danh tiếng Việt chính thống.

---

## 🚀 5. Hướng Dẫn Khởi Động Nhanh (1-Click Launch)

### Yêu Cầu Tiên Quyết:
* Đã cài đặt **Docker** và **Docker Compose**.

### Lệnh Khởi Động Duy Nhất (Dành cho Ban Giám Khảo):
```bash
docker compose up -d --build
```

Sau khi hệ thống khởi động hoàn tất, truy cập các cổng dịch vụ:
* 🗺️ **Trung tâm Điều hành WebGIS IOC (Trọng tâm chấm thi):** [http://localhost:8502](http://localhost:8502)
* 📊 **Bảng Phân Tích & Nghiên Cứu Thuật Toán (Streamlit BI):** [http://localhost:8501](http://localhost:8501)
* 🔌 **Tài Liệu API Gateway & Solver Core (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* 🗄️ **Cơ Sở Dữ Liệu Không Gian PostGIS:** Cổng `5432` (`dx_admin` / `dx_os_db`)

Để dừng hệ thống:
```bash
docker compose down
```

---

## ⏱️ 6. Kịch Bản 15 Phút Trình Diễn Trước Ban Giám Khảo

*Chi tiết kịch bản từng phút xem tại [docs/JUDGE_DEMO_GUIDE.md](docs/JUDGE_DEMO_GUIDE.md)*

1. **Phút 01 - 03:** Giới thiệu Kiến trúc Tháp 3 tầng DX-OS Open-Core và ánh xạ 4 không gian H-P-D-I.
2. **Phút 04 - 05:** Khởi động 1-click Docker và giới thiệu các cổng dịch vụ Tầng 1 PaaS.
3. **Phút 06 - 12 (Live Demo Trực Tiếp tại [http://localhost:8502](http://localhost:8502)):**
   - **Thao tác 1:** Chế độ Bản Đồ Kép (Dual Map) — so sánh lộ trình tối ưu 3D-ACO với thuật toán Baseline.
   - **Thao tác 2:** Mô phỏng sự cố rào chắn công trình — hệ thống tính đường vòng tức thì trong `< 50ms`.
   - **Thao tác 3:** Báo cáo tài xế qua giọng nói/text — Tác tử Kev AI nhận diện sự cố hẻm hẹp và kích hoạt cơ chế thu gom đi bộ.
   - **Thao tác 4:** Kiểm tra bảng chỉ số xanh môi trường (cắt giảm phát thải $\text{CO}_2$ và tiết kiệm 25-35% quãng đường).
4. **Phút 13 - 15:** Trình bày kết quả đo lường thực nghiệm (Benchmark) và trả lời phản biện của Ban Giám khảo.

---

## 📂 7. Cấu Trúc Mã Nguồn (Repository Structure)

```
Olympic/
├── core-platform/                         # TẦNG 1: NỀN TẢNG DỊCH VỤ LÕI SỐ (Headless PaaS)
│   ├── gateway/                           # Cấu hình API Gateway & Reverse Proxy (Nginx)
│   ├── auth/                              # Quản trị định danh & phân quyền (JWT / RBAC)
│   ├── database/                          # Cấu trúc CSDL Không gian (PostgreSQL + PostGIS init.sql)
│   └── workflow/                          # Động cơ luồng công việc & Event Bus bất đồng bộ
│
├── apps/                                  # TẦNG 2 & 3: ỨNG DỤNG THỰC CHỨNG (Civic-Tech Waste TMS)
│   ├── map_dispatcher/                    # Trung tâm Điều hành WebGIS IOC (Port 8502 - Dual Map)
│   │   ├── index.html                     # Giao diện bản đồ tương tác thời gian thực
│   │   ├── server.py                      # Máy chủ điều phối & API xử lý sự cố
│   │   ├── waste_solver.py                # Động cơ giải thuật định tuyến & tái định tuyến < 50ms
│   │   └── route_cache.json               # Bộ đệm ma trận khoảng cách mạng lưới giao thông OSRM
│   ├── solver_core/                       # Thuật toán tối ưu hóa bầy đàn song song 3 chiều (C++17)
│   │   ├── CMakeLists.txt                 # Cấu hình biên dịch CMake
│   │   ├── core/                          # Các lớp mô hình đối tượng VRP
│   │   └── solvers/                       # Cài đặt thuật toán PACO, ACO, SA, ALNS
│   ├── analytics/                         # Bảng điều khiển phân tích & nghiên cứu tham số (Port 8501)
│   └── backend_service/                   # Dịch vụ API backend phụ trợ
│
├── docs/                                  # HỆ THỐNG TÀI LIỆU CHUẨN THI ĐẤU OLP 2026
│   ├── ARCHITECTURE.md                    # Đặc tả chi tiết Khung Kiến trúc Tháp 3 Tầng
│   ├── HPDI_SPECIFICATION.md              # Phân rã kỹ thuật 4 không gian số H - P - D - I
│   ├── JUDGE_DEMO_GUIDE.md                # Kịch bản 15 phút trình diễn trước Ban Giám khảo
│   ├── API_REFERENCE.md                   # Đặc tả toàn bộ RESTful API & WebSocket
│   └── CHECKLIST.md                       # Bảng kiểm tra 15 mục trước giờ nộp bài cho BTC
│
├── assets/                                # Ảnh kiến trúc, demo GIF và video minh họa
├── docker-compose.yml                     # Khởi chạy toàn bộ hệ sinh thái bằng 1 lệnh duy nhất
├── Dockerfile                             # Đóng gói môi trường container độc lập
├── start.sh                               # Script chạy nhanh tự động
├── .env.example                           # Mẫu cấu hình biến môi trường
├── .gitignore                             # Bộ lọc loại bỏ tệp tin rác
└── LICENSE                                # Giấy phép mã nguồn mở Apache 2.0 (OSI-approved)
```

---

## 📧 8. Mẫu Thư Gửi Bài Thi (Theo Mục 5 Đề Thi OLP 2026)

* **Tiêu đề thư:** `BÀI THI PMNM 2026 - [Tên Đội] - [Tên Trường]`
* **Địa chỉ nhận bài:** `olpvietnam@vaip.vn`, `thuky@vfossa.vn`
* **Nội dung:**
  > Kính gửi BTC cuộc thi PMNM 2026,  
  > Đội thi **[Tên Đội]** - **[Tên Trường]** đã hoàn thành bài thi và xin gửi BTC kết quả như sau:  
  > **Thành viên đội:**  
  > 1. [Tên thành viên 1, năm sinh, ngành đào tạo]  
  > 2. [Tên thành viên 2, năm sinh, ngành đào tạo]  
  > 3. [Tên thành viên 3, năm sinh, ngành đào tạo]  
  > **Người hướng dẫn:** [Tên Thầy/Cô - Khoa/Viện/Trường]  
  > **Kho mã nguồn dự thi:** `https://github.com/congnghip/Olympic`  
  > Đội thi đã hoàn thành việc đăng kí dự thi theo đúng quy định của BTC thông qua [Tên Trường]. Chúng tôi cam kết toàn bộ bản quyền sử dụng đối với sản phẩm dự thi tuân thủ theo đúng các quy tắc của phần mềm tự do nguồn mở (Apache License 2.0).

---

## 📜 9. Giấy Phép & Bản Quyền (License)

Dự án được phân phối dưới giấy phép mã nguồn mở **Apache License 2.0** (tuân thủ 100% chuẩn mã nguồn mở quốc tế được OSI công nhận). Chi tiết xem tại tệp [`LICENSE`](LICENSE).