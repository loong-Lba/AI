# 导入FastAPI
from fastapi import FastAPI
# 导入uvicorn
import uvicorn
from pydantic import BaseModel

# 创建FastAPI对象
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


# 路径参数
@app.get("/hello/{name}/{password}")
def say_hello(name: str, password: str):
    return {"message": f"Hello {name} {password}"}

# 查询参数 --- 参数以key=value&key2=value....格式传递过来
@app.get("/queryParams")    # 定义请求路径字符串的时候，统一使用小驼峰命令，即第二个单词开始首字母大写、见文知意
def query_params(username: str, password: str):
    print(username, password)
    return {"message": f"Hello {username} {password}"}

# 分页查询：page变量表示当前数据的页码、size变量表示每页的数据条数、username变量表示查询的用户名【可能有可能无】
@app.get("/findUsers")
def find_users(page: int, size: int, username: str):
    print(page, size, username)
    return {"message": f"page: {page} size: {size} username: {username}"}

# 请求体 --- json数据接收
class User(BaseModel):
    username: str
    password: str

@app.post("/insert")
def insert(user: User):
    print(user)
    print(user.username)
    print(user.password)
    return {"message": f"username: {user.username} password: {user.password}"}


# 运行FastAPI
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=False,
    )