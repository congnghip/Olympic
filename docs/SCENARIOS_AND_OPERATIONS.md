# Hướng Dẫn Vận Hành & Các Kịch Bản Kiểm Thử Hệ Thống

Tài liệu hướng dẫn triển khai, vận hành và thử nghiệm các kịch bản thực tế trên nền tảng DX-OS Open-Core.

---

## 1. Khởi Động Hệ Thống

### Cách 1: Sử dụng Docker Compose (Khuyến nghị)
Yêu cầu hệ thống đã cài đặt Docker và Docker Compose:

```bash
docker compose up -d --build
```

Sau khi khởi chạy thành công, các dịch vụ sẽ hoạt động tại các cổng:
* **Trung tâm Điều hành WebGIS IOC:** [http://localhost:8502](http://localhost:8502)
* **Bảng Phân Tích & Nghiên Cứu Thuật Toán (Streamlit):** [http://localhost:8501](http://localhost:8501)
* **Tài Liệu Cổng API (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Cơ Sở Dữ Liệu Không Gian PostgreSQL + PostGIS:** Cổng `5432` (`dx_admin` / `dx_os_db`)

Để kiểm tra trạng thái các container:
```bash
docker compose ps
docker compose logs -f
```

Để dừng toàn bộ dịch vụ:
```bash
docker compose down
```

---

### Cách 2: Chạy Trực Tiếp Bằng Bash Script (Local Development)
Yêu cầu máy chủ Linux có sẵn Python $\ge 3.10$, `cmake`, `build-essential`:

```bash
chmod +x start.sh
./start.sh
```

---

## 2. Các Kịch Bản Kiểm Thử Vận Hành Thực Tế

### Kịch Bản 1: Tối Ưu Hóa Tuyến Tuyến Đa Phương Tiện
1. Mở giao diện điều hành tại `http://localhost:8502`.
2. Tại bảng điều khiển bên trái, chọn kịch bản mẫu: **`Q.1 Trung Tâm & Phố Đi Bộ`** hoặc **`Q.3 Khu Bàn Cờ - Hẻm Nhỏ`**.
3. Nhấn **"Tối Ưu Hóa Lộ Trình (Solve VRP)"**.
4. **Kết quả quan sát:**
   - Tuyến đường di chuyển của từng xe được thể hiện bằng các mã màu riêng biệt (Xanh ngọc, Tím, Cam).
   - Đoạn đường được bám sát đồ thị giao thông thực tế qua ma trận OSRM.
   - Bảng chỉ số góc phải cập nhật tổng quãng đường (km), phát thải $\text{CO}_2$ cắt giảm và hiệu suất tải trọng.

---

### Kịch Bản 2: Phản Ứng Sự Cố Rào Chắn & Tái Định Tuyến Tức Thời (< 50ms)
1. Trong lúc xe đang trên lộ trình, kích hoạt sự cố: **"Chặn đường Nguyễn Huệ / Rào chắn thi công"**.
2. **Kết quả quan sát:**
   - Đoạn đường bị phong tỏa lập tức chuyển sang vạch cảnh báo đỏ kèm biểu tượng rào chắn ⛔.
   - Hệ thống tự động tính toán lại đường vòng thay thế (detour) trong thời gian dưới 50 mili-giây.
   - Tuyến đường mới tránh hoàn toàn đoạn đường cấm mà không làm gián đoạn lịch trình các điểm còn lại.

---

### Kịch Bản 3: San Tải Tự Động Khi Phương Tiện Gặp Sự Cố Kỹ Thuật
1. Kích hoạt sự cố xe số 1 bị hỏng hóc động cơ tại một vị trí trên tuyến.
2. **Kết quả quan sát:**
   - Hệ thống tự động ngắt kết nối xe số 1.
   - Các điểm gom chưa hoàn thành của xe số 1 được tự động tính toán và san sẻ sang các xe lân cận còn dung tích chứa khả dụng.

---

### Kịch Bản 4: Báo Cáo Hiện Trường & Chế Độ Thu Gom Đi Bộ (Walk-in Alley)
1. Tại khung phản ánh của tài xế, nhập nội dung: *"Hẻm 42 Nguyễn Huệ xe tải không vào được, vướng công trình cáp"*.
2. Nhấn nút gửi báo cáo.
3. **Kết quả quan sát:**
   - Tác tử NLP phân tích và phân loại sự cố: `access_blocked`.
   - Hệ thống chuyển đổi chế độ thu gom sang **Đi bộ cự ly ngắn (Walk-in)**: hiển thị vị trí đỗ xe thích hợp tại đầu hẻm và đường nối đi bộ tiếp cận thùng rác.
