from __future__ import annotations

import asyncio
from fastmcp import Client
from app.core.config import settings
from app.mcp import server as local_server


class MCPToolClient:
    """MCP 客户端包装。

    优先通过 HTTP 调用本地 MCP Server；如果当前环境里还没把 Server 完全拉起，
    则自动回退到同进程本地调用，避免课程演示时因为时序问题直接失败。
    """

    def call_tool(self, tool_name: str, **kwargs):
        """同步调用 MCP 工具。

        课程项目默认优先本地调用，确保带状态的开发模式验证码流程在同一进程内可复现；
        如果后续你想单独部署 MCP 服务，可把这里改回远程优先。
        """

        try:
            return self._call_local(tool_name, **kwargs)
        except Exception:
            return asyncio.run(self._call_remote(tool_name, **kwargs))

    async def _call_remote(self, tool_name: str, **kwargs):
        async with Client(settings.mcp_server_url) as client:
            result = await client.call_tool(tool_name, kwargs)
            if hasattr(result, "data"):
                return result.data
            return result

    def _call_local(self, tool_name: str, **kwargs):
        dispatch = {
            "lookup_user_email": local_server.lookup_user_email,
            "send_verification_code": local_server.send_verification_code,
            "verify_code": local_server.verify_code,
            "search_graph": local_server.search_graph,
            "search_docs": local_server.search_docs,
            "rerank_hits": local_server.rerank_hits_tool,
            "search_code_evidence": local_server.search_code_evidence,
        }
        return dispatch[tool_name](**kwargs)
