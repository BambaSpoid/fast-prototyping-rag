from fastapi.testclient import TestClient
from rag.api.main import app

client = TestClient(app)


def test_rag_endpoint_returns_200():
    response = client.post("/rag", json={"question": "What is RAG?"})
    assert response.status_code == 200
    assert "answer" in response.json()
