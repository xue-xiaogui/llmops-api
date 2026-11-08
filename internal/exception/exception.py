"""通用自定义异常类"""
from dataclasses import field
from pkg.response import HTTPCode

from typing import Any

class CustomException(Exception):
    """自定义异常基类"""

    code: HTTPCode = HTTPCode.FAIL
    message: str = ""
    data: Any = field(default_factory=dict)

    def __init__(self, message: str = None, data: Any = None):
        super().__init__()
        self.message = message
        self.data = data

class FailException(CustomException):
    # 通用失败异常
    pass

class NotFoundException(CustomException):
    # 资源不存在异常
    code = HTTPCode.NOT_FOUND

class UnauthorizedException(CustomException):
    # 未授权异常
    code = HTTPCode.UNAUTHORIZED

class ForbiddenException(CustomException):
    # 无权限异常
    code = HTTPCode.FORBIDDEN

class ValidationException(CustomException):
    # 参数校验失败异常
    code = HTTPCode.VALIDATION_ERROR
