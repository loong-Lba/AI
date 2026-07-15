from __future__ import annotations

import uvicorn
from app.core.config import settings


if __name__ == "__main__":
    # 课程项目默认直接启动 FastAPI 主服务。
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=False,
    )
