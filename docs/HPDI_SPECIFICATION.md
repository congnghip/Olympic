# Ánh Xạ Kiến Trúc Nghiệp Vụ Theo Khung H - P - D - I

Tài liệu chi tiết về sự phân bổ các module kỹ thuật thực tế trong mã nguồn dự án tương ứng với 4 không gian năng lực số hoá:

---

## 1. [H] Human (Con người số) - Giao Tiếp Hiện Trường
* **Module hiện thực:** Giao diện điều phối hiện trường trong [`map_ui/index.html`](../map_ui/index.html) và endpoint [`/api/waste/driver-report`](../map_ui/server.py).
* **Tính năng:**
  - Kênh phản ánh của tài xế: Cho phép nhập hoặc ghi âm phản ánh hiện trường (ngõ hẻm bị chặn, rác cồng kềnh, công trình thi công).
  - Nút bấm phát tín hiệu báo động SOS khẩn cấp (`alarm=sos`).
  - Hiển thị trực quan trạng thái pin và viễn trắc phương tiện.

---

## 2. [P] Process (Quy trình số) - Tự Động Hóa Xử Lý Ngoại Lệ (SOP)
* **Module hiện thực:** Logic nghiệp vụ trong [`map_ui/waste_solver.py`](../map_ui/waste_solver.py) và [`backend/waste_dispatcher.py`](../backend/waste_dispatcher.py).
* **Tính năng:**
  - Quy trình thu gom tiêu chuẩn: Xuất phát từ trạm $\rightarrow$ đi qua các điểm gom tối ưu theo sức chứa $\rightarrow$ hồi quy về trạm.
  - Kịch bản tự động phản ứng rào chắn: Loại bỏ đoạn đường bị chặn khỏi đồ thị và tự động tính đường vòng thay thế (detour) trong `< 50ms`.
  - Kịch bản san tải xe hỏng: Tự động phân bổ lại các điểm gom chưa thực hiện sang các xe lân cận còn dung tích trống.
  - Kịch bản thu gom ngõ hẻm: Tính toán điểm đỗ xe đầu hẻm và khoảng cách nhân viên đi bộ tiếp cận thùng rác.

---

## 3. [D] Data (Dữ liệu số) - Trung Tâm Điều Hành WebGIS & Đo Lường ESG
* **Module hiện thực:** Giao diện Bản Đồ Kép trong [`map_ui/index.html`](../map_ui/index.html) và bộ đệm [`map_ui/route_cache.json`](../map_ui/route_cache.json).
* **Tính năng:**
  - Bản đồ kép (Dual-Map): Hiển thị đồng thời hai góc nhìn để đối chiếu giữa thuật toán đề xuất và thuật toán Baseline.
  - Bản đồ chuẩn chủ quyền: Sử dụng OpenStreetMap và ArcGIS World Imagery (100% không đường lưỡi bò).
  - Bộ đệm ma trận OSRM: Lưu trữ trước hình học tuyến đường trên mạng lưới đường phố TP.HCM giúp hiển thị không độ trễ.
  - Đo lường chỉ số xanh (ESG): Tự động tính toán tổng quãng đường (km), lượng phát thải $\text{CO}_2$ cắt giảm, và tỷ lệ lấp đầy thùng xe.

---

## 4. [I] Intelligence (Trí tuệ số) - Bộ Giải 3D-ACO & Tác Tử NLP
* **Module hiện thực:** Lõi giải thuật C++17 trong [`src/`](../src/) và các hàm tối ưu trong [`map_ui/waste_solver.py`](../map_ui/waste_solver.py).
* **Tính năng:**
  - Clarke-Wright Savings với hệ số ưu tiên mùi hôi: Ưu tiên gom sớm các thùng rác đang bốc mùi (`has_smell=true`).
  - Google OR-Tools VRP Solver: Mô hình tham chiếu so sánh đối chứng.
  - Lõi giải thuật C++17 Parallel ACO (PACO): Giải thuật đàn kiến đa luồng (OpenMP) giải bài toán tối ưu hóa quy mô lớn.
  - Tác tử phân loại báo cáo tài xế: Phân loại tự động ngữ nghĩa báo cáo hiện trường để kích hoạt hành vi điều phối tương ứng.
