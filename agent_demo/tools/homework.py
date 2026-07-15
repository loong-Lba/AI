from typing import Optional

from langchain_core.tools import StructuredTool, tool
from pydantic import BaseModel, Field


@tool
def send_email_by_decorator(
    to_email: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
) -> str:
    """发送邮件工具（tool 装饰器方式）。"""
    # 使用伪代码模拟真实发信逻辑
    pseudo_result = {
        "provider": "smtp.example.com",
        "action": "send",
        "to": to_email,
        "cc": cc,
        "subject": subject,
        "body": body,
        "status": "success",
        "message_id": "mock-message-id-001",
    }
    return f"decorator tool execute result: {pseudo_result}"


class SendEmailInput(BaseModel):
    to_email: str = Field(description="收件人邮箱")
    subject: str = Field(description="邮件主题")
    body: str = Field(description="邮件正文")
    cc: Optional[str] = Field(default=None, description="抄送邮箱")


def send_email_by_structured(
    to_email: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
) -> str:
    """发送邮件工具（StructuredTool 方式）。"""
    pseudo_result = {
        "provider": "smtp.example.com",
        "action": "send",
        "to": to_email,
        "cc": cc,
        "subject": subject,
        "body": body,
        "status": "success",
        "message_id": "mock-message-id-002",
    }
    return f"structured tool execute result: {pseudo_result}"


send_email_structured_tool = StructuredTool.from_function(
    func=send_email_by_structured,
    name="send_email_structured_tool",
    description="发送邮件工具，适合给 Agent 使用。",
    args_schema=SendEmailInput,
)


if __name__ == "__main__":
    decorator_result = send_email_by_decorator.invoke(
        {
            "to_email": "user@example.com",
            "subject": "欢迎使用 Agent 工具",
            "body": "这是一封通过 tool 装饰器方式发送的伪代码邮件。",
            "cc": "leader@example.com",
        }
    )
    print(decorator_result)

    structured_result = send_email_structured_tool.invoke(
        {
            "to_email": "user@example.com",
            "subject": "欢迎使用 StructuredTool",
            "body": "这是一封通过 StructuredTool 方式发送的伪代码邮件。",
            "cc": "leader@example.com",
        }
    )
    print(structured_result)
