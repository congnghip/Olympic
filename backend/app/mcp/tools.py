from typing import Dict, Any, List

class MCPToolsRegistry:
    """
    Đăng ký danh mục các Tool của MCP Server theo chuẩn Model Context Protocol.
    Cho phép AI Agent (Claude, Qwen, Gemini) gọi các công cụ này để tương tác với Tầng 1.
    """

    @staticmethod
    def get_tools_manifest() -> List[Dict[str, Any]]:
        return [
            {
                "name": "parse_notice_document",
                "description": "Bóc tách văn bản công văn hành chính (PDF/scan) thành danh sách các vấn đề vi phạm kỹ thuật.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "notice_text": {"type": "string", "description": "Nội dung văn bản công văn thô"}
                    },
                    "required": ["notice_text"]
                }
            },
            {
                "name": "get_drawing_vector_layer",
                "description": "Trích xuất lớp hình học vector, lưới trục tọa độ và số đo từ bản vẽ CAD/PDF.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "drawing_id": {"type": "string", "description": "UUID của bản vẽ"},
                        "layer_name": {"type": "string", "description": "Tên layer: dimensions, walls, axes"}
                    },
                    "required": ["drawing_id"]
                }
            },
            {
                "name": "query_building_code",
                "description": "Tra cứu cơ sở dữ liệu Quy chuẩn Kỹ thuật Xây dựng Việt Nam (QCVN 06:2022, QCVN 01:2021).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Nội dung cần tra cứu (ví dụ: chiều rộng vế thang, khoảng lùi)"}
                    },
                    "required": ["query"]
                }
            }
        ]

    @staticmethod
    def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi công cụ được gọi bởi AI qua MCP"""
        if tool_name == "parse_notice_document":
            from app.services.ai.docling_parser import docling_parser
            raw_text = arguments.get("notice_text", "")
            return {"status": "success", "issues": docling_parser.parse_notice_text(raw_text)}

        elif tool_name == "get_drawing_vector_layer":
            return {
                "status": "success",
                "drawing_id": arguments.get("drawing_id"),
                "grid_axes": ["Trục 1", "Trục 2", "Trục 3", "Trục A", "Trục B"],
                "units": "mm",
                "scale": "1:100"
            }

        elif tool_name == "query_building_code":
            q = arguments.get("query", "").lower()
            if "thang" in q:
                return {
                    "standard": "QCVN 06:2022/BXD",
                    "article": "Mục 3.2.1",
                    "requirement": "Bề rộng bản thang của các lối thoát nạn không được nhỏ hơn chiều rộng lối đi và không nhỏ hơn 1.20 m đối với nhà hỗn hợp hoặc 0.90 m đối với nhà ở dưới 3 tầng."
                }
            elif "khoảng lùi" in q:
                return {
                    "standard": "QCVN 01:2021/BXD",
                    "article": "Mục 2.6.2",
                    "requirement": "Khoảng lùi công trình đối với tuyến đường có lộ giới dưới 19m và công trình cao trên 19m tối thiểu là 3m; khoảng lùi phía sau tối thiểu 1.0m đối với nhà ở riêng lẻ đô thị."
                }
            return {
                "standard": "QCVN 01:2021/BXD",
                "article": "Quy định chung",
                "requirement": "Tuân thủ chỉ giới xây dựng và mật độ xây dựng tối đa theo đồ án quy hoạch phân khu đã được phê duyệt."
            }

        return {"status": "error", "message": f"Không tìm thấy tool: {tool_name}"}

mcp_tools = MCPToolsRegistry()
