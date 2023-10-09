import requests
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append('..')
from app.main import app

client = TestClient(app)

def test_can_call_endpoint():
    '''Function to test if the api endpoint '''
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Test" : "Route working!"}
    pass

