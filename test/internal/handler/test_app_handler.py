from pkg.response import HTTPCode
import pytest

class TestAppHandler:
    """app控制器的测试类"""
    @pytest.mark.parametrize("query", [None, "你好，你是？"])
    def test_completion(self, query, client):
        """测试完成接口"""
        response = client.post("/chat", json={"query": query})
        assert response.status_code == 200
        if query is None:
            assert response.json.get("code") == HTTPCode.VALIDATION_ERROR
        else:
            assert response.json.get("code") == HTTPCode.SUCCESS 
