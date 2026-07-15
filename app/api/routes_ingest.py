from __future__ import annotations

from fastapi import APIRouter
from app.core.schemas import IngestRequest
from app.services.vector_store import LocalVectorStore


router = APIRouter(tags=["ingest"])


@router.post("/ingest")
def ingest_document(payload: IngestRequest):
    """导入文本到本地向量库。"""

    store = LocalVectorStore()
    source_id = payload.source_id or payload.title
    chunks = store.add_document(
        title=payload.title,
        content=payload.content,
        source_id=source_id,
        metadata=payload.metadata,
    )
    return {
        "code": 200,
        "msg": "导入成功",
        "data": {"source_id": source_id, "chunks": chunks},
    }
