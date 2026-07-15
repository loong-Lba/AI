from __future__ import annotations

import re
from fastapi import APIRouter
from app.agent.singleton import get_agent


router = APIRouter(tags=["auth"])
_agent = get_agent()


@router.get("/sendEmail/{username}")
def send_email(username: str):
    """发送验证码接口。

    保持和课件一致的路径风格，便于课堂演示或前端直接联调。
    """

    result = _agent.ask(f"请给{username}发送验证码")
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", result)
    code_match = re.search(r"验证码：?(\d{4,6})", result) or re.search(r"(\d{4,6})", result)
    return {
        "code": 200,
        "msg": "发送完成",
        "data": {
            "username": username,
            "email": email_match.group(0) if email_match else None,
            "debug_code": code_match.group(1) if code_match else None,
            "message": result,
        },
    }


@router.get("/verifyCode/{receiver}/{code}")
def verify_email_code(receiver: str, code: str):
    """验证码校验接口。"""

    result = _agent.ask(f"请校验验证码，邮箱为{receiver}，验证码为{code}")
    ok = "成功" in result or "通过" in result
    return {
        "code": 200 if ok else 400,
        "msg": result,
        "data": {"receiver": receiver, "verified": ok},
    }
