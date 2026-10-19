from typing import List, Dict, Any, Optional

class DrawingGroundingEngine:
    """
    Engine định vị lỗi từ văn bản lên bản vẽ kỹ thuật (Multimodal Grounding).
    Tính toán tọa độ Bounding Box [x_min, y_min, x_max, y_max] theo tỷ lệ phần trăm (0 - 100%).
    """

    def map_issue_to_drawing(self, issue: Dict[str, Any], drawings: List[Any]) -> Dict[str, Any]:
        """
        Ánh xạ một issue vào bản vẽ phù hợp nhất dựa trên từ khóa bản vẽ (KT-01, Mặt bằng, etc.)
        """
        desc = issue.get("issue_description", "").lower()
        matched_drawing_id = None
        matched_drawing_number = None

        # 1. Tìm bản vẽ khớp theo số hiệu (KT-01, KT-02...)
        for d in drawings:
            d_num = getattr(d, "drawing_number", "").lower()
            if d_num and d_num in desc:
                matched_drawing_id = getattr(d, "id", None)
                matched_drawing_number = getattr(d, "drawing_number", "")
                break

        # 2. Nếu chưa thấy, tìm theo tiêu đề (Tầng 1, Mặt đứng, Cầu thang...)
        if not matched_drawing_id:
            for d in drawings:
                d_title = getattr(d, "title", "").lower()
                if any(w in desc and w in d_title for w in ["tầng 1", "tầng 2", "mặt đứng", "mặt cắt", "móng"]):
                    matched_drawing_id = getattr(d, "id", None)
                    matched_drawing_number = getattr(d, "drawing_number", "")
                    break

        # 3. Gán tọa độ Bounding Box mẫu (theo tỷ lệ canvas 0-100%)
        bbox = self._calculate_bounding_box(issue.get("issue_number", 1), desc)

        return {
            "drawing_id": matched_drawing_id,
            "drawing_number": matched_drawing_number,
            "bounding_box": bbox
        }

    def _calculate_bounding_box(self, issue_num: int, description: str) -> Dict[str, float]:
        """Tính toán hộp bao trực quan trên bản vẽ"""
        if "khoảng lùi" in description or "phía sau" in description:
            # Tọa độ khu vực ranh đất phía sau
            return {"x_min": 72.5, "y_min": 15.0, "x_max": 95.0, "y_max": 45.0}
        elif "thang" in description or "thoát hiểm" in description:
            # Tọa độ buồng thang giữa nhà
            return {"x_min": 38.0, "y_min": 42.0, "x_max": 58.0, "y_max": 68.0}
        elif "chiều cao" in description or "mặt đứng" in description:
            # Tọa độ cao độ tầng 1
            return {"x_min": 15.0, "y_min": 60.0, "x_max": 45.0, "y_max": 85.0}
        else:
            # Vùng mặc định
            offset = (issue_num * 15) % 60
            return {"x_min": 20.0 + offset, "y_min": 30.0 + offset, "x_max": 45.0 + offset, "y_max": 55.0 + offset}

drawing_grounding = DrawingGroundingEngine()
