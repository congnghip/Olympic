# 🧬 Đặc Tả Không Gian Năng Lực Số H - P - D - I
### (HPDI Operational Framework - DX-OS Open-Core)

Đề tài hiện thực hóa trọn vẹn mô hình chuỗi tiến hóa năng lực quản trị số **H - P - D - I** theo đúng lý thuyết chuyển đổi số trong đề thi OLP 2026:

---

## 🧑‍💻 1. [H] Human (Con người số) - Môi Trường Tác Nghiệp Hiện Trường

Khởi tạo môi trường số kết nối toàn diện lực lượng lao động hiện trường (tài xế xe gom rác, công nhân vệ sinh môi trường, cán bộ điều phối):
* **Web Mobile Tracker không cần cài đặt:** Hoạt động trực tiếp trên trình duyệt mọi điện thoại (Safari, Chrome, Zalo browser).
* **Kết nối thời gian thực:** Đồng bộ tọa độ GPS vệ tinh (sai số 5 - 15m), vận tốc và hướng di chuyển của xe về máy chủ điều hành.
* **Giao tiếp đa phương thức:**
  - Nút bấm **Báo động SOS khẩn cấp** kích hoạt chuông cảnh báo tại trung tâm điều hành.
  - Hộp nhập **Báo cáo sự cố bằng Giọng nói & Chữ viết** (Voice-to-Text / Text Report).
  - Tự động nhận diện mức pin thiết bị để cảnh báo khi máy sắp hết nguồn.

---

## ⚙️ 2. [P] Process (Quy trình số) - Chuẩn Hóa & Xử Lý Ngoại Lệ Tự Động

Số hóa các quy trình tác nghiệp tiêu chuẩn (SOP) và tự động hóa các kịch bản phản ứng sự cố:
* **Quy trình Thu gom Chuẩn:**
  1. Tiếp nhận danh sách điểm gom theo ca làm việc $\rightarrow$
  2. Xuất phát từ trạm trung chuyển (Depot) $\rightarrow$
  3. Lần lượt tiếp cận các bô rác theo thứ tự tối ưu $\rightarrow$
  4. Trở về trạm khi đầy tải hoặc hoàn thành lộ trình.
* **Quy trình Xử lý Ngoại lệ Tự động (Exception Handling SOP):**
  - **Kịch bản 1: Rào chắn công trình / Đường cấm:** Hệ thống loại bỏ cung đường bị chặn trên đồ thị giao thông, tự động tìm đường vòng thay thế trong `< 50ms`.
  - **Kịch bản 2: Xe hỏng động cơ giữa tuyến:** Tự động cắt các điểm gom còn lại của xe gặp sự cố, tính toán san tải sang các xe lân cận còn dư dung tích chứa mà không cần điều phối viên thao tác thủ công.
  - **Kịch bản 3: Hẻm sâu không vào được:** Kích hoạt quy trình thu gom đi bộ cự ly ngắn (*walk-in alley collection*), tính toán điểm đỗ xe tối ưu tại đầu hẻm.

---

## 📊 3. [D] Data (Dữ liệu số) - Trung Tâm Điều Hành WebGIS & Đo Lường Thực Chứng

Chuyển đổi từ quản trị cảm tính sang quản trị hoàn toàn dựa trên dữ liệu thực chứng:
* **Trung tâm Điều hành WebGIS (IOC) Chế độ Bản Đồ Kép (Dual-Map):**
  - Màn hình chia đôi cho phép đối chiếu song song: Bên trái là thuật toán tối ưu cải tiến của hệ thống, bên phải là thuật toán truyền thống (Baseline).
  - Lớp bản đồ tuân thủ 100% chủ quyền lãnh thổ Việt Nam (OpenStreetMap & ArcGIS vệ tinh, tuyệt đối không có đường lưỡi bò).
* **Bản sao số (Digital Twin):** Trực quan hóa chính xác vị trí thời gian thực của đội xe, mức đầy của từng bô rác (% fill level), và cảnh báo rác bốc mùi.
* **Bảng Đo Lường Chỉ Số Môi Trường & ESG:**
  - Đo lường tổng quãng đường di chuyển (km).
  - Định lượng khối lượng $\text{CO}_2$ cắt giảm được: $\Delta E = \Delta D \times 0.285 \text{ kg CO}_2/\text{km}$.
  - Tỷ lệ tối ưu hóa sức chứa thùng xe (Capacity Utilization Rate).

---

## 🧠 4. [I] Intelligence (Trí tuệ số) - Tác Tử Thông Minh & Thuật Toán 3D-ACO

Ở bậc thang cao nhất của chuỗi tiến hóa số, hệ thống tích hợp trí tuệ nhân tạo và giải thuật bầy đàn tự hành:
* **Tác tử Thông minh Phân tích Ngữ nghĩa Hiện trường (Kev AI Agent):**
  - Tiếp nhận chuỗi phản ánh của tài xế và dữ liệu GPS.
  - Tự động phân loại bản chất sự cố: `access_blocked` (đường bị chặn), `vehicle_breakdown` (xe hỏng), `invalid_waste` (rác vi phạm), `normal_success` (hoàn thành).
  - Đưa ra quyết định điều phối tức thì kèm điểm tin cậy (Confidence Score).
* **Động cơ Giải thuật 3D-Parallel ACO Core (C++17):**
  - Ứng dụng thuật toán Đàn kiến Song song 3 chiều (3D-Parallel Ant Colony Optimization) giải bài toán định tuyến phương tiện phức hợp.
  - Tận dụng đa luồng OpenMP trên phần cứng máy chủ, giải bài toán quy mô lớn trong vài chục mili-giây.
