from __future__ import annotations

from pathlib import Path
from app.core.config import settings
from app.core.schemas import RetrievalHit
from app.models.embeddings import embed_query, embed_texts
import numpy as np


class CodeSearchService:
    """代码证据检索服务。

    当用户问“哪个文件负责什么逻辑”时，Agent 可以基于这个服务返回代码证据而不是凭空回答。
    """

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or settings.project_root

    def search(self, query: str, top_k: int = 3) -> list[RetrievalHit]:
        """对 Python 源码做轻量向量检索。"""

        py_files = sorted(self.root.glob(settings.code_index_glob))
        chunks: list[tuple[str, str]] = []
        for file_path in py_files:
            text = file_path.read_text(encoding="utf-8")
            for idx, chunk in enumerate(self._split_code(text)):
                chunks.append((f"{file_path}:{idx}", chunk))

        if not chunks:
            return []

        query_vector = np.array(embed_query(query), dtype=np.float32)
        content_vectors = embed_texts([item[1] for item in chunks])
        hits: list[RetrievalHit] = []
        for (chunk_id, chunk), vector in zip(chunks, content_vectors):
            score = float(np.dot(query_vector, np.array(vector, dtype=np.float32)))
            file_name = chunk_id.split(":")[0]
            hits.append(
                RetrievalHit(
                    source_type="code",
                    source_id=chunk_id,
                    title=file_name,
                    content=chunk,
                    score=score,
                    metadata={"chunk_id": chunk_id},
                )
            )
        hits.sort(key=lambda item: item.score, reverse=True)
        return hits[:top_k]

    def _split_code(self, text: str) -> list[str]:
        """按固定窗口切分代码片段。"""

        lines = text.splitlines()
        chunks: list[str] = []
        window = 30
        for start in range(0, len(lines), 20):
            chunk = "\n".join(lines[start:start + window]).strip()
            if chunk:
                chunks.append(chunk)
        return chunks
