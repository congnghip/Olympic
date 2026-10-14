# 🏅 Olympic Competition Repository Template & Standards
### Bộ Khung Quy Chuẩn & Hướng Dẫn Trình Bày Repository Dự Thi Olympic Tin Học & Hackathon

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Olympic Standard](https://img.shields.io/badge/Competition-Olympic%20%7C%20Hackathon%20Standard-brightgreen.svg)](docs/COMPETITION_REPO_GUIDELINES.md)
[![Docker Ready](https://img.shields.io/badge/Docker-1--Click%20Ready-2496ED.svg)](docker-compose.yml)
[![Pre-submission Checklist](https://img.shields.io/badge/Checklist-15%20Verified%20Items-orange.svg)](docs/CHECKLIST.md)

---

## 📌 Giới Thiệu

Repository này được thiết kế và cấu trúc hóa theo **bộ tiêu chuẩn quốc gia dành cho các kỳ thi Phần mềm Nguồn mở (Olympic Tin học Sinh viên - VFOSSA), Hackathon và Giải thưởng Sáng tạo Khoa học Công nghệ**.

Tất cả các thành phần đặc thù trước đây (thu gom rác) đã được lược bỏ hoàn toàn, giữ lại bộ khung chuẩn hoá cùng hệ thống tài liệu hướng dẫn chi tiết giúp đội thi sẵn sàng áp dụng ngay cho đề tài mới của mình.

---

## 📚 Hệ Thống Tài Liệu Hướng Dẫn Kèm Theo

| Tài liệu | Nội dung chính |
|---|---|
| 📖 [**`docs/COMPETITION_REPO_GUIDELINES.md`**](docs/COMPETITION_REPO_GUIDELINES.md) | **Cẩm nang quy chuẩn dự thi:** Ma trận thang điểm 5 trụ cột của Ban Giám Khảo, quy tắc thiết kế README, các "tử huyệt" khiến đội thi bị trừ điểm hoặc loại trực tiếp |
| 📑 [**`docs/TEMPLATE_PROJECT_README.md`**](docs/TEMPLATE_PROJECT_README.md) | **Khung mẫu README hoàn chỉnh:** Bản mẫu chuẩn với các section điểm cộng (Mermaid, Benchmark, Quick Start, Demo Scenario) để copy-paste cho đề tài mới |
| 📋 [**`docs/CHECKLIST.md`**](docs/CHECKLIST.md) | **Bảng kiểm tra 15 mục trước giờ nộp bài:** Rà soát bản quyền OSI, bảo mật secret, tính tương thích Docker, kiểm tra chủ quyền bản đồ không dính đường lưỡi bò |

---

## 🏗️ Cấu Trúc Thư Mục Tiêu Chuẩn Trong Repository Này

```
Olympic/
├── docs/                                  # Hệ thống hướng dẫn & tiêu chuẩn nộp thi
│   ├── COMPETITION_REPO_GUIDELINES.md     # Cẩm nang tiêu chí chấm điểm & quy tắc vàng
│   ├── TEMPLATE_PROJECT_README.md         # Khung mẫu README sẵn sàng cho đề tài mới
│   └── CHECKLIST.md                       # 15 tiêu chí kiểm tra trước khi nộp bài
├── backend/                               # Phân hệ API dịch vụ (FastAPI)
│   ├── main.py                            # Cổng API chính
│   ├── service.py                         # Điều phối logic nghiệp vụ
│   └── utils.py                           # Tiện ích bổ trợ
├── streamlit/                             # Phân hệ giao diện phân tích / Dashboard
│   ├── app.py                             # Giao diện trực quan tương tác
│   └── solver_api_client.py               # Kết nối với API backend
├── src/                                   # Mã nguồn thuật toán lõi hiệu năng cao (C++17)
│   ├── CMakeLists.txt                     # Cấu hình biên dịch chuẩn CMake
│   ├── core/                              # Các mô hình dữ liệu cốt lõi
│   └── solvers/                           # Cài đặt thuật toán tối ưu hóa
├── docker-compose.yml                     # Khởi chạy toàn bộ hệ thống bằng 1 lệnh duy nhất
├── Dockerfile                             # Đóng gói môi trường container độc lập
├── start.sh                               # Script chạy nhanh dành cho Linux / macOS
├── .env.example                           # Mẫu cấu hình biến môi trường
├── .gitignore                             # Bộ lọc loại bỏ file rác, file tạm, cache
└── LICENSE                                # Giấy phép mã nguồn mở Apache 2.0 (OSI-approved)
```

---

## 🎯 5 Tiêu Chuẩn "Vàng" Của Một Repository Đạt Giải Cao

### 1. 🚀 Khả năng chạy được ngay bằng 1 lệnh (1-Click Run)
Ban Giám khảo chấm hàng chục đội thi trong thời gian ngắn và không thể cài đặt môi trường thủ công cho từng dự án. Repository đạt điểm tối đa khi hỗ trợ:
```bash
docker compose up -d --build
```
Và cung cấp ngay các cổng truy cập rõ ràng:
* **Giao diện Web:** [http://localhost:8501](http://localhost:8501)
* **Tài liệu API (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. 🗺️ Tuân thủ 100% chủ quyền lãnh thổ Việt Nam
Nếu đề tài có hiển thị bản đồ: **Tuyệt đối không sử dụng bất kỳ nguồn tile nào chứa đường lưỡi bò (đường 9 đoạn)**. Chỉ sử dụng OpenStreetMap, ArcGIS World Imagery hoặc tile Google Maps chính thức với ngôn ngữ tiếng Việt (`hl=vi`).

### 3. 📜 Giấy phép mã nguồn mở đạt chuẩn OSI
Repository bắt buộc phải có tệp [`LICENSE`](LICENSE) hợp lệ (như **Apache License 2.0**, **MIT License** hoặc **GPL v3**). Thiếu giấy phép là lỗi nghiêm trọng ở khối thi Phần mềm Nguồn mở (VFOSSA).

### 4. 📊 Bảng so sánh định lượng (Benchmarks)
Luôn đưa ra bảng đo lường số liệu cụ thể: Tốc độ xử lý (ms), tỷ lệ cải thiện (%), lượng tài nguyên tiết kiệm so với giải pháp truyền thống (Baseline) để chứng minh tính vượt trội khoa học của đề tài.

### 5. 🎬 Minh họa trực quan (GIF/Video Demo)
Có ảnh động demo (`assets/demo.gif`) hoặc video ngắn 2 phút giúp giám khảo nắm bắt trọn vẹn giá trị sản phẩm chỉ trong 10 giây đầu tiên khi mở repo.

---

## 🛠️ Hướng Dẫn Sử Dụng Khung Này Cho Đề Tài Mới

1. **Bước 1:** Sao chép nội dung từ [docs/TEMPLATE_PROJECT_README.md](docs/TEMPLATE_PROJECT_README.md) vào `README.md` chính.
2. **Bước 2:** Điền tên đề tài, mô tả bài toán, sơ đồ kiến trúc Mermaid và bảng số liệu của nhóm bạn.
3. **Bước 3:** Đặt mã nguồn vào các thư mục tương ứng: `backend/` (dịch vụ), `frontend/` (giao diện), `src/` (thuật toán).
4. **Bước 4:** Chạy kiểm tra Docker bằng `docker compose up --build`.
5. **Bước 5:** Đối chiếu với [docs/CHECKLIST.md](docs/CHECKLIST.md) để đảm bảo 15/15 tiêu chí đã hoàn thiện trước khi nộp bài.

---

## 📜 Giấy Phép (License)

Dự án được phân phối dưới giấy phép mã nguồn mở **Apache License 2.0**. Xem chi tiết tại tệp [`LICENSE`](LICENSE).