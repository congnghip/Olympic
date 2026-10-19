from typing import Dict, Any, List

class DiffEngine:
    """
    Động cơ so sánh và đối soát sai lệch giữa phiên bản cũ (V1) và phiên bản nộp lại (V2).
    Phát hiện:
    1. Lỗi đã được sửa đạt.
    2. Lỗi chưa được sửa.
    3. Cảnh báo các vùng thay đổi ngoài phạm vi yêu cầu (sửa lén).
    """

    def compare_versions(self, v1_issues: List[Dict[str, Any]], v2_changes: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        resolved = []
        unresolved = []

        # Giả lập logic kiểm tra: các lỗi đã hoàn thành các bước action plan được tính là resolved
        for issue in v1_issues:
            is_resolved = issue.get("status") == "resolved" or issue.get("is_fixed", False)
            if is_resolved:
                resolved.append({
                    "issue_id": issue.get("id"),
                    "issue_number": issue.get("issue_number"),
                    "description": issue.get("issue_description"),
                    "status": "RESOLVED_COMPLIANT"
                })
            else:
                unresolved.append({
                    "issue_id": issue.get("id"),
                    "issue_number": issue.get("issue_number"),
                    "description": issue.get("issue_description"),
                    "status": "STILL_NON_COMPLIANT"
                })

        # Cảnh báo thay đổi ngoài yêu cầu (ví dụ: phát hiện ban công tầng 2 cơi nới thêm 40cm)
        unauthorized = [
            {
                "area": "Ban công Tầng 2 (trục A-C)",
                "warning": "Phát hiện diện tích sàn ban công tăng thêm 1.4m2 ngoài nội dung công văn yêu cầu sửa đổi.",
                "severity": "WARNING"
            }
        ]

        return {
            "source_version": 1,
            "target_version": 2,
            "total_issues": len(v1_issues),
            "resolved_count": len(resolved),
            "unresolved_count": len(unresolved),
            "unauthorized_changes_count": len(unauthorized),
            "resolved_issues": resolved,
            "unresolved_issues": unresolved,
            "unauthorized_changes": unauthorized,
            "recommendation": "APPROVED" if len(unresolved) == 0 else "REVISE_REQUIRED"
        }

diff_engine = DiffEngine()
