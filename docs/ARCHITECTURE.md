# Đặc Tả Kiến Trúc Hệ Thống: DX-OS Open-Core

DX-OS Open-Core là nền tảng hệ điều hành chuyển đổi số theo kiến trúc lõi mở (Open-Core Architecture), áp dụng nguyên tắc phân tách mối quan tâm (Separation of Concerns) thành mô hình tháp 3 tầng.

---

## 1. Sơ Đồ Kiến Trúc Tháp 3 Tầng

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
        H_Space["<b>[H] Human:</b> Web Mobile Tracker cho Tài xế, SOS, Báo Cáo Hiện Trường"]:::t2
        P_Space["<b>[P] Process:</b> Chuẩn hóa Luồng Thu Gom (SOP), Tự Động San Tải Xe Hỏng"]:::t2
        D_Space["<b>[D] Data:</b> Trung Tâm WebGIS (Dual-Map), Bản Sao Số, Chỉ Số Xanh ESG & CO2"]:::t2
        I_Space["<b>[I] Intelligence:</b> NLP Agent + Bộ Giải C++17 3D-ACO (< 50ms)"]:::t2
    end

    subgraph Tier1 ["TẦNG 1: NỀN TẢNG DỊCH VỤ LÕI SỐ (Headless Open-Core PaaS)"]
        Gateway["Cổng API Gateway & Kiểm Soát Biên Mạng (Reverse Proxy)"]:::t1
        Auth["Định Danh & Phân Quyền Tập Trung (JWT / RBAC Engine)"]:::t1
        SpatialDB["Quản Trị Dữ Liệu Không Gian & Giao Dịch (PostgreSQL + PostGIS)"]:::t1
        Workflow["Động Cơ Luồng Sự Kiện Bất Đồng Bộ (Async Event Bus)"]:::t1
        Cache["Bộ Đệm Đồ Thị Mạng Lưới Giao Thông (OSRM Routing Matrix Cache)"]:::t1
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

## 2. Chi Tiết Phân Tầng Kỹ Thuật

### Tầng 1: Nền tảng Dịch vụ Lõi số (Headless Open-Core PaaS)
Vận hành hoàn toàn ngầm không giao diện (headless), trừu tượng hóa hạ tầng kỹ thuật và cung cấp các dịch vụ dùng chung qua API:
1. **API Gateway & Biên mạng:** Kiểm soát truy cập tập trung, phân luồng request tới các dịch vụ backend, hỗ trợ WebSocket truyền phát thời gian thực.
2. **Định danh & Phân quyền (Identity & RBAC):** Cung cấp cơ chế xác thực JWT, bảo vệ thông tin định danh và phân quyền theo vai trò (`ADMIN`, `OPERATOR`, `DRIVER`).
3. **Cơ sở dữ liệu Không gian (Spatial Database):** Sử dụng PostgreSQL tích hợp PostGIS, quản lý các thực thể địa lý (trạm trung chuyển, bô rác, vết di chuyển GPS) trên hệ quy chiếu WGS84 (SRID 4326).
4. **Động cơ Sự kiện & Luồng nghiệp vụ (Event Bus & Workflow):** Cơ chế Publish/Subscribe bất đồng bộ để tiếp nhận và điều phối các sự kiện hiện trường (tắc đường, sự cố kỹ thuật xe, thùng rác quá tải).
5. **Bộ đệm Đồ thị Giao thông (Routing Matrix Cache):** Tiền tính toán và lưu đệm ma trận khoảng cách OSRM giúp giảm tải truy vấn lặp lại và đảm bảo thời gian phản hồi định tuyến `< 50ms`.

---

### Tầng 2: Không gian Năng lực Quản trị số (Khung H-P-D-I)
Cung cấp giao diện tương tác và nghiệp vụ số hóa theo 4 không gian năng lực:
* **[H] Human (Con người số):** Web Mobile Tracker cho lực lượng hiện trường; hỗ trợ cập nhật trạng thái GPS, gửi báo cáo hiện trường bằng giọng nói/văn bản và phát tín hiệu SOS khẩn cấp.
* **[P] Process (Quy trình số):** Chuẩn hóa quy trình thu gom thường kỳ (SOP) và quy trình tự động hóa phản ứng sự cố: tự động định tuyến đường vòng khi gặp rào chắn, tự động san tải thùng rác khi xe gặp sự cố động cơ.
* **[D] Data (Dữ liệu số):** Trung tâm điều hành thông minh (IOC) với giao diện WebGIS Bản Đồ Kép (Dual-Map); cập nhật bản sao số (Digital Twin) theo thời gian thực; tính toán các chỉ số môi trường (quãng đường tiết kiệm, phát thải $\text{CO}_2$ cắt giảm, tỷ lệ tối ưu tải trọng).
* **[I] Intelligence (Trí tuệ số):** Tác tử NLP phân tích báo cáo tài xế để nhận diện trở ngại; tích hợp động cơ giải thuật bầy đàn 3 chiều (3D-Parallel Ant Colony Optimization - 3D-ACO) viết bằng C++17 giải bài toán định tuyến phương tiện đa điểm (VRP).

---

### Tầng 3: Nền tảng Ứng dụng Nghiệp vụ (Business Applications)
Phân hệ ứng dụng thực chiến trong lĩnh vực Quản lý Vận tải Giao nhận (TMS) và Đô thị Thông minh (Smart City IoT), giải quyết bài toán điều phối tuyến xe thu gom rác tại các khu vực đô thị có mật độ ngõ hẻm cao.
