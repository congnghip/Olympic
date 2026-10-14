# 🏛️ Kiến Trúc Hệ Điều Hành Chuyển Đổi Số: DX-OS Open-Core
### (Open-Source Digital Transformation Operating System - OLP 2026)

Tài liệu đặc tả kiến trúc kỹ thuật của hệ thống dự thi **Olympic Tin học Sinh viên Việt Nam 2026 (Khối Phần mềm Nguồn mở - VFOSSA)**. Hệ thống được xây dựng bám sát 100% Khung Kiến trúc 3 Tầng theo đề bài của Ban Tổ Chức.

---

## 🏗️ 1. Sơ Đồ Kiến Trúc Tháp 3 Tầng (3-Tier DX-OS Architecture)

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

    %% Tầng 3 kết nối Tầng 2
    TMS <--> Tier2
    SmartCity <--> Tier2

    %% Tầng 2 kết nối Tầng 1
    Tier2 <--> Gateway
    Gateway --> Auth
    Gateway --> SpatialDB
    Gateway --> Workflow
    Gateway --> Cache
```

---

## 🧩 2. Chi Tiết Các Tầng Kỹ Thuật

### Tầng 1: Nền tảng Dịch vụ Lõi số (Headless Open-Core PaaS)
Hoạt động hoàn toàn ngầm không giao diện (Headless PaaS), cung cấp các dịch vụ dùng chung nền móng:
1. **API Gateway & Biên mạng:** Kiểm soát truy cập tập trung, phân luồng lưu lượng tới các microservices.
2. **Định danh & Bảo mật (Identity/SSO):** Cung cấp cơ chế xác thực JWT, bảo vệ thông tin cá nhân và phân quyền theo vai trò (Admin, Điều phối viên, Tài xế, Giám sát).
3. **Cơ sở dữ liệu Không gian (Spatial OLTP):** PostgreSQL tích hợp phần mở rộng **PostGIS** lưu trữ dữ liệu địa lý (tọa độ trạm trung chuyển, vị trí bô rác, vết di chuyển GPS của đội xe).
4. **Động cơ luồng công việc & Sự kiện (Workflow & Event Bus):** Đón nhận các sự kiện thời gian thực (rào chắn, xe hỏng, thùng rác đầy) và tự động kích hoạt tiến trình xử lý ngầm.
5. **Bộ đệm đồ thị OSRM:** Lưu trữ ma trận khoảng cách thực tế giữa các nút giao thông, phục vụ tính toán định tuyến tức thời.

---

### Tầng 2: Không gian Năng lực Quản trị số H-P-D-I
Lớp đệm chuyển giao năng lực quản trị theo mô hình trưởng thành số:
* **[H] Human (Con người số):** Ứng dụng di động tác nghiệp hiện trường không cần cài đặt (Web Mobile Tracker), hỗ trợ tài xế nhận lộ trình, gửi báo cáo sự cố bằng giọng nói/chữ viết và nút SOS khẩn cấp.
* **[P] Process (Quy trình số):** Số hóa quy trình thu gom thường kỳ và quy trình xử lý ngoại lệ tự động (tránh đường cấm, phân bổ lại thùng rác của xe bị hỏng).
* **[D] Data (Dữ liệu số):** Trung tâm điều hành thông minh (IOC) với chế độ **Bản đồ Kép (Dual-Map)**, hiển thị bản sao số (Digital Twin) của toàn bộ mạng lưới thu gom và bảng đồng hồ đo lường phát thải $\text{CO}_2$, năng lượng và chi phí vận hành (ESG).
* **[I] Intelligence (Trí tuệ số):** Tích hợp Tác tử thông minh **Kev AI** phân loại ngữ nghĩa báo cáo hiện trường và Động cơ giải thuật tối ưu bầy đàn **3D-ACO** phát triển bằng C++17 cho tốc độ giải bài toán định tuyến trong `< 50ms`.

---

### Tầng 3: Ứng dụng Thực chứng Quản trị Đô thị Thông minh (Smart City Waste TMS)
* Ứng dụng chuyên ngành Quản lý vận tải giao nhận (TMS) và Hạ tầng đô thị thông minh (Smart City IoT), giải quyết bài toán môi trường và giao thông nhức nhối tại các đại đô thị Việt Nam.
