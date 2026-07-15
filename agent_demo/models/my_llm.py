"""
创建大模型
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from utils.env_util import qwen_model_name, qwen_api_key, qwen_base_url

qwen_llm = ChatOpenAI(
    model=qwen_model_name,
    api_key=qwen_api_key,
    base_url=qwen_base_url,
    temperature=0.3,
    max_tokens=1024
)

if __name__ == '__main__':
    prompt_template = ChatPromptTemplate.from_messages([
        ("human", "{question}")
    ])

    chain = prompt_template | qwen_llm

    # result = chain.invoke({"question": "你叫什么名字，有什么功能?"})
    # print(result)

    for result in chain.stream({"question": "你叫什么名字，有什么功能"}):
        print(result)