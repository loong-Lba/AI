from __future__ import annotations

import json
from fastapi import APIRouter
from starlette.responses import StreamingResponse
from app.agent.singleton import get_agent


router = APIRouter(tags=["chat"])
_agent = get_agent()


@router.get("/chat")
def chat(messages: str):
    """SSE 流式问答接口。"""

    def event_stream():
        for piece in _agent.stream(messages):
            yield f"data: {json.dumps({'content': piece}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
