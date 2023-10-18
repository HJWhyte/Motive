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
    username = "TESTUSER"
    start = "2000-01-08"
    end = "2000-01-20"
    availability = ["2000-01-10", "2000-01-15"]

    db_client, db_users, db_events = db_connect()
    client.post(f"/createUser?username={username}")
    client.post(f"/createMotive?motive_name={name}&start_date={start}&end_date={end}")
    response = client.post(f"/vote/{name}?motive_name={name}&username={username}&availability={availability[0]}&availability={availability[1]}")
    response_json = response.json()
    assert f'Availablity succesfully added to {name}' in response_json[f"{username}"]
    assert response.status_code == 200
    clear_test_events(db_events)
    clear_test_users(db_users)
    db_close(db_client)

def test_motive_invalid_date_fail():
    """Test that an event will not allow the same user to vote on it twice"""

    name = "TESTEVENT"
    username = "TESTUSER1"
    start = "2000-01-08"
    end = "2000-01-20"
    availability = ["2000-02-10", "2000-02-15"]

    db_client, db_users, db_events = db_connect()
    client.post(f"/createUser?username={username}")
    client.post(f"/createMotive?motive_name={name}&start_date={start}&end_date={end}")
    response1 = client.post(f"/vote/{name}?motive_name={name}&username={username}&availability={availability[0]}&availability={availability[1]}")
    response_json = response1.json()
    assert response1.status_code == 400
    assert 'Availability dates must be within the event\'s date range' in response_json["detail"]
    clear_test_events(db_events)
    clear_test_users(db_users)
    db_close(db_client)

