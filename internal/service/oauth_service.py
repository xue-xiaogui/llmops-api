"""OAuth 服务"""


class OAuthService:
    """第三方 OAuth 登录服务"""

    def __init__(self, provider: str = "github"):
        self.provider = provider

    def get_authorization_url(self) -> str:
        """获取授权链接"""
        raise NotImplementedError

    def exchange_token(self, code: str) -> dict:
        """用授权码换取 access token"""
        raise NotImplementedError
