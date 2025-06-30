from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rate_limiting():
    for _ in range(5):
        response = client.get("/search?company_id=1")
        assert response.status_code in [200, 422]  # missing required filters

    response = client.get("/search?company_id=1")
    assert response.status_code == 429
