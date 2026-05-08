from datetime import date

from fastapi.testclient import TestClient

from src.service.main import app
from src.service.schemas import PredictRequest

client = TestClient(app)


def test_health_endpoint_contract():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_path"].endswith("artifacts/model.pkl")
    assert body["data_path"].endswith("data/data.csv")


def test_regions_endpoint():
    response = client.get("/regions")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0


def test_predict_endpoint():
    payload = {
        "admin_center": "Краснодар",
        "date": "2026-06-15"
    }
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "predictions" in body
    assert len(body["predictions"]) > 0


def test_predict_endpoint_invalid_payload():
    payload = {"admin_center": "", "date": ""}
    response = client.post("/predict", json=payload)

    assert response.status_code == 422
