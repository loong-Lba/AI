from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from app.core.config import settings
from app.core.schemas import RetrievalHit
from app.models.embeddings import embed_query, embed_texts


class LocalVectorStore:
    """极简本地向量库。

    这里不用额外数据库，直接把向量和元数据落盘到 JSON，便于课程项目本地运行。
    """

    def __init__(self, store_path: Path | None = None) -> None:
        self.store_path = store_path or settings.index_dir / "doc_index.json"
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.store_path.exists():
            self._save([])

    def _load(self) -> list[dict]:
        return json.loads(self.store_path.read_text(encoding="utf-8"))

    def _save(self, payload: list[dict]) -> None:
        self.store_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_document(self, title: str, content: str, source_id: str, metadata: dict | None = None) -> int:
        """切块后写入本地索引。"""

        chunks = self._split_text(content)
        vectors = embed_texts(chunks)
        records = [record for record in self._load() if record["source_id"] != source_id]

        for idx, (chunk, vector) in enumerate(zip(chunks, vectors)):
            records.append(
                {
                    "chunk_id": f"{source_id}:{idx}",
                    "source_id": source_id,
                    "title": title,
                    "content": chunk,
                    "vector": vector,
                    "metadata": metadata or {},
                }
            )
        self._save(records)
        return len(chunks)

    def has_source(self, source_id: str) -> bool:
        """判断某个来源是否已经入库。"""

        return any(record["source_id"] == source_id for record in self._load())

    def search(self, query: str, top_k: int | None = None) -> list[RetrievalHit]:
        """做一次余弦相似度召回。"""

        records = self._load()
        if not records:
            return []

        query_vector = np.array(embed_query(query), dtype=np.float32)
        results: list[RetrievalHit] = []
        for record in records:
            vector = np.array(record["vector"], dtype=np.float32)
            score = float(np.dot(query_vector, vector))
            results.append(
                RetrievalHit(
                    source_type="doc",
                    source_id=record["source_id"],
                    title=record["title"],
                    content=record["content"],
                    score=score,
                    metadata={**record.get("metadata", {}), "chunk_id": record["chunk_id"]},
                )
            )

        results.sort(key=lambda item: item.score, reverse=True)
        return results[: (top_k or settings.retrieval_top_k)]

    def _split_text(self, text: str) -> list[str]:
        """按固定窗口切块，避免引入额外依赖。"""

        chunk_size = settings.chunk_size
        overlap = settings.chunk_overlap
        chunks: list[str] = []
        cursor = 0
        clean_text = text.strip()
        while cursor < len(clean_text):
            end = cursor + chunk_size
            chunks.append(clean_text[cursor:end])
            if end >= len(clean_text):
                break
            cursor = max(end - overlap, cursor + 1)
        return chunks
