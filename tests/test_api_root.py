import sys
import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.insert(0, r"..")
from main import app  # noqa: E402, E501,E501 pylint: disable=C0413

client = TestClient(app)

def test_can_call_endpoint():
    '''Function to test if the api endpoint '''
    response = client.get("/")
    assert response.status_code == 200
    pass