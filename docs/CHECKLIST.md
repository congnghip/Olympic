# 📋 Checklist Kiểm Tra Toàn Diện Trước Giờ Nộp Bài (Pre-Submission Checklist)

Trước khi gửi đường link repository GitHub cho Ban Tổ Chức cuộc thi, đội thi cần rà soát qua 15 tiêu chí bắt buộc dưới đây:

---

## 🔒 I. Pháp Lý, Bản Quyền & Chủ Quyền Lãnh Thổ (Bắt Buộc 100%)

- [ ] **1. Giấy phép mã nguồn mở (`LICENSE`):** Đã có tệp `LICENSE` theo chuẩn OSI (khuyến nghị Apache-2.0, MIT hoặc GPL-3.0).
- [ ] **2. Kiểm tra chủ quyền bản đồ (Map Sovereignty):**
  - Tuyệt đối **KHÔNG CÓ ĐƯỜNG LƯỠI BÒ** (đường 9 đoạn) trên bất kỳ màn hình nào.
  - Các tile bản đồ dùng OpenStreetMap, ArcGIS World Imagery hoặc Google Maps có tham số `hl=vi`.
- [ ] **3. Bảo mật bí mật (No Secrets/Keys in Repo):**
  - Không commit file `.env`, mật khẩu database, token bot Telegram, private key.
  - File `.env.example` chỉ chứa biến mẫu không có giá trị nhạy cảm.

---

## 🚀 II. Khả Năng Vận Hành & Đóng Gói (Reproducibility)

- [ ] **4. Triển khai 1-click Docker:** Đã test lệnh `docker compose up -d --build` trên một máy tính sạch khác và hệ thống chạy trơn tru không lỗi.
- [ ] **5. Script dự phòng (`start.sh`):** Đã cấp quyền thực thi `chmod +x start.sh` và kiểm tra chạy độc lập không cần Docker.
- [ ] **6. Định tuyến cổng mạng:** Không bị xung đột cổng mạng phổ biến, tài liệu ghi rõ cổng truy cập (Port 8000, 8501...).

---

## 📖 III. Tài Liệu Thuyết Minh & Trình Bày (README Quality)

- [ ] **7. Banner & Badges trực quan:** Có các huy hiệu trạng thái (Build, License, Tech Stack) ở đầu README.
- [ ] **8. Ảnh động demo (GIF / Video):** Có ít nhất 1 ảnh GIF hoặc video ngắn mô tả sản phẩm hoạt động thật.
- [ ] **9. Sơ đồ kiến trúc Mermaid:** Hiển thị rõ các tầng giao diện, xử lý nghiệp vụ, thuật toán và lưu trữ dữ liệu.
- [ ] **10. Kịch bản chấm thi cho Ban Giám khảo (`DEMO_GUIDE.md`):** Có hướng dẫn chi tiết từng bước click để giám khảo tự trải nghiệm trong 5-10 phút.
- [ ] **11. Bảng số liệu Benchmark:** Có số liệu so sánh định lượng chứng minh giải pháp vượt trội hơn Baseline.

---

## 🧹 IV. Vệ Sinh Mã Nguồn & Lịch Sử Git (Git Hygiene)

- [ ] **12. Bộ lọc `.gitignore` chuẩn:** Không còn các tệp rác như `__pycache__`, `.pyc`, `.DS_Store`, file log, thư mục `.venv`, file PDF/ảnh nháp.
- [ ] **13. Trạng thái Git sạch sẽ:** Lệnh `git status` trả về `nothing to commit, working tree clean`.
- [ ] **14. Lịch sử commit minh bạch:** Các commit có thông điệp rõ ràng theo chuẩn Conventional Commits (`feat:`, `fix:`, `docs:`), thể hiện quá trình làm việc thực sự.
- [ ] **15. Quyền truy cập repository:** Đã chuyển trạng thái repository sang **Public** (hoặc cấp quyền cộng tác cho tài khoản chấm thi của BTC nếu được yêu cầu).
