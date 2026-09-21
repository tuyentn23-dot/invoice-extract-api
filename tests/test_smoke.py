"""Smoke test: FastAPI app imports and health endpoint works with TestClient."""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "Invoice Extraction API"


def test_short_content_rejected():
    r = client.post("/v1/invoice/extract", json={"content": "hi"})
    assert r.status_code == 400
