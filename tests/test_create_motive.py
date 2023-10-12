import sys
import os 
from dotenv import load_dotenv
import pymongo
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from utils import clear_test_events

sys.path.append('..')
from app.main import app
from app.db import db_connect, db_close

test_client = TestClient(app)

def test_event_creation_success():
    '''Test an event can be successfully created'''

    name = 'TEST'
    start = "2000-01-08"
    end = "2000-01-09"

    db_client, db_users, db_events = db_connect()
    response = test_client.post(f"/createMotive?motive_name={name}&start_date={start}&end_date={end}")
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    # Check the response content
    response_json = response.json()
    assert response_json["Message"] == "Motive event created successfully"
    assert response_json["Motive Name"] == name
    # Ensure user_id is present in the response
    assert "Event ID" in response_json
    clear_test_events(db_events)
    db_close(db_client)

def test_event_username_fail():
    '''Test for a failure if two events are created with the same name'''

    name = 'FAILTEST'
    start = "2000-01-08"
    end = "2000-01-09"

    db_client, db_users, db_events = db_connect()
    response1 = test_client.post(f"/createMotive?motive_name={name}&start_date={start}&end_date={end}")
    response2 = test_client.post(f"/createMotive?motive_name={name}&start_date={start}&end_date={end}")
    assert response2.status_code == 400
    response_json = response2.json()
    assert "Event creation failed" in response_json["detail"]
    clear_test_events(db_events)
    db_close(db_client)