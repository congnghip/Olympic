from fastapi import APIRouter, Request
from app.mcp.tools import mcp_tools

mcp_router = APIRouter(prefix="/mcp", tags=["Model Context Protocol"])

@mcp_router.get("/tools")
async def list_tools():
    """Endpoint liệt kê danh sách MCP Tools cho AI Agent"""
    return {
        "tools": mcp_tools.get_tools_manifest()
    }

@mcp_router.post("/execute")
async def execute_mcp_tool(request: Request):
    """Endpoint thực thi MCP Tool qua chuẩn JSON-RPC"""
    body = await request.json()
    tool_name = body.get("name")
    arguments = body.get("arguments", {})
    result = mcp_tools.execute_tool(tool_name, arguments)
    return {
        "tool": tool_name,
        "result": result
    }
