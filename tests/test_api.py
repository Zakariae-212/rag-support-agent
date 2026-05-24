import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_chat_success():

    response = client.post("/chat", json={
        "message": "Quels sont les moyens de paiement ?"
    })

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "response" in data


def test_email_validation():

    response = client.post("/chat", json={
        "message": "Bonjour",
        "email": "bad-email"
    })

    data = response.json()

    assert data["status"] == "error"