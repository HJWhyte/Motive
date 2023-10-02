import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app  # noqa: E402, E501,E501 pylint: disable=C0413

client = TestClient(app)

def test_can_call_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    pass