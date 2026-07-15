from __future__ import annotations

from app.core.sample_data import DEFAULT_DOCS
from app.services.vector_store import LocalVectorStore


def bootstrap_demo_docs(vector_store: LocalVectorStore) -> None:
    """初始化课程演示文档。

    首次启动时把示例知识写进本地向量库，后续重复启动不会重复追加。
    """

    for doc in DEFAULT_DOCS:
        if not vector_store.has_source(doc["source_id"]):
            vector_store.add_document(
                title=doc["title"],
                content=doc["content"],
                source_id=doc["source_id"],
                metadata=doc["metadata"],
            )
