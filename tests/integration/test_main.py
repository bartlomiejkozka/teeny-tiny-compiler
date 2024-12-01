from fastapi.testclient import TestClient
from backend.main import app


class TestMain:
    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    
    def test_run_code_button(self):
        response = self.client.post("/run_code", json={"code": "PRINT \"Hello World!\"\nEND"})
        assert response.status_code == 200
