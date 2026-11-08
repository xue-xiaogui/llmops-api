"""账户相关路由处理器"""
from flask import jsonify


def get_account_info():
    """获取账户信息"""
    return jsonify({"message": "account info"})
