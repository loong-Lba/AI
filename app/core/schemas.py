from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class RetrievalHit(BaseModel):
    """统一的检索结果结构，便于多源结果合并后再重排。"""

    source_type: Literal["doc", "graph", "code"]
    source_id: str
    title: str
    content: str
    score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    """导入文本到本地向量库的请求体。"""

    title: str
    content: str
    source_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    """通用对话请求。"""

    message: str


class VerificationState(BaseModel):
    """验证码缓存对象。"""

    receiver: str
    code: str
    expires_at: float


class ToolEnvelope(BaseModel):
    """MCP 工具调用的标准输出包装。"""

    ok: bool = True
    data: Any = None
    error: str | None = None


class HealthResponse(BaseModel):
    """健康检查输出。"""

    service: str
    llm_configured: bool
    embedding_model_exists: bool
    reranker_model_exists: bool
    sqlite_ready: bool
    mcp_server_url: str
