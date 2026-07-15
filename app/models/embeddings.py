from __future__ import annotations

from functools import lru_cache
from typing import Any
from app.core.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> Any:
    """加载本地中文多语种嵌入模型。

    课程要求必须使用 models 目录中的模型，这里选用 MiniLM 作为向量检索编码器。
    """

    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(str(settings.embedding_model_dir))


def embed_texts(texts: list[str]) -> list[list[float]]:
    """把文本列表编码为向量。"""

    model = get_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()


def embed_query(text: str) -> list[float]:
    """把单条查询编码为向量。"""

    model = get_embedding_model()
    vector = model.encode([text], normalize_embeddings=True)[0]
    return vector.tolist()
