# ⏱️ Kịch Bản 15 Phút Trình Diễn Trước Ban Giám Khảo (Chung Kết OLP 2026)
### (15-Minute Live Demonstration Walkthrough - Mục 6 Đề Thi OLP PMNM)

> Theo quy định tại Mục 6 Đề thi OLP 2026: *"Mỗi đội thi được trình bày trước Ban Giám khảo trong 15 phút bao gồm: Giải pháp thiết kế & công nghệ, Các tính năng nền tảng & bài toán minh họa, Kết quả sản phẩm và trình diễn demo, Định hướng phát triển."*

---

## 🕒 Phân Bổ Thời Gian 15 Phút Trình Diễn

| Phần | Nội Dung Trình Bày | Thời Lượng | Trọng Tâm Đạt Điểm Cao |
|:---:|---|:---:|---|
| **1** | **Giới thiệu Giải pháp & Kiến trúc Tháp 3 Tầng** | 3 phút | Khẳng định mô hình DX-OS Open-Core (Tầng 1 Headless PaaS + Tầng 2 HPDI + Tầng 3 Smart Waste TMS) |
| **2** | **Trình diễn Nền tảng Lõi & Khởi chạy Docker** | 2 phút | Chứng minh khả năng khởi động 1-click `docker compose up -d` trơn tru trên máy sạch |
| **3** | **Trình diễn Trực Tiếp (Live Demo) Không gian H-P-D-I** | 7 phút | Thao tác trực tiếp trên bản đồ WebGIS (Port 8502), kích hoạt sự cố động, xem AI đổi tuyến < 50ms |
| **4** | **Báo cáo Kết quả Đo lường Định lượng (Benchmarks & ESG)** | 2 phút | Chứng minh tiết kiệm 25-35% quãng đường, cắt giảm phát thải CO2 rõ rệt |
| **5** | **Định hướng Phát triển & Trả lời Phản biện** | 1 phút | Tích hợp mở rộng sang các bài toán TMS logistics khác |

---

## 🎬 Kịch Bản Thao Tác Chi Tiết Trong 7 Phút Live Demo

### Bước 1: Khởi động hệ thống (1 Lệnh duy nhất)
```bash
docker compose up -d --build
```
Mở trình duyệt truy cập:
* 🗺️ **Trung tâm Điều hành WebGIS IOC:** [http://localhost:8502](http://localhost:8502) *(Màn hình chính)*
* 📊 **Bảng Phân Tích & Nghiên Cứu:** [http://localhost:8501](http://localhost:8501)
* 🔌 **API Documentation (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Bước 2: Trình diễn Không gian Dữ liệu [D] - Bản Đồ Kép Thời Gian Thực
1. Giới thiệu chế độ **Dual Map**:
   - Bên trái: Lộ trình tối ưu hóa bằng thuật toán 3D-ACO của DX-OS.
   - Bên phải: Lộ trình truyền thống (Baseline) để giám khảo thấy ngay sự khác biệt.
2. Bật tắt lớp vệ tinh **ArcGIS World Imagery** và **OpenStreetMap**, nhấn mạnh: **100% tuân thủ chủ quyền lãnh thổ Việt Nam, không dính đường lưỡi bò**.
3. Chọn kịch bản **`Q.1 Trung Tâm & Phố Đi Bộ`**, nhấn nút **"Tối Ưu Hóa Lộ Trình (Solve VRP)"**.
4. Quan sát các xe rác số 1, 2, 3 được vạch tuyến đường uốn lượn chính xác theo từng khúc cua đường phố TP.HCM.

---

### Bước 3: Trình diễn Không gian Quy trình [P] & Trí tuệ [I] - Sự Cố Động & Đổi Tuyến < 50ms
1. **Mô phỏng rào chắn giao thông:**
   - Nhấn nút mô phỏng: *"Chặn đường Nguyễn Huệ / Rào chắn thi công"*.
   - Đoạn đường lập tức đổi sang vạch đỏ cảnh báo ⛔.
   - Thuật toán **tự động tính toán đường vòng thay thế trong `< 50ms`**, xe rác chuyển hướng mượt mà qua tuyến đường song song mà không cần can thiệp thủ công.
2. **Mô phỏng xe hỏng động cơ (San tải tự động):**
   - Kích hoạt sự cố xe số 1 bị hỏng giữa đường.
   - Hệ thống tự động phân bổ lại các thùng rác chưa gom của Xe 1 sang Xe 2 và Xe 3 lân cận.

---

### Bước 4: Trình diễn Không gian Con người [H] - Tác Tử Kev AI
1. Nhập vào ô báo cáo tài xế: *"Hẻm 42 Nguyễn Huệ xe tải không vào được vì vướng rạp cưới"*.
2. Nhấn nút gửi báo cáo.
3. Tác tử thông minh **Kev AI** lập tức phân loại: `access_blocked` (độ tin cậy 96%), tự động chuyển sang chế độ **"Thu gom đi bộ cự ly ngắn (Walk-in Alley)"**, hướng dẫn tài xế đỗ xe ở đầu hẻm để đi bộ vào lấy rác.

---

### Bước 5: Bảng Chỉ Số ESG & API Swagger
1. Chỉ vào bảng chỉ số ESG bên góc màn hình: **Tổng quãng đường tiết kiệm**, **Số kg $\text{CO}_2$ cắt giảm**, **Mức tối ưu hóa tải trọng**.
2. Mở tab Swagger `http://localhost:8000/docs` chứng minh hệ thống cung cấp đầy đủ REST API chuẩn mực cho Tầng 1 PaaS.
