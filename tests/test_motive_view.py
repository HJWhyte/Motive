import requests
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient
from utils import clear_test_events, clear_test_users

sys.path.append('..')
from app.main import app
from app.db import db_connect, db_close

client = TestClient(app)

def test_event_view():
    """Test a motive can be viewed"""
    
    name = 'TEST'
    start = "2000-01-08"
    end = "2000-01-09"

    db_client, db_users, db_events = db_connect()
    client.post(f"/createMotive?motive_name={name}&start_date={start}&end_date={end}")
    response = client.get(f'/view/{name}')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Motive Name"] == name
    clear_test_events(db_events)
    db_close(db_client)