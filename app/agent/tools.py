from __future__ import annotations

from app.mcp.client import MCPToolClient


_mcp_client = MCPToolClient()


def lookup_user_email(username: str) -> dict:
    """根据用户名查询邮箱。

    适用场景：用户说“给某个人发送验证码”“查一下某人的邮箱”。
    参数：
    - username: 用户名，例如 cc
    """

    return _mcp_client.call_tool("lookup_user_email", username=username)


def send_verification_code(receiver: str) -> dict:
    """给邮箱发送验证码。

    适用场景：已知邮箱后，需要生成并发送验证码。
    参数：
    - receiver: 收件邮箱
    """

    return _mcp_client.call_tool("send_verification_code", receiver=receiver)


def verify_code(receiver: str, code: str) -> dict:
    """校验邮箱验证码。

    适用场景：用户提供邮箱和验证码后进行验证。
    """

    return _mcp_client.call_tool("verify_code", receiver=receiver, code=code)


def search_graph(disease: str, relation: str) -> dict:
    """查询本地医疗知识图谱。

    支持 relation 取值示例：症状、药物、科室、检查、能吃、不能吃、菜肴、并发症、分类、治疗。
    当用户的问题明显属于疾病知识查询时优先调用本工具。
    """

    return _mcp_client.call_tool("search_graph", disease=disease, relation=relation)


def search_docs(query: str, top_k: int = 6) -> dict:
    """查询本地向量知识库。

    当图谱信息不足、需要补充描述性知识时调用本工具。
    """

    return _mcp_client.call_tool("search_docs", query=query, top_k=top_k)


def rerank_hits(query: str, items: list[dict], top_k: int = 4) -> dict:
    """对召回结果重排。

    当 search_docs 返回了多条候选结果，且需要更精确筛选时调用。
    """

    return _mcp_client.call_tool("rerank_hits", query=query, items=items, top_k=top_k)


def search_code_evidence(query: str, top_k: int = 3) -> dict:
    """检索项目代码证据。

    用于回答“哪个文件负责验证码”“哪里实现了向量入库”这类问题。
    """

    return _mcp_client.call_tool("search_code_evidence", query=query, top_k=top_k)
