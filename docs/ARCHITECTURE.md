# Kiến Trúc Hệ Thống: Smart Waste Management & Dynamic Incident Re-routing Platform

Hệ thống được thiết kế theo mô hình vi dịch vụ phân tán (Microservices & Event-Driven Architecture), phục vụ bài toán tối ưu hóa vận tải đô thị xanh, tự động điều phối đội xe gom rác thời gian thực và xử lý sự cố tức thì (*Dynamic Incident Re-routing*).

---

## 🏗️ 1. Sơ Đồ Kiến Trúc Tổng Thể (System Architecture)

```mermaid
flowchart TD
    classDef clientNode fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef serviceNode fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc;
    classDef engineNode fill:#312e81,stroke:#6366f1,stroke-width:2px,color:#f8fafc;
    classDef storageNode fill:#701a75,stroke:#ec4899,stroke-width:2px,color:#f8fafc;

    subgraph PresentationLayer ["Tầng Giao Diện Người Dùng (Presentation Layer)"]
        UI_Map["Bản Đồ Điều Phối Thời Gian Thực<br/><b>Map UI (Port 8502)</b><br/>Leaflet / MapLibre Dual Map"]:::clientNode
        UI_Streamlit["Trung Tâm Phân Tích & Tối Ưu Tham Số<br/><b>Streamlit Dashboard (Port 8501)</b>"]:::clientNode
        DriverApp["Ứng Dụng Thu Gom Hiện Trường<br/><b>Mobile Web Tracker</b> (GPS & Voice/Text)"]:::clientNode
    end

    subgraph GatewayLayer ["Tầng Cổng Giao Tiếp & Điều Phối (API & Dispatching)"]
        FastAPI_Gateway["<b>FastAPI Incident Gateway (Port 8502 / 8000)</b><br/>Xử lý định tuyến, REST API, WebSocket"]:::serviceNode
        IncidentDispatcher["<b>Dynamic Incident Dispatcher</b><br/>Phân loại sự cố & Quyết định giải pháp"]:::serviceNode
    end

    subgraph OptimizationLayer ["Tầng Thuật Toán & Trí Tuệ Nhân Tạo (Engines)"]
        ACO_Core["<b>3D-Parallel ACO Solver Core (C++17)</b><br/>Thuật toán Đàn kiến Tối ưu hóa VRP"]:::engineNode
        DynamicHeuristic["<b>Dynamic Re-routing Heuristic Engine</b><br/>Tìm đường vòng tức thời < 50ms"]:::engineNode
        KevAI["<b>Kev System One AI Engine</b><br/>Phân tích giọng nói & Báo cáo hiện trường"]:::engineNode
        OSRM["<b>OSRM Routing & Street Graph</b><br/>Mạng lưới giao thông thực tế TP.HCM"]:::engineNode
    end

    subgraph PersistenceLayer ["Tầng Dữ Liệu & Bộ Đệm (Storage & Cache)"]
        RouteCache[("<b>High-speed Route Cache</b><br/>(JSON & Memory Precomputed Matrix)")]:::storageNode
        InstanceData[("<b>Benchmark Datasets</b><br/>(Solomon / Real HCMC GeoJSON)")]:::storageNode
    end

    %% Connections
    UI_Map <-->|REST API / JSON| FastAPI_Gateway
    UI_Streamlit <-->|RPC / HTTP| FastAPI_Gateway
    DriverApp -->|Báo cáo sự cố & GPS| FastAPI_Gateway

    FastAPI_Gateway --> IncidentDispatcher
    IncidentDispatcher --> DynamicHeuristic
    IncidentDispatcher --> KevAI
    IncidentDispatcher --> ACO_Core

    DynamicHeuristic <--> RouteCache
    DynamicHeuristic <--> OSRM
    ACO_Core <--> InstanceData
```

---

## ⚙️ 2. Luồng Xử Lý Sự Cố Động (Dynamic Incident Resolution Flow)

Khi phát sinh sự cố trong quá trình xe gom rác di chuyển trên đường phố (ngập úng, rào chắn công trình hẻm nhỏ, xe hư hỏng kỹ thuật hoặc rác thải nguy hại), quy trình điều phối diễn ra như sau:

```mermaid
sequenceDiagram
    autonumber
    actor Driver as Tài xế / Cảm biến hiện trường
    participant UI as Giao diện Giám sát (Map UI)
    participant Server as FastAPI Incident Server
    participant Dispatcher as Waste Dispatcher & AI
    participant Solver as Re-routing Engine (3D-ACO / Heuristics)

    Driver->>Server: Gửi báo cáo sự cố (Voice/Text/Tọa độ GPS)
    Note over Server,Dispatcher: Tiếp nhận sự kiện và trích xuất ngữ cảnh
    Server->>Dispatcher: Phân tích phân loại sự cố (Incident Classification)
    Dispatcher-->>Server: Xác định mức độ khẩn cấp (Urgency Score & Action)
    
    alt Đường bị rào chắn / Sự cố giao thông
        Server->>Solver: Loại bỏ điểm nghẽn, tính đường vòng (Detour Calculation)
        Solver-->>Server: Lộ trình mới đã tránh đoạn đường cấm
    else Xe gặp sự cố kỹ thuật hỏng hóc
        Server->>Solver: Phân bổ lại các điểm gom còn lại sang xe kế cận (Load Transfer)
        Solver-->>Server: Lộ trình tái cấu trúc cho toàn đội xe
    end

    Server-->>UI: Cập nhật lộ trình thời gian thực (< 100ms)
    UI-->>Driver: Hướng dẫn tuyến đường mới trên bản đồ
```

---

## 🗺️ 3. Quy Chuẩn Bản Đồ & Chủ Quyền Lãnh Thổ (Map Sovereignty)

Dự án tuân thủ nghiêm ngặt quy định về chủ quyền lãnh thổ Việt Nam và tiêu chuẩn trình bày bản đồ trong các kỳ thi CNTT cấp quốc gia:
- **100% Tuyệt đối không sử dụng các nguồn bản đồ có đường lưỡi bò (đường 9 đoạn)**.
- Tích hợp lớp bản đồ chuẩn quốc tế:
  - **OpenStreetMap** chính thức qua tile server chuẩn.
  - **ArcGIS World Imagery** vệ tinh độ nét cao.
  - Tùy chọn Google Maps chuẩn với tham số quốc gia Việt Nam (`hl=vi`).
- Dữ liệu điểm tập kết, bô rác và lộ trình lấy mẫu thực nghiệm trực tiếp tại các phường thuộc **Quận 1, Quận 3, TP. Hồ Chí Minh**.

---

## 🌿 4. Mô Hình Đo Lường Môi Trường (ESG & Carbon Emission Model)

Hệ thống tính toán trực tiếp chỉ số xanh và hiệu quả môi trường sau mỗi lần tối ưu:
- **Quãng đường cắt giảm:** $\Delta D = D_{\text{truyền thống}} - D_{\text{tối ưu}}$ (km).
- **Phát thải $\text{CO}_2$ tiết kiệm:** $E = \Delta D \times 0.285 \text{ kg CO}_2/\text{km}$ (hệ số tiêu chuẩn xe tải thu gom đô thị hạng nhẹ).
- **Chi phí nhiên liệu tiết kiệm:** $C = \Delta D \times \text{Định mức tiêu hao} \times \text{Đơn giá nhiên liệu}$.
