from enum import Enum
"""HTTP 状态码枚举"""
class HTTPCode(str, Enum):
    # HTTP基础业务状态码
    SUCCESS = "success"  # 成功
    FAIL = "fail"  # 失败   
    BAD_REQUEST = "bad_request"  # 请求错误
    UNAUTHORIZED = "unauthorized"  # 未授权
    FORBIDDEN = "forbidden"  # 无权限
    NOT_FOUND = "not_found"  # 未找到资源
    CREATED = "created"  # 创建成功
    NO_CONTENT = "no_content"  # 无内容
    INTERNAL_SERVER_ERROR = "internal_server_error"  # 内部服务器错误
    VALIDATION_ERROR = "validation_error"  # 数据验证错误