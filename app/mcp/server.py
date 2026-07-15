from __future__ import annotations

from fastmcp import FastMCP
from app.core.schemas import RetrievalHit, ToolEnvelope
from app.services.graph_service import GraphService
from app.services.user_service import UserService
from app.services.verification_service import VerificationService
from app.services.mail_service import MailService
from app.services.vector_store import LocalVectorStore
from app.services.code_search_service import CodeSearchService
from app.services.bootstrap import bootstrap_demo_docs
from app.models.reranker import rerank_hits


mcp = FastMCP("agentic-rag")

_graph_service = GraphService()
_user_service = UserService()
_verification_service = VerificationService()
_mail_service = MailService()
_vector_store = LocalVectorStore()
_code_search_service = CodeSearchService()
_docs_bootstrapped = False


@mcp.tool(name="lookup_user_email", description="根据用户名查询邮箱")
def lookup_user_email(username: str) -> dict:
    """通过用户名获取邮箱。"""

    email = _user_service.get_email_by_username(username)
    return ToolEnvelope(ok=bool(email), data={"username": username, "email": email}).model_dump()


@mcp.tool(name="send_verification_code", description="给邮箱发送验证码")
def send_verification_code(receiver: str) -> dict:
    """生成并发送验证码。"""

    code = _verification_service.issue_code(receiver)
    payload = _mail_service.send_code(receiver, code)
    return ToolEnvelope(ok=True, data=payload).model_dump()


@mcp.tool(name="verify_code", description="校验邮箱验证码")
def verify_code(receiver: str, code: str) -> dict:
    """验证验证码是否正确。"""

    ok = _verification_service.verify_code(receiver, code)
    return ToolEnvelope(ok=ok, data={"receiver": receiver, "verified": ok}).model_dump()


@mcp.tool(name="search_graph", description="查询本地医疗知识图谱")
def search_graph(disease: str, relation: str) -> dict:
    """按疾病和关系查询图谱数据。"""

    return ToolEnvelope(ok=True, data=_graph_service.raw_lookup(disease, relation)).model_dump()


@mcp.tool(name="search_docs", description="查询本地向量知识库")
def search_docs(query: str, top_k: int = 6) -> dict:
    """从本地向量库中召回相关文档片段。"""

    global _docs_bootstrapped
    if not _docs_bootstrapped:
        bootstrap_demo_docs(_vector_store)
        _docs_bootstrapped = True
    hits = [item.model_dump() for item in _vector_store.search(query, top_k=top_k)]
    return ToolEnvelope(ok=True, data=hits).model_dump()


@mcp.tool(name="rerank_hits", description="对检索结果进行重排")
def rerank_hits_tool(query: str, items: list[dict], top_k: int = 4) -> dict:
    """对召回结果进行二阶段排序。"""

    ranked = rerank_hits(query, hits=[RetrievalHit(**item) for item in items], top_k=top_k)
    return ToolEnvelope(ok=True, data=[item.model_dump() for item in ranked]).model_dump()


@mcp.tool(name="search_code_evidence", description="查询项目中的代码证据")
def search_code_evidence(query: str, top_k: int = 3) -> dict:
    """用于回答哪个文件负责什么逻辑。"""

    hits = [item.model_dump() for item in _code_search_service.search(query, top_k=top_k)]
    return ToolEnvelope(ok=True, data=hits).model_dump()


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=9000, path="/mcp")
