from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.api.routes_ingest import router as ingest_router
from app.core.config import settings
from app.core.schemas import HealthResponse
from app.models.llm_provider import LLMProvider
from app.services.user_service import UserService
from app.services.vector_store import LocalVectorStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期。

    启动时只做轻量初始化，避免首次运行因为大模型依赖未装完而导致服务完全无法启动。
    向量库会在真正使用时再进行懒初始化。
    """

    UserService()
    app.state.vector_store = LocalVectorStore()
    yield


app = FastAPI(
    title="Agentic-RAG Course Project",
    description="基于 MCP、多源检索与本地 embedding/reranker 的课程版 Agentic-RAG 项目",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ingest_router)


@app.get("/")
def index() -> FileResponse:
    """返回前端演示页面。"""

    return FileResponse(Path("D:/daima/rag_agent/app/static/index.html"))


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """健康检查接口。"""

    llm_provider = LLMProvider()
    return HealthResponse(
        service="agentic-rag",
        llm_configured=llm_provider.configured,
        embedding_model_exists=settings.embedding_model_dir.exists(),
        reranker_model_exists=settings.reranker_model_dir.exists(),
        sqlite_ready=settings.sqlite_path.exists(),
        mcp_server_url=settings.mcp_server_url,
    )
