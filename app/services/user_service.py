from __future__ import annotations

import sqlite3
from app.core.config import settings
from app.core.sample_data import SAMPLE_USERS


class UserService:
    """用户信息服务。

    课件里是 MySQL，这里默认用 SQLite 做本地化替代，保证项目开箱可跑。
    """

    def __init__(self) -> None:
        settings.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(settings.sqlite_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user (
                    username TEXT PRIMARY KEY,
                    email TEXT NOT NULL
                )
                """
            )
            existing = conn.execute("SELECT COUNT(*) FROM user").fetchone()[0]
            if existing == 0:
                conn.executemany(
                    "INSERT INTO user(username, email) VALUES(?, ?)",
                    [(item["username"], item["email"]) for item in SAMPLE_USERS],
                )
            conn.commit()

    def get_email_by_username(self, username: str) -> str | None:
        """根据用户名查询邮箱。"""

        with self._connect() as conn:
            row = conn.execute(
                "SELECT email FROM user WHERE username = ?",
                (username,),
            ).fetchone()
            return row[0] if row else None
