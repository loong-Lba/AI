"""
定义Agent的工具
使用tool装饰器定义：
1.@tool装饰器：定义在方法上边，表示方法是一个工具
2.写方法描述，两种方式：1) 在@tool的description中添加，2) 使用Docstring方式添加(方法注释)
3.如果方法有参数，需要给参数添加描述
"""
from typing import Annotated

from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field


# tool：agent工具装饰器，参数：
# - name: 指定工具的名称，如果不指定，则默认使用方法名称作为工具名称
# # - description：工具方法的描述，用来描述该方法是什么，有什么作用，什么时候调用
# @tool(description="计算长方形面积的工具，当需要计算面积时调用该工具")
# def calculate_area(
#         width: Annotated[float, "长方形的宽"],
#         height: Annotated[float, "长方形的高"]
# ):
#     return width * height


# 方法描述：
# 1.tool装饰器中description做方法描述
# 2.使用Docstring做方法描述，一般定义在方法体的第一行，使用多行注释符号来进行描述
# description和Docstring的优先级：description > Docstring
# Docstring更常用
@tool(description="计算长方形面积的工具，当需要计算面积时调用该工具")
def calculate_area(
        width: Annotated[float, "长方形的宽"],
        height: Annotated[float, "长方形的高"]
):
    """计算长方形面积的工具"""

    return width * height


class AddRequest(BaseModel):
    a: float = Field(..., description="加数1", ge=0, le=10)
    b: float = Field(..., description="加数2", ge=0, le=10)


# 工具参数描述：
# 1.使用Annotated进行描述，可以对参数进行类型指定，参数描述，参数约束
# 2.使用pydantic模块进行参数描述和校验，使用方式：
# 1) 定义一个类，继承pydantic的BaseModel，在该类中定义参数，包括：数据类型、描述、约束等
# 2) 在tool装饰器的args_schema属性中引用该类
# Annotated相对常用，比较复杂的参数一般使用pydantic方式
@tool(args_schema=AddRequest)
def add(a: float, b: float):
    """计算两个加数之和"""
    return a + b


# 动态转换工具

# 定义一个普通函数
def get_weather(city: str, unit: str = "C"):
    return f"{city}的温度为25°{unit}"


# 把普通函数转换为工具
weather_tool = StructuredTool.from_function(
    func=get_weather,
    name="get_weather",
    description="查询指定城市温度的工具"
)

if __name__ == '__main__':
    # result = calculate_area.invoke({"width": 10, "height": 20})
    # print(result)
    #
    # print(calculate_area.description)

    # result = add.invoke({"a": 10, "b": 2})
    # print(result)
    # print(add.description)
    # print(add.args_schema)

    result = weather_tool.invoke({"city": "成都"})
    print(result)
    print(type(weather_tool))
