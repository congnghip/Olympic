# Kịch Bản Chấm Thi & Hướng Dẫn Trình Diễn (Competition Demo Guide)

> **Tài liệu dành cho Ban Giám khảo và Hội đồng Đánh giá**  
> Dự án: **Smart Waste Management & Dynamic Incident Re-routing Platform (3D-ACO)**

---

## ⏱️ Tổng Quan Thời Gian Chấm Thi (Khuyến nghị 5 - 10 phút)

| Bước | Nội dung trình diễn | Mục tiêu đánh giá | Thời gian |
|:---:|---|---|:---:|
| **1** | Khởi động 1 lệnh duy nhất với Docker | Tính sẵn sàng & đóng gói chuẩn mực | 1 phút |
| **2** | Trình diễn Bản đồ Điều phối Thời gian thực | Tính năng trực quan, chuẩn bản đồ VN | 2 phút |
| **3** | Tối ưu hóa lộ trình đa xe (Multi-truck VRP) | Hiệu năng thuật toán 3D-ACO / Heuristics | 2 phút |
| **4** | Kích hoạt sự cố động & Tính đường vòng tức thì | Khả năng tự thích ứng (Self-healing Re-routing) | 2 phút |
| **5** | Kiểm tra ESG, API Swagger & Báo cáo kết quả | Tính hoàn thiện kỹ thuật & tác động thực tế | 2 phút |

---

## 🚀 Bước 1: Khởi Động Hệ Thống 1 Lệnh (One-Click Launch)

Mở Terminal tại thư mục gốc của dự án và chạy:

```bash
docker compose up -d --build
```
*Hoặc khởi động trực tiếp bằng Bash script nếu môi trường đã có sẵn Python:*
```bash
./start.sh
```

Hệ thống sẽ đồng loạt kích hoạt 3 cổng dịch vụ:
- 🗺️ **Bản đồ điều phối rác thời gian thực:** [http://localhost:8502](http://localhost:8502) *(Trọng tâm chấm thi)*
- 📊 **Bảng điều khiển tham số & phân tích:** [http://localhost:8501](http://localhost:8501)
- 🔌 **FastAPI Swagger Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧭 Bước 2: Trình Diễn Bản Đồ Điều Phối (Port 8502)

1. Truy cập vào trình duyệt: **`http://localhost:8502`**.
2. **Quan sát giao diện:**
   - **Chế độ màn hình chia đôi (Dual Map):** So sánh trực quan giữa thuật toán cải tiến của đội thi và thuật toán Baseline.
   - Bản đồ hiển thị rõ ràng các điểm tập kết bô rác, dung lượng thùng (% fill level), chỉ số cảnh báo bốc mùi (`has_smell`), và trạm trung chuyển (Depot).
   - Tùy chọn chuyển đổi lớp nền vệ tinh **ArcGIS World Imagery** hoặc **OpenStreetMap** (100% tuân thủ chủ quyền, không có đường lưỡi bò).

---

## 🧮 Bước 3: Tối Ưu Hóa Tuyến Tuyến Đa Xe (Multi-truck Routing)

1. Trên bảng điều khiển bên trái, chọn preset: **`Q.1 Trung Tâm & Phố Đi Bộ`** hoặc **`Q.3 Khu Bàn Cờ - Hẻm Nhỏ`**.
2. Nhấn nút **"Tối Ưu Hóa Lộ Trình (Solve VRP)"**.
3. **Kết quả hiển thị:**
   - Tuyến đường xe chạy được vẽ mượt mà bám sát từng khúc cua đường phố thực tế (thông qua đồ thị OSRM và Route Cache).
   - Phân màu trực quan theo từng xe thu gom: Xe số 1 (màu xanh ngọc), Xe số 2 (màu tím), Xe số 3 (màu cam).
   - Hiển thị bảng chỉ số ESG: **Tổng quãng đường (km)**, **Lượng $\text{CO}_2$ cắt giảm**, **Tỷ lệ lấp đầy thùng rác**.

---

## ⚡ Bước 4: Thử Nghiệm Sự Cố Động & Đổi Tuyến Thời Gian Thực (Dynamic Re-routing)

Đây là **tính năng đột phá** giúp giải quyết thực trạng giao thông phức tạp tại các đô thị Việt Nam:

1. **Thử nghiệm 1: Rào chắn đường đột xuất (Roadblock Incident)**
   - Nhấn vào nút mô phỏng sự cố: **"Chặn đường Nguyễn Huệ / Rào chắn thi công"**.
   - **Hiện tượng quan sát:** 
     + Đoạn đường bị chặn chuyển sang màu đỏ kèm biểu tượng cảnh báo ⛔.
     + Hệ thống tự động tính toán lại lộ trình chỉ trong **< 50ms**, xe rác lập tức chuyển hướng đi đường vòng qua đường song song mà không cần người điều hành can thiệp thủ công.

2. **Thử nghiệm 2: Xe rác gặp sự cố hỏng hóc (Vehicle Breakdown)**
   - Kích hoạt sự cố xe số 1 bị hỏng động cơ giữa tuyến.
   - **Hiện tượng quan sát:**
     + Toàn bộ các điểm gom rác chưa hoàn thành của Xe 1 được điều phối viên tự động chia tải sang Xe số 2 và Xe số 3 đang ở gần nhất còn sức chứa.

3. **Thử nghiệm 3: Báo cáo bằng giọng nói/văn bản của tài xế (Voice/Text Report)**
   - Nhập nội dung vào ô báo cáo tài xế: *"Hẻm 42 Nguyễn Huệ đang sửa cống xe không vào được, cần đi bộ vào lấy thùng"*.
   - Nhấn **"Gửi Báo Cáo"**.
   - Hệ thống Kev AI tự động phân loại sự cố: `access_blocked`, kích hoạt cơ chế `walk-in collection` (thu gom đi bộ cự ly ngắn) thay vì bỏ sót rác của người dân.

---

## 📊 Bước 5: Kiểm Tra API RESTful & Chỉ Số ESG

1. Mở tab mới truy cập [http://localhost:8000/docs](http://localhost:8000/docs) hoặc các endpoint tại port 8502:
   - Thử nghiệm endpoint `/api/waste/presets`: Trả về danh sách kịch bản đô thị chuẩn.
   - Thử nghiệm endpoint `/api/waste/driver-report`: Nhận diện báo cáo hiện trường thời gian thực.
2. Kiểm tra log vận hành tại terminal để xác nhận không phát sinh lỗi hoặc cảnh báo ngoại lệ.
