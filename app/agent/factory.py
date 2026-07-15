from __future__ import annotations

import re
from typing import Iterable

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import (
    lookup_user_email,
    rerank_hits,
    search_code_evidence,
    search_docs,
    search_graph,
    send_verification_code,
    verify_code,
)
from app.models.llm_provider import LLMProvider


class AgentFacade:
    """课程项目用的 Agent 门面。

    优先使用远程模型 + 工具调用；当远程模型未配置时，自动退化为本地启发式流程，
    确保项目依然能演示 Agentic-RAG 的核心链路。
    """

    def __init__(self) -> None:
        self.llm_provider = LLMProvider()

    def ask(self, message: str) -> str:
        """返回完整回答。"""

        return self._ask_with_local_router(message)

    def stream(self, message: str) -> Iterable[str]:
        """返回流式回答。"""

        answer = self.ask(message)
        chunk_size = 24
        for index in range(0, len(answer), chunk_size):
            yield answer[index:index + chunk_size]

    def _ask_with_local_router(self, message: str) -> str:
        """本地保底路由。

        当远程生成模型未配置时，仍然能完成课程要求中的主要业务链路；
        当需要自然语言总结但没有更强工具证据时，再调用远程 OpenAI 兼容模型润色输出。
        """

        if any(keyword in message for keyword in ["校验验证码", "验证验证码", "检验验证码", "验证码是否正确", "验证码对不对"]):
            email = self._extract_email(message)
            code = self._extract_code(message)
            if not email or not code:
                return "请同时提供邮箱和验证码。"
            result = verify_code(email, code)
            ok = ((result or {}).get("data") or {}).get("verified")
            return "验证码验证成功。" if ok else "验证码错误或已过期。"

        if any(keyword in message for keyword in ["发送验证码", "发送邮件", "发验证码", "发邮件"]):
            username = self._extract_username(message)
            if not username:
                return "请提供需要发送验证码的用户名。"
            email_result = lookup_user_email(username)
            email = ((email_result or {}).get("data") or {}).get("email")
            if not email:
                return "未找到该用户名绑定的邮箱，请确认用户名是否正确。"
            send_result = send_verification_code(email)
            debug_code = ((send_result or {}).get("data") or {}).get("debug_code")
            return f"已为用户 {username} 生成验证码并发送到 {email}。开发模式验证码：{debug_code}。"

        if any(keyword in message for keyword in ["哪个文件", "哪段代码", "哪里实现", "接口负责"]):
            code_hits = ((search_code_evidence(message) or {}).get("data") or [])
            if not code_hits:
                return "未检索到相关代码证据。"
            lines = ["根据代码检索结果，相关位置如下："]
            for hit in code_hits[:3]:
                lines.append(f"- {hit['title']}: {hit['content'][:120].replace(chr(10), ' ')}")
            return "\n".join(lines)

        graph_answer = self._build_graph_answer(message)
        if graph_answer:
            return graph_answer

        doc_hits = ((search_docs(message) or {}).get("data") or [])
        if doc_hits:
            ranked = ((rerank_hits(message, doc_hits) or {}).get("data") or doc_hits)[:3]
            context = "\n".join(f"- {hit['content']}" for hit in ranked)
            if self.llm_provider.configured:
                return self.llm_provider.generate_text(
                    SYSTEM_PROMPT,
                    f"用户问题：{message}\n可用知识片段：\n{context}\n请基于这些片段用中文简洁回答，并说明这是根据本地知识库整理的。",
                )
            lines = ["根据本地知识库检索结果："]
            lines.extend(f"- {hit['content']}" for hit in ranked)
            return "\n".join(lines)

        return self.llm_provider.generate_text(
            SYSTEM_PROMPT,
            f"用户问题：{message}\n请在没有工具证据时明确说明信息有限。",
        )

    def _build_graph_answer(self, message: str) -> str | None:
        """根据问题拼出图谱查询回答。"""

        disease = self._extract_disease(message)
        relation = self._extract_relation(message)
        if not disease or not relation:
            return None
        result = search_graph(disease, relation)
        values = (((result or {}).get("data") or {}).get("values") or [])
        if not values:
            return None
        return f"根据图谱结果，{disease}的{relation}包括：{'、'.join(values)}。"

    def _extract_username(self, message: str) -> str | None:
        match = re.search(r"给([a-zA-Z0-9_\-]+)", message)
        return match.group(1) if match else None

    def _extract_email(self, message: str) -> str | None:
        match = re.search(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", message)
        return match.group(0) if match else None

    def _extract_code(self, message: str) -> str | None:
        match = re.search(r"验证码[为:： ]*(\d{4,6})", message)
        if match:
            return match.group(1)
        fallback = re.search(r"(\d{4,6})", message)
        return fallback.group(1) if fallback else None

    def _extract_disease(self, message: str) -> str | None:
        for disease in ["糖尿病", "高血压"]:
            if disease in message:
                return disease
        return None

    def _extract_relation(self, message: str) -> str | None:
        for relation in ["症状", "药物", "科室", "检查", "能吃", "不能吃", "菜肴", "并发症", "分类", "治疗"]:
            if relation in message:
                return relation
        return None


def build_agent() -> AgentFacade:
    """构建项目 Agent。"""

    return AgentFacade()
