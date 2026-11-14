from typing import Any
from pkg.response.http_code import HTTPCode
from dataclasses import field, dataclass
from flask import jsonify

# 设计响应格式
@dataclass
class Response:
    # 基础HTTP接口响应格式
    code: HTTPCode = HTTPCode.SUCCESS
    message: str = ""
    data: Any = field(default_factory=dict)

def json(data: Response = None):
    response = jsonify(data)
    # 添加跨域响应头
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    # 基础响应格式
    return response, 200
   
def success_json(data: Any = None):
    # 成功响应
    return json(Response(code=HTTPCode.SUCCESS, message="", data=data))

def fail_json(data: Any = None  ):
    # 失败响应
    return json(Response(code=HTTPCode.FAIL, message="", data=data))

def validate_error_json(errors: dict = None):
    # 校验错误响应
    first_key = next(iter(errors))
    if first_key is not None:
        msg = errors.get(first_key)[0]
    else:
        msg = ""
    return json(Response(code=HTTPCode.VALIDATION_ERROR, message=msg, data=errors))

# 消息响应
def message(code: HTTPCode = None, msg: str = ""):
    # 消息响应
    return json(Response(code=code, message=msg, data={}))
        
def success_message(msg: str = ""):
    # 成功消息响应
    return message(code=HTTPCode.SUCCESS, msg=msg)

def fail_message(msg: str = ""):
    # 失败消息响应
    return message(code=HTTPCode.FAIL, msg=msg)

def node_found_message(msg: str = ""):
    # 未找到消息响应
    return message(code=HTTPCode.NOT_FOUND, msg=msg)

def unauthorized_message(msg: str = ""):
    # 未授权消息响应
    return message(code=HTTPCode.UNAUTHORIZED, msg=msg)

def forbidden_message(msg: str = ""):
    # 无权限消息响应
    return message(code=HTTPCode.FORBIDDEN, msg=msg)