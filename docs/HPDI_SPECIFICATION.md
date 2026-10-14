# Đặc Tả Kỹ Thuật: Khung Năng Lực Quản Trị Số H - P - D - I

Tài liệu chi tiết về 4 không gian năng lực số hoá trong kiến trúc Tầng 2 của nền tảng DX-OS Open-Core.

---

## 1. [H] Human (Con người số) - Giao Tiếp & Tác Nghiệp Hiện Trường

Không gian kết nối nhân sự vận hành giữa trung tâm điều phối và nhân sự tác nghiệp ngoài hiện trường:
* **Web Mobile Tracker:** Ứng dụng nền web nhẹ, tương thích với trình duyệt di động không cần cài đặt ứng dụng gốc.
* **Định vị & Viễn trắc phương tiện:** Đồng bộ tọa độ GPS thời gian thực, vận tốc, hướng la bàn và trạng thái pin thiết bị.
* **Kênh phản ánh sự cố hiện trường:**
  - Nút bấm phát tín hiệu ưu tiên SOS (`alarm=sos`) về phòng điều hành khi xảy ra va chạm hoặc sự cố khẩn cấp.
  - Trường nhập dữ liệu phản ánh hiện trường (Voice-to-Text / Text), cho phép ghi nhận nguyên nhân chậm trễ hoặc chướng ngại vật trên tuyến.

---

## 2. [P] Process (Quy trình số) - Chuẩn Hóa & Phản Ứng Tự Động

Chuẩn hóa các luồng quy trình vận hành tiêu chuẩn (SOP) và kịch bản xử lý ngoại lệ:
* **Quy trình Thu gom Chuẩn:**
  1. Khởi tạo phiên làm việc tại trạm trung chuyển (Depot).
  2. Tiếp nhận lộ trình định tuyến đã được tối ưu hóa theo thứ tự bô rác.
  3. Cập nhật trạng thái sau khi hoàn thành thu gom tại từng điểm (`collected`).
  4. Hồi quy về bãi đổ rác/trạm trung chuyển khi đạt ngưỡng tải trọng cho phép.
* **Quy trình Xử lý Ngoại lệ Tự động (Automated Exception Handling):**
  - **Sự cố Rào chắn / Đường cấm:** Hệ thống ghi nhận đoạn đường nghẽn, cập nhật trọng số cạnh đồ thị và tái định tuyến đường vòng trong `< 50ms`.
  - **Sự cố Hỏng hóc Phương tiện:** Hệ thống chuyển giao các điểm gom chưa thực hiện của xe gặp sự cố sang các phương tiện lân cận còn dung tích khả dụng.
  - **Sự cố Không thể tiếp cận (Ngõ sâu / Hẹp):** Kích hoạt cơ chế "Thu gom đi bộ cự ly ngắn (Walk-in Alley Collection)", tính toán điểm đỗ gần nhất trên trục đường chính và cự ly di chuyển bộ của nhân viên.

---

## 3. [D] Data (Dữ liệu số) - Trung Tâm Điều Hành WebGIS & Đo Lường Thực Chứng

Hệ thống hóa dòng chảy dữ liệu phục vụ điều hành và đánh giá hiệu năng:
* **Trung tâm Điều hành WebGIS (IOC) - Chế độ Bản Đồ Kép (Dual-Map):**
  - Hiển thị song song hai khung nhìn để đối chiếu hiệu quả định tuyến giữa thuật toán tối ưu cải tiến và thuật toán Baseline.
  - Lớp bản đồ sử dụng nguồn OpenStreetMap và ArcGIS World Imagery, tuân thủ quy chuẩn không gian địa lý và chủ quyền lãnh thổ Việt Nam.
* **Bản sao số (Digital Twin):** Thể hiện trực quan trạng thái mạng lưới: tọa độ di chuyển của đội xe, mức đầy của thùng rác (% fill level), và cảnh báo điểm nóng môi trường.
* **Mô hình Đo lường Chỉ số Xanh & ESG:**
  - Tổng quãng đường di chuyển: $D = \sum d_i$ (km).
  - Lượng phát thải $\text{CO}_2$ cắt giảm: $\Delta E = (D_{\text{baseline}} - D_{\text{opt}}) \times 0.285 \text{ kg CO}_2/\text{km}$.
  - Hệ số tối ưu hóa tải trọng phương tiện: $\eta = \frac{\text{Tải thực tế}}{\text{Sức chứa tối đa}} \times 100\%$.

---

## 4. [I] Intelligence (Trí tuệ số) - Xử Lý Ngôn Ngữ & Thuật Toán 3D-ACO

Tích hợp trí tuệ nhân tạo và giải thuật bầy đàn giải quyết bài toán tối ưu:
* **Tác tử Xử lý Ngôn ngữ Báo cáo Hiện trường:**
  - Tiếp nhận chuỗi phản ánh của tài xế và dữ liệu GPS.
  - Phân loại ngữ nghĩa theo các danh mục: `access_blocked` (đường bị chặn), `vehicle_breakdown` (xe hỏng), `invalid_waste` (rác vi phạm), `normal_success` (thu gom bình thường).
  - Tự động kích hoạt hành động nghiệp vụ tương ứng kèm chỉ số độ tin cậy.
* **Động cơ Giải thuật 3D-Parallel ACO Core (C++17):**
  - Hiện thực hóa thuật toán Tối ưu hóa Đàn kiến Song song 3 chiều (3D-Parallel Ant Colony Optimization) giải bài toán định tuyến phương tiện có giới hạn tải trọng (CVRP).
  - Ứng dụng OpenMP đa luồng, hỗ trợ xử lý đồ thị hàng trăm điểm dừng trong thời gian ngắn.
