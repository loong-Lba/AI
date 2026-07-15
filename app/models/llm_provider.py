from __future__ import annotations

import json
from typing import Iterable
from openai import OpenAI
from app.core.config import settings


class LLMProvider:
    """远程 OpenAI 兼容模型包装。

    本地没有生成式大模型，因此这里用可配置远程接口承接回答生成。
    若用户未配置 API，则项目仍可完成检索与业务流演示，只是返回降级提示。
    """

    def __init__(self) -> None:
        self._client = None
        if settings.llm_base_url and settings.llm_api_key:
            self._client = OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)

    @property
    def configured(self) -> bool:
        return self._client is not None

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        """同步生成完整文本。"""

        if not self._client:
            return (
                "远程生成模型未配置。当前项目的本地 embedding 与 reranker 已可用，"
                "但请设置 OPENAI_COMPAT_BASE_URL、OPENAI_COMPAT_API_KEY 和 OPENAI_COMPAT_MODEL 后再生成自然语言回答。"
            )

        response = self._client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or "模型没有返回内容"

    def stream_text(self, system_prompt: str, user_prompt: str) -> Iterable[str]:
        """按增量流式生成文本。

        FastAPI 的 SSE 接口会逐段把这里的输出推送给前端。
        """

        if not self._client:
            yield (
                "远程生成模型未配置。请设置 OPENAI_COMPAT_BASE_URL、OPENAI_COMPAT_API_KEY 和 OPENAI_COMPAT_MODEL。"
            )
            return

        stream = self._client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            if delta:
                yield delta
