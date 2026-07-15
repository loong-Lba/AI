from __future__ import annotations

from functools import lru_cache
from app.agent.factory import AgentFacade


@lru_cache(maxsize=1)
def get_agent() -> AgentFacade:
    """返回全局单例 Agent。

    验证码等带状态的业务需要共享同一个内存态，否则发送和校验会落在不同实例上。
    """

    return AgentFacade()
