from __future__ import annotations

from functools import lru_cache
from typing import Any
from app.core.config import settings
from app.core.schemas import RetrievalHit


@lru_cache(maxsize=1)
def get_reranker() -> Any:
    """加载本地重排模型。

    该模型来自 models 目录中的 BAAI/bge-reranker-large，用于二阶段排序。
    """

    from sentence_transformers import CrossEncoder

    return CrossEncoder(str(settings.reranker_model_dir))


def rerank_hits(query: str, hits: list[RetrievalHit], top_k: int | None = None) -> list[RetrievalHit]:
    """对多源检索结果进行交叉编码重排。"""

    if not hits:
        return []

    reranker = get_reranker()
    pairs = [[query, hit.content] for hit in hits]
    scores = reranker.predict(pairs)

    ranked: list[RetrievalHit] = []
    for hit, score in zip(hits, scores):
        ranked.append(hit.model_copy(update={"score": float(score)}))

    ranked.sort(key=lambda item: item.score, reverse=True)
    limit = top_k or settings.rerank_top_k
    return ranked[:limit]
