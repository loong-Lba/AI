"""
模型供应商切换
"""
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField, RunnableConfig
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from utils.env_util import qwen_model_name, qwen_api_key, qwen_base_url

llm = ChatOpenAI(
    model=qwen_model_name,
    api_key=qwen_api_key,
    base_url=qwen_base_url,
    temperature=0.3
).configurable_alternatives(
    ConfigurableField(
        id="model",
        name="model",
        description="AI大模型"
    ),
    default_key="ollama_qwen",
    ollama=ChatOllama(model="qwen3.7-plus")
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("human", "{question}")
    ]
)

chain = prompt_template | llm

class ParameterChecker(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs):
        # 查看实际使用的调用参数
        metadata = kwargs.get('metadata',{})
        print(f"实际使用的model：{metadata.get('model')}")

config = RunnableConfig(
    configurable={
        "model": "ollama_qwen"
    },
    callbacks=[ParameterChecker()]
)

result = chain.invoke({"question": "你叫什么名字"}, config=config)
print(result.content)