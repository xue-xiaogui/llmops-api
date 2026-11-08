"""GitHub OAuth 实现"""
import os

import httpx


class GitHubOAuth:
    """GitHub OAuth 登录"""

    AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_URL = "https://api.github.com/user"

    def __init__(self):
        self.client_id = os.getenv("GITHUB_CLIENT_ID", "")
        self.client_secret = os.getenv("GITHUB_CLIENT_SECRET", "")

    def get_authorization_url(self, state: str = "") -> str:
        """获取 GitHub 授权链接"""
        return (
            f"{self.AUTHORIZE_URL}?client_id={self.client_id}"
            f"&state={state}&scope=user:email"
        )

    async def exchange_token(self, code: str) -> dict:
        """用 code 换取 access token"""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.TOKEN_URL,
                json={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                },
                headers={"Accept": "application/json"},
            )
            return resp.json()
