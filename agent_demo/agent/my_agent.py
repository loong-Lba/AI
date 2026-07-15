"""
创建并执行agent
"""
import asyncio

from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate

from models.my_llm import qwen_llm
from tools.my_tools import calculate_area, add



agent = create_agent(
    model=qwen_llm,
    tools=[calculate_area, add],
    system_prompt="你是一个计算AI助手，擅长数学计算"
)

# 定义提示词模板
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("human", "{question}")
    ]
)
# 定义LCEL链
chain = prompt_template | agent


# results = agent.invoke({"messages":[("human", "计算宽为10，高为5的长方形面积")]})
#
# for result in results ["messages"]:
#     result.pretty_print()

async def main():
    async for result in chain.astream_events({"question": "计算宽为10高为5的长方形面积"}, version="v2"):
        if result["event"] == "on_chat_model_stream":
            content = result["data"]["chunk"].content
            if content:
                print(content, end="", flush=True)

if __name__ == '__main__':
    asyncio.run(main())