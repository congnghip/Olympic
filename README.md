# DX-OS OPEN-CORE: CDE & AI-POWERED CONSTRUCTION APPRAISAL PLATFORM
### Hệ điều hành Chuyển đổi số DX-OS Open-Core phục vụ Môi trường Dữ liệu Chung (CDE) và Thẩm định Tự động Hồ sơ Xây dựng
**Đề tài tham dự:** Olympic Tin học Sinh viên Việt Nam 2026 — Khối Phần mềm Nguồn Mở (PMNM)  
**Đơn vị chủ trì chuyên môn:** Hội Tin học Việt Nam (VAIP) & CLB Phần mềm Tự do Nguồn mở Việt Nam (VFOSSA)

---

## 📌 1. TỔNG QUAN HỆ THỐNG
Dự án được xây dựng dựa trên Khung Kiến trúc Hệ điều hành Chuyển đổi số **DX-OS Open-Core (3 Tầng)** theo đúng quy chuẩn đề thi OLP 2026, tích hợp giải pháp **Môi trường Dữ liệu Chung (CDE)** và **Tác tử AI Đa phương thức (Multimodal AI Agent)** nhằm tự động hóa quy trình thẩm định hồ sơ xây dựng và lập kế hoạch sửa đổi cho người nộp theo **Điều 102 Luật Xây dựng**.

```
🏛️ TẦNG 3: NỀN TẢNG KINH DOANH SỐ (ỨNG DỤNG NGHIỆP VỤ - WEB PORTAL)
   ├── Cổng Kỹ sư / Doanh nghiệp: Nộp bản vẽ, xem highlight lỗi trực quan, nhận To-do Action Plan
   └── Cổng Cán bộ Thẩm định: Rà soát danh sách hồ sơ, xem báo cáo đối soát Diff V1 vs V2, phê duyệt

🧠 TẦNG 2: KHÔNG GIAN NĂNG LỰC SỐ (H - P - D - I)
   ├── [H] Con người số: Đồng bộ phiên Keycloak SSO, thông báo Telegram/Email
   ├── [P] Quy trình số: Quản lý vòng đời trạng thái hồ sơ (State Machine)
   ├── [D] Dữ liệu số: Lập chỉ mục không gian bản vẽ & quản lý phả hệ phiên bản
   └── [I] Trí tuệ số (AI Agent Core):
       ├── Docling Parser: Bóc tách văn bản công văn hành chính có dấu đỏ
       ├── Drawing Grounding Engine: Ánh xạ lỗi và tính toán Bounding Box tọa độ bản vẽ
       ├── Action Plan Builder: Tự động biên soạn danh sách hành động sửa chữa
       └── Diffing Engine: Tự động so sánh sai lệch giữa bản vẽ nộp lại V2 và bản cũ V1

⚙️ TẦNG 1: NỀN TẢNG DỊCH VỤ LÕI SỐ (DX-OS OPEN-CORE - HEADLESS PaaS)
   ├── API Gateway: Apache APISIX / Traefik (Định tuyến, bảo mật Zero-Trust, Rate-Limit)
   ├── Backend Services: FastAPI (Python 3.11 Microservices)
   ├── MCP Server: Cung cấp Tools/Resources chuẩn Model Context Protocol cho AI
   ├── Identity & SSO: Keycloak / Authentik (Chuẩn OIDC/OAuth2)
   ├── Workflow Engine: Flowable BPMN 2.0 (Quản lý luồng phê duyệt & SLA)
   ├── Structured Data: PostgreSQL 16 (Lưu trữ Metadata, Hồ sơ, Tọa độ lỗi)
   ├── Object Storage: MinIO S3 (Lưu trữ file lớn: PDF bản vẽ khổ A0/A1, file CAD)
   └── OpenBIM Engine: xeokit / web-ifc / ezdxf (Dựng hình & bóc tách CAD/BIM nguồn mở)
```

---

## 📂 2. CẤU TRÚC THƯ MỤC DỰ ÁN

```bash
Olympic/
├── BRD.md                     # Tài liệu Yêu cầu Nghiệp vụ (Business Requirements Document)
├── SRS.md                     # Đặc tả Yêu cầu Kỹ thuật Phần mềm (Software Requirements Spec)
├── README.md                  # Hướng dẫn kiến trúc và vận hành hệ thống
├── docker-compose.yml         # Triển khai đồng bộ 3 tầng dịch vụ bằng Docker
├── Makefile                   # Các lệnh điều khiển nhanh hệ thống (make up, make down)
├── .env.example               # Mẫu cấu hình các biến môi trường
│
├── deploy/
│   └── init-db/
│       └── 01-init-schema.sql # Script khởi tạo cơ sở dữ liệu PostgreSQL chuẩn ERD
│
├── backend/                   # Tầng 1 & 2: Backend REST API & MCP Server (FastAPI)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py            # Entrypoint FastAPI, CORS, Routers
│       ├── core/              # Cấu hình biến môi trường & kết nối CSDL bất đồng bộ
│       ├── models/            # SQLAlchemy ORM Models (Dossier, Drawing, Notice, Issue)
│       ├── schemas/           # Pydantic Schemas cho Request/Response
│       ├── mcp/               # Model Context Protocol Server (Tools & Resources)
│       ├── api/v1/            # Các REST API: Dossiers, Notices, AI Appraisal, Diff
│       └── services/          # MinIO Storage, Flowable Workflow, AI Core Engines
│
├── frontend/                  # Tầng 3: Web Portal (Vite + React + Tailwind CSS)
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── App.jsx            # Giao diện tương tác bản vẽ & Action Plan
│       └── main.jsx
│
└── samples/                   # Dữ liệu mẫu phục vụ thử nghiệm & chấm thi
    └── cong_van_yeu_cau_sua_doi.txt # Mẫu công văn thực tế từ Sở Xây dựng
```

---

## 🚀 3. HƯỚNG DẪN KHỞI CHẠY (QUICK START)

### Yêu cầu tiên quyết
* Đã cài đặt **Docker** và **Docker Compose** (hoặc Python 3.11+ và Node.js 20+ nếu chạy cục bộ).

### Cách 1: Khởi chạy toàn bộ hệ thống bằng 1 lệnh duy nhất (Khuyên dùng)
```bash
# Di chuyển vào thư mục dự án
cd /home/congnghiep/nghich/Olympic

# Khởi động toàn bộ cụm container
make up
# hoặc: docker compose up -d --build
```

### Danh mục Cổng dịch vụ (Service Ports)
Sau khi khởi động thành công, bạn có thể truy cập các dịch vụ:
| Dịch vụ | Địa chỉ truy cập | Tài khoản mặc định | Nhiệm vụ |
| :--- | :--- | :--- | :--- |
| **Frontend Web Portal** | `http://localhost:3000` | - | Giao diện tương tác Bản vẽ & Action Plan |
| **Backend Swagger API** | `http://localhost:8000/docs` | - | Tài liệu tra cứu & thử nghiệm REST API |
| **MCP Server Tools** | `http://localhost:8000/mcp/tools` | - | Danh mục Tools chuẩn Model Context Protocol |
| **MinIO S3 Console** | `http://localhost:9001` | `minioadmin` / `minioadmin_secret_2026` | Quản trị file bản vẽ CAD/PDF tải lên |
| **Flowable REST BPMN** | `http://localhost:8090` | `admin` / `test` | Động cơ điều phối luồng quy trình nghiệp vụ |
| **PostgreSQL Database**| `localhost:5432` | `dxos_admin` / `dxos_secret_password_2026` | CSDL quan hệ lưu trữ metadata |

---

### Cách 2: Chạy thử nghiệm Cục bộ từng phần (Development Mode)
```bash
# 1. Chạy Backend FastAPI
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 2. Chạy Frontend Web Portal
cd frontend
npm install
npm run dev
```

---

## 🧪 4. KỊCH BẢN TRÌNH DIỄN (LIVE DEMO WALKTHROUGH)

Khi trình diễn trước Ban Giám khảo OLP 2026:
1. **Bước 1 (Tiếp nhận):** Mở giao diện `http://localhost:3000`, chọn vai trò **Kỹ sư thiết kế**. Xem danh sách hồ sơ mẫu đang có trạng thái *"Cần sửa đổi"*.
2. **Bước 2 (Kích hoạt AI):** Bấm nút **"⚡ Chạy AI Thẩm định lại"**. Tác tử AI đọc công văn mẫu số `458/SXD-QLĐT`, tự động bóc tách 3 vấn đề vi phạm kỹ thuật và ánh xạ tọa độ lên bản vẽ.
3. **Bước 3 (Tương tác Trực quan):** Click vào từng mục trong danh sách **Action Plan**:
   * *Mục 1 (Khoảng lùi phía sau):* Bản vẽ bên phải tự động nhảy đến đúng ranh đất và đóng khung đỏ vi phạm `QCVN 01:2021/BXD`.
   * *Mục 2 (Vế thang bộ):* Bản vẽ phóng to vào vị trí cầu thang trục 2-3 chỉ rõ chiều rộng 1.05m thiếu 150mm theo `QCVN 06:2022/BXD`.
4. **Bước 4 (Đối soát Sai lệch V1 vs V2):** Chuyển sang vai trò **Cán bộ thẩm định**, chuyển sang tab **"🔍 Đối soát Diff V1/V2"**, bấm **Chạy Đối soát**. Hệ thống lập tức báo cáo: *2 mục đã sửa đạt, 1 mục chưa sửa, và phát hiện 1 cảnh báo cơi nới ban công ngoài thẩm quyền*.

---

## 📜 5. CAM KẾT BẢN QUYỀN MÃ NGUỒN MỞ
Toàn bộ mã nguồn và công nghệ sử dụng trong dự án đều tuân thủ các giấy phép nguồn mở được công nhận quốc tế (Apache 2.0, MIT, MPL 2.0). Hệ thống hoàn toàn độc lập, có thể vận hành On-Premise không phụ thuộc vào bất kỳ dịch vụ đám mây thương mại đóng nào.