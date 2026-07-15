from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pymysql

app = FastAPI()

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """登录响应模型"""
    code: int
    msg: str
    data: Optional[dict] = None


DB_CONFIG = {
    "host": "localhost",  # MySQL 主机地址
    "port": 3306,  # MySQL 端口
    "user": "root",  # MySQL 用户名
    "password": "root",  # MySQL 密码（改成你自己的）
    "database": "fastapi",  # 数据库名（改成你自己的）
    "charset": "utf8mb4"
}

def get_db_connection():
    """获取 MySQL 数据库连接"""
    return pymysql.connect(**DB_CONFIG)


def check_user(username: str):
    """
    查询用户是否存在
    返回: (存在, 密码)
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # SQL 查询语句
            sql = "SELECT password FROM user WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()

            if result:
                return True, result[0]  # 存在，返回密码
            else:
                return False, None  # 不存在
    finally:
        conn.close()

@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    用户登录接口（使用 MySQL 数据库）
    """
    # 1. 检查账号是否存在
    exists, stored_password = check_user(request.username)

    if not exists:
        return {
            "code": 500,
            "msg": "账号不存在",
            "data": None
        }

    # 2. 检查密码是否正确
    if stored_password != request.password:
        return {
            "code": 500,
            "msg": "密码错误",
            "data": None
        }

    # 3. 登录成功
    return {
        "code": 200,
        "msg": "登录成功",
        "data": None
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9000)