"""应用中间件：包含登录校验等"""
from flask import request, jsonify


def login_required_middleware():
    """校验请求是否登录的中间件（示例）"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"message": "未登录", "code": 401}), 401
    return None
