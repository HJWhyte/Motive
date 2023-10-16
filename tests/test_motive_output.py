import requests
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient
from utils import clear_test_events, clear_test_users

sys.path.append('..')
from app.main import app
from app.db import db_connect, db_close

client = TestClient(app)

def test_motive_vote_success():
    """Test that an event can be succesfully voted on"""

    name = "TESTEVENT"
    username1 = "TESTUSER"
    username2 = "TESTUSER1"
    start = "2000-01-08"
    end = "2000-01-20"
    availability1 = ["2000-01-10", "2000-01-15"]
    availability2 = ["2000-01-10", "2000-01-13"]

    db_client, db_users, db_events = db_connect()
    client.post(f"/createUser?username={username1}")
    client.post(f"/createMotive?motive_name={name}&start_date={start}&end_date={end}")
    response = client.post(f"/vote/{name}?motive_name={name}&username={username1}&availability={availability1[0]}&availability={availability1[1]}")
    response = client.post(f"/vote/{name}?motive_name={name}&username={username2}&availability={availability2[0]}&availability={availability2[1]}")


    
    response_json = response.json()
    assert f'Availablity succesfully added to {name}' in response_json[f"{username}"]
    assert response.status_code == 200
    clear_test_events(db_events)
    clear_test_users(db_users)
    db_close(db_client)