"""
动态切换参数
"""
from typing import Any

from langchain.agents import create_agent
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField, RunnableConfig
from langchain_openai import ChatOpenAI

from tools.my_tools import calculate_area, add
from utils.env_util import qwen_base_url, qwen_api_key, qwen_model_name


# 定义大模型，并允许动态修改temperature参数
llm = ChatOpenAI(
    model=qwen_model_name,
    api_key=qwen_api_key,
    base_url=qwen_base_url,
    temperature=0.3
).configurable_fields(
    temperature=ConfigurableField(
        id='temperature',
        name='temperature level',
        description='控制随机值，取值范围0-1'
    )
)

# 回调函数的类
class ParamsChecker(BaseCallbackHandler):
    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        **kwargs: Any
    ):
        inv_params = kwargs.get('invocation_params', None)
        print(f"实际使用的temperature参数:{inv_params['temperature']}")


# 运行时配置，在agent当次运行过程中作为全局变量使用
config = RunnableConfig(
    configurable={
        'temperature': 0.9
    },
    callbacks=[ParamsChecker()],
)

agent = create_agent(
    model=llm,
    tools=[calculate_area, add]
)

# 提示词模板
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("human", "{question}")
    ]
)

# LCEL链
# |： 管道，表示管道前对象的输出作为管道后对象的输出
# chain = prompt_template | agent

chain = prompt_template | llm


results = chain.invoke({"question": "计算宽为15，高为20的长方形面积"}, config=config)
# for result in results['messages']:
#     result.pretty_print()

print(results.content)