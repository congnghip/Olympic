import httpx
from app.core.config import settings

class WorkflowService:
    """
    Quản lý luồng công việc phê duyệt hồ sơ theo chuẩn BPMN 2.0 (Flowable REST API)
    Có cơ chế Local State Machine fallback nếu Flowable chưa khởi động xong.
    """
    def __init__(self):
        self.api_url = settings.FLOWABLE_API_URL
        self.auth = (settings.FLOWABLE_ADMIN_USER, settings.FLOWABLE_ADMIN_PASSWORD)

    async def start_dossier_process(self, dossier_code: str, version_number: int) -> str:
        """Kích hoạt tiến trình BPMN mới cho hồ sơ"""
        payload = {
            "processDefinitionKey": "dossierApprovalProcess",
            "businessKey": f"{dossier_code}-V{version_number}",
            "variables": [
                {"name": "dossierCode", "value": dossier_code},
                {"name": "version", "value": version_number},
                {"name": "status", "value": "SUBMITTED"}
            ]
        }
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.post(
                    f"{self.api_url}/runtime/process-instances",
                    json=payload,
                    auth=self.auth
                )
                if res.status_code in [200, 201]:
                    data = res.json()
                    return data.get("id", f"mock-flow-{dossier_code}-v{version_number}")
        except Exception:
            pass
        # Fallback local instance ID
        return f"proc-instance-{dossier_code}-v{version_number}"

    async def transition_state(self, current_status: str, action: str) -> str:
        """Chuyển đổi trạng thái hồ sơ theo máy trạng thái (State Machine)"""
        transitions = {
            ("draft", "submit"): "submitted",
            ("submitted", "analyze_ai"): "ai_analyzing",
            ("ai_analyzing", "complete_ai"): "under_review",
            ("under_review", "require_revision"): "revision_required",
            ("under_review", "approve"): "approved",
            ("under_review", "reject"): "rejected",
            ("revision_required", "resubmit"): "submitted"
        }
        return transitions.get((current_status, action), current_status)

workflow_service = WorkflowService()
