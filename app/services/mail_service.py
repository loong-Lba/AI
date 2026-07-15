from __future__ import annotations


class MailService:
    """开发模式邮件服务。

    真实 SMTP 在课程场景里经常因为权限或授权码缺失无法直接演示，所以这里用本地回显模式保底。
    """

    def send_code(self, receiver: str, code: str) -> dict:
        """模拟发送验证码。"""

        return {
            "message": "开发模式下验证码已生成，未真正发送邮件。",
            "receiver": receiver,
            "debug_code": code,
        }
