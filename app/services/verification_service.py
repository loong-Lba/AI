from __future__ import annotations

import random
import time
from app.core.config import settings


class VerificationService:
    """本地内存验证码服务。"""

    def __init__(self) -> None:
        self._store: dict[str, dict] = {}

    def issue_code(self, receiver: str) -> str:
        """生成并缓存 4 位验证码。"""

        code = "".join(str(random.randint(0, 9)) for _ in range(4))
        self._store[receiver] = {
            "code": code,
            "expires_at": time.time() + settings.verification_ttl_seconds,
        }
        return code

    def verify_code(self, receiver: str, code: str) -> bool:
        """校验验证码是否正确且未过期。"""

        item = self._store.get(receiver)
        if not item:
            return False
        if time.time() > item["expires_at"]:
            self._store.pop(receiver, None)
            return False
        return item["code"] == code

    def get_debug_code(self, receiver: str) -> str | None:
        """开发模式下返回当前验证码，方便本地演示。"""

        item = self._store.get(receiver)
        return item["code"] if item else None
