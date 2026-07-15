from __future__ import annotations

import os
from pathlib import Path
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """项目全局配置。

    这里把路径、模型、远程 LLM 和运行参数统一收口，方便课程项目演示时直接改环境变量。
    """

    project_root: Path = Path("D:/daima/rag_agent")
    data_dir: Path = Path("D:/daima/rag_agent/data")
    runtime_dir: Path = Path("D:/daima/rag_agent/data/runtime")
    index_dir: Path = Path("D:/daima/rag_agent/data/indexes")

    embedding_model_dir: Path = Path(
        "D:/daima/rag_agent/models/embedding_model/models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2/snapshots/e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
    )
    reranker_model_dir: Path = Path(
        "D:/daima/rag_agent/models/bge-reranker-large_v1/models--BAAI--bge-reranker-large/snapshots/55611d7bca2a7133960a6d3b71e083071bbfc312"
    )

    llm_base_url: str | None = os.getenv("OPENAI_COMPAT_BASE_URL")
    llm_api_key: str | None = os.getenv("OPENAI_COMPAT_API_KEY")
    llm_model: str = os.getenv("OPENAI_COMPAT_MODEL", "claude-opus-4-8")

    app_host: str = os.getenv("APP_HOST", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    mcp_host: str = os.getenv("MCP_HOST", "127.0.0.1")
    mcp_port: int = int(os.getenv("MCP_PORT", "9000"))
    mcp_path: str = os.getenv("MCP_PATH", "/mcp")

    retrieval_top_k: int = int(os.getenv("RETRIEVAL_TOP_K", "6"))
    rerank_top_k: int = int(os.getenv("RERANK_TOP_K", "4"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "280"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "40"))
    verification_ttl_seconds: int = int(os.getenv("VERIFICATION_TTL_SECONDS", "300"))

    sqlite_path: Path = Path("D:/daima/rag_agent/data/runtime/users.db")
    code_index_glob: str = "app/**/*.py"

    @property
    def mcp_server_url(self) -> str:
        return f"http://{self.mcp_host}:{self.mcp_port}{self.mcp_path}"


settings = Settings()
