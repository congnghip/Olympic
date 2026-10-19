from typing import List, Dict, Any

class ActionPlanBuilder:
    """
    Tự động biên soạn danh sách hành động (Action Plan Checklist)
    kèm giải pháp kỹ thuật theo từng bước cho Kỹ sư thiết kế.
    """

    def generate_plan_for_issue(self, issue: Dict[str, Any]) -> List[Dict[str, Any]]:
        desc = issue.get("issue_description", "").lower()
        std_ref = issue.get("standard_reference", "Quy chuẩn Xây dựng")

        if "khoảng lùi" in desc:
            return [
                {
                    "step_order": 1,
                    "action_title": "Dịch chuyển ranh xây dựng lùi 1.0m",
                    "technical_guidance": f"Mở bản vẽ Mặt bằng Tầng 1 (KT-01), dịch chuyển tường bao phía sau theo trục Y lùi vào trong tối thiểu 1000mm để đảm bảo quy định {std_ref}."
                },
                {
                    "step_order": 2,
                    "action_title": "Cập nhật bảng tính Diện tích Xây dựng & Mật độ",
                    "technical_guidance": "Tính toán lại mật độ xây dựng sau khi lùi, cập nhật bảng thống kê diện tích trong Thuyết minh thiết kế."
                }
            ]
        elif "thang" in desc:
            return [
                {
                    "step_order": 1,
                    "action_title": "Tăng bề rộng thông thủy vế thang lên >= 1.20m",
                    "technical_guidance": f"Mở bản vẽ KT-02 và KT-03, dịch trục tường buồng thang thêm 150mm để thông thủy vế thang đạt 1200mm theo {std_ref}."
                },
                {
                    "step_order": 2,
                    "action_title": "Kiểm tra chiều rộng cửa mở ra buồng thang",
                    "technical_guidance": "Đảm bảo cửa chống cháy mở theo chiều thoát nạn và không làm hẹp bề rộng chiếu nghỉ thang."
                }
            ]
        elif "chiều cao" in desc:
            return [
                {
                    "step_order": 1,
                    "action_title": "Hạ cốt trần và dầm Tầng 1 xuống 3.90m",
                    "technical_guidance": f"Điều chỉnh cao độ sàn Tầng 2 từ +4.200m xuống +3.900m trên bản vẽ Mặt cắt và Mặt đứng chính theo {std_ref}."
                },
                {
                    "step_order": 2,
                    "action_title": "Đồng bộ cao độ sang bản vẽ Kết cấu",
                    "technical_guidance": "Cập nhật chiều dài cột tầng 1 trong bản vẽ Kết cấu KC-01 tương ứng với cao độ mới."
                }
            ]
        else:
            return [
                {
                    "step_order": 1,
                    "action_title": "Hiệu chỉnh chi tiết theo công văn",
                    "technical_guidance": f"Rà soát và chỉnh sửa thông số kỹ thuật trên bản vẽ theo đúng yêu cầu tại {std_ref}."
                }
            ]

action_plan_builder = ActionPlanBuilder()
