"""
Waste Dispatcher & Re-routing Module
Tích hợp Kev AI System One (nhận diện báo cáo tài xế + GPS) và PACO VRP Solver (tính toán lại lộ trình tức thì)
"""

from typing import List, Dict, Any, Optional
import requests
import json
from dataclasses import dataclass
from service import SolverService, SolverResult
from utils import generate_instance_content

KEV_API_URL = "http://127.0.0.1:8009/v1/systemone"

@dataclass
class WasteIncidentEvaluation:
    incident_category: str
    incident_confidence: float
    trigger_reroute: bool
    reroute_probability: float
    dispatcher_action: str
    urgency_score: float
    raw_response: Dict[str, Any]

class WasteDispatcherService:
    def __init__(self, kev_url: str = KEV_API_URL):
        self.kev_url = kev_url
        self.solver_service = SolverService()

    def evaluate_incident(
        self,
        vehicle_id: str,
        driver_report: str,
        gps_status: str,
        remaining_points_count: int
    ) -> WasteIncidentEvaluation:
        """
        Gọi Kev AI để phân tích sự cố từ báo cáo tài xế và GPS
        """
        state_text = (
            f"Phương tiện: {vehicle_id}\n"
            f"Báo cáo tài xế: {driver_report}\n"
            f"Trạng thái GPS Traccar: {gps_status}\n"
            f"Số điểm gom còn lại: {remaining_points_count}"
        )

        payload = {
            "state": state_text,
            "model": "kev-latest",
            "questions": {
                "incident_category": {
                    "type": "choice",
                    "instructions": "Phân loại bản chất sự kiện / sự cố này?",
                    "criteria": {
                        "access_blocked": "Đường bị chặn, ngõ cụt, công trình cản trở không vào được",
                        "invalid_waste": "Rác sai quy định, xà bần, nguy hiểm, từ chối thu gom",
                        "vehicle_breakdown": "Xe gặp sự cố kỹ thuật hỏng hóc, dừng hoạt động",
                        "normal_success": "Thu gom bình thường, hoàn thành tốt nhiệm vụ"
                    }
                },
                "trigger_reroute": {
                    "type": "noul",
                    "instructions": "Có cần kích hoạt thuật toán tính toán lại lộ trình (Re-route) không?"
                },
                "dispatcher_action": {
                    "type": "choice",
                    "instructions": "Hành động tức thì cho hệ thống điều phối?",
                    "criteria": {
                        "skip_and_continue": "Bỏ qua điểm này, tối ưu lại đường đi cho các điểm còn lại",
                        "dispatch_rescue_fleet": "Chuyển giao toàn bộ các điểm còn lại cho xe dự phòng khác",
                        "create_special_ticket": "Từ chối gom, tạo phiếu xử lý rác quá khổ/xà bần cho đơn vị khác",
                        "confirm_completed": "Ghi nhận nghiệm thu thành công điểm gom"
                    }
                },
                "urgency": {
                    "type": "score",
                    "instructions": "Mức độ khẩn cấp cần Điều phối viên can thiệp",
                    "criteria": [
                        "Không cần (hệ thống tự xử lý)",
                        "Cần lưu ý",
                        "Khẩn cấp (cần can thiệp ngay)"
                    ]
                }
            }
        }

        try:
            resp = requests.post(self.kev_url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            answers = data.get("answers", {})

            incident_choice = answers.get("incident_category", {})
            reroute_noul = answers.get("trigger_reroute", {})
            action_choice = answers.get("dispatcher_action", {})
            urgency_score = answers.get("urgency", {})

            reroute_prob = reroute_noul.get("noul", 0.0)
            should_reroute = reroute_prob >= 0.55

            return WasteIncidentEvaluation(
                incident_category=incident_choice.get("choice", "unknown"),
                incident_confidence=incident_choice.get("confidence", 0.0),
                trigger_reroute=should_reroute,
                reroute_probability=reroute_prob,
                dispatcher_action=action_choice.get("choice", "unknown"),
                urgency_score=urgency_score.get("score", 0.0),
                raw_response=data
            )
        except Exception as e:
            # Fallback nếu Kev tạm thời bận
            return WasteIncidentEvaluation(
                incident_category="error",
                incident_confidence=0.0,
                trigger_reroute=True,
                reroute_probability=1.0,
                dispatcher_action="manual_dispatch",
                urgency_score=2.0,
                raw_response={"error": str(e)}
            )

    def reroute_waste_tour(
        self,
        current_gps: Dict[str, float],
        remaining_points: List[Dict[str, Any]],
        depot: Dict[str, float],
        skipped_point_id: Optional[int] = None,
        vehicle_capacity: int = 100,
        num_vehicles: int = 1
    ) -> SolverResult:
        """
        Tự động loại bỏ điểm gặp sự cố và giải lại bài toán VRP để có lộ trình mới
        """
        # Lọc bỏ điểm bị bỏ qua (nếu có)
        active_customers = [
            pt for pt in remaining_points
            if pt.get("id") != skipped_point_id
        ]

        if not active_customers:
            return SolverResult(
                objective=0, vehicles=0, runtime=0,
                routes=[], raw_routes=[], success=True,
                error_message="Không còn điểm gom rác nào cần thực hiện."
            )

        # Định dạng chuẩn bị cho VRP Generator
        # Sử dụng tọa độ GPS hiện tại của xe làm điểm bắt đầu (hoặc depot)
        current_depot = {
            "x": current_gps.get("x", depot.get("x", 50.0)),
            "y": current_gps.get("y", depot.get("y", 50.0)),
            "earliest": 0.0,
            "latest": 1000.0
        }

        customers_formatted = []
        for c in active_customers:
            customers_formatted.append({
                "x": float(c.get("x", 0.0)),
                "y": float(c.get("y", 0.0)),
                "demand": int(c.get("demand", 10)),
                "earliest": float(c.get("earliest", 0.0)),
                "latest": float(c.get("latest", 1000.0)),
                "service_time": float(c.get("service_time", 10.0)),
                "type": int(c.get("type", 1))
            })

        # Lockers để trống cho bài toán gom rác thông thường
        lockers_list = []

        instance_content = generate_instance_content(
            num_vehicles=num_vehicles,
            vehicle_capacity=vehicle_capacity,
            depot=current_depot,
            customers=customers_formatted,
            lockers=lockers_list
        )

        # Chạy thuật toán PACO
        return self.solver_service.run_solver(
            instance_content=instance_content,
            solver="paco",
            size="small"
        )
