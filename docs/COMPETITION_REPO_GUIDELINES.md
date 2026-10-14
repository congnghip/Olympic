# 🏆 Cẩm Nang Quy Chuẩn Trình Bày Repository Dự Thi Olympic & Hackathon
### (Official Guidelines for Competition-Grade Open Source Repositories)

Tài liệu này tổng hợp toàn bộ các tiêu chuẩn, kinh nghiệm thực chiến và thang điểm đánh giá của Ban Giám Khảo (BGK) tại các kỳ thi lớn như:
- **Olympic Tin học Sinh viên Việt Nam (Khối Phần mềm Nguồn mở - VFOSSA)**
- **Các giải thưởng NCKH sinh viên (Euréka, SV-NCKH các cấp)**
- **Các cuộc thi Hackathon, AI Challenge & Sáng tạo Công nghệ Quốc gia**

---

## 📊 1. Ma Trận Thang Điểm Đánh Giá Của Ban Giám Khảo

Khi BGK mở link GitHub của đội thi, họ chấm điểm dựa trên 5 trụ cột cốt lõi:

| Trụ Cột Đánh Giá | Tỷ Trọng | Trọng Tâm Giám Khảo Xem Xét |
|---|:---:|---|
| **1. Khả năng tái lập & Đóng gói (Reproducibility & 1-Click Launch)** | **30%** | Có chạy được ngay bằng `docker compose up` không? Có script cài đặt tự động không? Hay báo lỗi thiếu thư viện/môi trường? |
| **2. Kiến trúc & Chất lượng Mã nguồn (Architecture & Code Quality)** | **25%** | Cấu trúc thư mục mạch lạc, phân tách rõ Frontend - Backend - Core Logic; mã nguồn sạch, có chú thích, tuân thủ linter |
| **3. Tài liệu kỹ thuật & Trình bày (README & Documentation)** | **20%** | README trực quan, có sơ đồ Mermaid, có demo GIF/video, kịch bản demo rõ ràng từng bước cho BGK thao tác thử |
| **4. Tính giải quyết vấn đề & Sáng tạo (Practical Impact & Innovation)** | **15%** | Đề tài giải quyết được nút thắt thực tế nào? Có kết quả đo lường định lượng (Benchmark, so sánh baseline) không? |
| **5. Chuẩn Mã nguồn mở & Lịch sử Git (OSS Compliance & Git Flow)** | **10%** | Có giấy phép OSI-Approved (`LICENSE`), lịch sử commit thể hiện sự đóng góp đều đặn của các thành viên trong nhóm |

---

## 📁 2. Cấu Trúc Thư Mục Tiêu Chuẩn (Standard Folder Structure)

Một repository đạt giải cao luôn tuân theo bố cục chuẩn sau:

```
ten-du-an/
├── assets/                  # Ảnh chụp màn hình, ảnh kiến trúc, video demo, GIF demo
├── docs/                    # Tài liệu chuyên sâu (Kiến trúc, API, Kịch bản chấm thi)
│   ├── ARCHITECTURE.md      # Chi tiết kiến trúc hệ thống và luồng dữ liệu
│   ├── DEMO_GUIDE.md        # Kịch bản từng bước để BGK thao tác và chấm thi
│   └── API_REFERENCE.md     # Đặc tả API (Swagger / OpenAPI / Postman collection)
├── backend/                 # Mã nguồn dịch vụ backend (FastAPI, Go, Node.js...)
├── frontend/                # Mã nguồn giao diện người dùng (React, Vue, Streamlit...)
├── core/ hoặc src/          # Thuật toán lõi (AI model, solver C++, optimization...)
├── tests/                   # Kiểm thử tự động (Unit tests, Integration tests)
├── .env.example             # Mẫu cấu hình biến môi trường (KHÔNG CHỨA KEY THẬT)
├── .gitignore               # Bộ lọc loại bỏ file rác, file tạm, cache, credentials
├── docker-compose.yml       # Khởi chạy toàn bộ hệ thống bằng 1 lệnh duy nhất
├── Dockerfile               # Đóng gói môi trường container độc lập
├── start.sh                 # Script chạy nhanh dành cho Linux / macOS
├── LICENSE                  # Giấy phép mã nguồn mở bắt buộc (Apache 2.0 / MIT / GPLv3)
└── README.md                # Bộ mặt chính của đề tài (Quyết định 80% ấn tượng ban đầu)
```

---

## ✍️ 3. Quy Tắc "Vàng" Khi Thiết Kế `README.md`

Ban Giám khảo chỉ dành **từ 2 đến 3 phút** để lướt qua README trước khi chấm. Để ghi điểm tối đa, README cần tuân thủ cấu trúc 8 phần:

### 1. Header & Badges (Huy hiệu nhận diện)
* Đặt tên đề tài rõ ràng, kèm slogan định vị sản phẩm.
* Sử dụng shields.io badges: License, Ngôn ngữ, Framework, Trạng thái Docker, Trạng thái CI/CD.

### 2. Bối Cảnh & Đóng Góp (Problem Statement & Value Proposition)
* Nêu ngắn gọn 2 - 3 khó khăn thực tế mà sản phẩm giải quyết.
* Bảng tóm tắt các tính năng nổi bật và lợi ích mang lại.

### 3. Hình Ảnh / Demo Trực Quan (Hero Banner / Demo GIF)
* **Bắt buộc phải có ít nhất 1 ảnh động GIF hoặc video ngắn (1 - 2 phút)** minh họa sản phẩm đang chạy thật. Tránh repo chỉ toàn chữ khô khan.

### 4. Sơ Đồ Kiến Trúc Hệ Thống (Architecture Diagram)
* Vẽ bằng cú pháp **Mermaid flowchart**: hiển thị rõ luồng dữ liệu từ Client $\rightarrow$ API Gateway $\rightarrow$ Core Solver/AI $\rightarrow$ Database.
* Mermaid hiển thị trực tiếp trên GitHub mà không lo vỡ ảnh.

### 5. Hướng Dẫn Khởi Động Nhanh 1 Lệnh (Quick Start)
* Hướng dẫn bằng Docker:
  ```bash
  git clone <repo_url>
  cd <repo_name>
  docker compose up -d --build
  ```
* Ghi rõ danh sách các cổng (Port) và đường dẫn truy cập (ví dụ: Giao diện Web: `http://localhost:8500`, API: `http://localhost:8000/docs`).

### 6. Bảng Đo Lường & So Sánh (Benchmark / Evaluation)
* Đưa ra các con số định lượng: Tốc độ xử lý (ms), tỷ lệ chính xác (%), lượng chi phí/năng lượng tiết kiệm được so với phương pháp truyền thống (Baseline).

### 7. Kịch Bản Chấm Thi Từng Bước (Judge Walkthrough)
* Đánh số thứ tự các bước cụ thể: Click nút gì $\rightarrow$ Nhập dữ liệu gì $\rightarrow$ Kết quả mong đợi ra sao.

### 8. Đội Ngũ & Giấy Phép (Team & License)
* Họ tên thành viên, vai trò (Frontend, Backend, AI/Thuật toán), Giảng viên hướng dẫn.
* Tuyên bố bản quyền mã nguồn mở.

---

## ⚠️ 4. Các "Tử Huyệt" Cần Tránh Tuyệt Đối (Red Flags)

| Lỗi Tử Huyệt | Hậu Quả | Cách Khắc Phục |
|---|---|---|
| 🚩 **Bản đồ dính đường lưỡi bò (đường 9 đoạn)** | **Bị loại trực tiếp ngay lập tức** do vi phạm chủ quyền lãnh thổ Việt Nam | Chỉ dùng OpenStreetMap, ArcGIS World Imagery hoặc tile Google Maps chính thức với `hl=vi` |
| 🚩 **Không chạy được bằng 1 lệnh Docker** | Mất từ 30% - 50% số điểm cài đặt | Luôn test build Docker trên máy trắng (clean machine) trước khi nộp bài |
| 🚩 **Commit "1 cục" vào sát ngày nộp** | Bị nghi ngờ sao chép/không minh bạch quá trình làm | Chia nhỏ commit theo chuẩn Conventional Commits (`feat:`, `fix:`, `docs:`) trong suốt quá trình phát triển |
| 🚩 **Thiếu file `LICENSE`** | Bị trừ điểm nặng ở khối thi Phần mềm Nguồn mở (VFOSSA) | Luôn bổ sung file `LICENSE` chuẩn OSI (Apache 2.0 hoặc GPLv3) |
| 🚩 **Để lộ API Key bí mật hoặc mật khẩu** | Trừ điểm bảo mật, nguy cơ lộ tài khoản cá nhân | Sử dụng `.env.example` và đưa `.env` vào `.gitignore` |
| 🚩 **Tồn tại file rác, file tạm biên dịch** | Gây ấn tượng thiếu chuyên nghiệp | Chặn toàn bộ `.pyc`, `__pycache__`, `.DS_Store`, file log, PDF nháp qua `.gitignore` |
