# Danh Sách Kiểm Tra Đóng Gói & Triển Khai (Deployment Checklist)

Bảng kiểm tra tiêu chuẩn kỹ thuật trước khi triển khai hoặc phát hành hệ thống lên môi trường production.

---

## 1. Hạ Tầng & Triển Khai
- [ ] **Docker Compose:** Đã kiểm thử lệnh `docker compose up -d --build` trên môi trường sạch, khởi động đầy đủ các dịch vụ mà không phát sinh lỗi thoát (exit code 0).
- [ ] **Script Dự phòng (`start.sh`):** Đã phân quyền thực thi `chmod +x start.sh`, kiểm tra tính năng chạy độc lập khi không sử dụng Docker.
- [ ] **Định cấu hình Cổng mạng:** Các cổng 8000, 8501, 8502 và 5432 không bị xung đột, được ánh xạ chính xác trong tệp `docker-compose.yml`.
- [ ] **Biến Môi Trường:** Tệp `.env.example` chứa đầy đủ các biến cấu hình mẫu, không lưu trữ thông tin bí mật (mật khẩu thật, private key).

---

## 2. Dữ Liệu & Không Gian Địa Lý (GIS)
- [ ] **Cơ Sở Dữ Liệu PostGIS:** Tệp `core-platform/database/init.sql` nạp thành công các phần mở rộng `uuid-ossp` và `postgis`, tạo đủ các bảng dữ liệu thực thể.
- [ ] **Tuân Thủ Quy Chuẩn Bản Đồ:** 
  - Toàn bộ các lớp bản đồ WebGIS sử dụng OpenStreetMap và ArcGIS World Imagery chính thức.
  - Tuyệt đối không sử dụng các nguồn dữ liệu có đường 9 đoạn (đường lưỡi bò).
  - Tọa độ mẫu kiểm thử nằm trong địa phận hợp pháp của TP. Hồ Chí Minh.

---

## 3. Mã Nguồn & Giấy Phép Bản Quyền
- [ ] **Giấy Phép Mã Nguồn Mở (`LICENSE`):** Đã có tệp `LICENSE` theo chuẩn Apache License 2.0.
- [ ] **Vệ Sinh Kho Lưu Trữ (`.gitignore`):** Không commit các tệp rác hệ điều hành (`.DS_Store`), tệp thực thi biên dịch (`*.o`, `build/`), bộ nhớ đệm Python (`__pycache__`, `*.pyc`), hoặc nhật ký (`*.log`).
- [ ] **Tài Liệu Kỹ Thuật:** Tài liệu `README.md`, `docs/ARCHITECTURE.md`, `docs/HPDI_SPECIFICATION.md` và `docs/API_REFERENCE.md` đồng nhất về mặt kiến trúc và thông số kỹ thuật.
