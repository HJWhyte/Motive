import requests
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append('..')
from app.main import app

client = TestClient(app)

def test_get_motive():
    """Test the home page basic functionality"""
    response = client.get('/motive')
    response_json = response.json()
    assert response_json["Message"] == "Welcome to Motive!"
    assert response.status_code == 200