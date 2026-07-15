from __future__ import annotations

from app.core.config import settings
from app.mcp.server import mcp


if __name__ == "__main__":
    # 课程项目的 MCP 工具服务入口。
    mcp.run(
        transport="http",
        host=settings.mcp_host,
        port=settings.mcp_port,
        path=settings.mcp_path,
    )
