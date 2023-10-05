import sys
import os 
from dotenv import load_dotenv
import pymongo
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from utils import clear_test_users

sys.path.append('..')
from app.main import app 

client = TestClient(app)

@pytest.mark.parametrize("username", ["TEST1", "TEST2", "TEST3"])
def test_create_user_success(username):
    '''Function to test the createUser route works as intended'''
    
    response = client.post(f"/createUser?username={username}")
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    # Check the response content
    response_json = response.json()
    assert response_json["message"] == "User created successfully"
    assert response_json["username"] == username
    # Ensure user_id is present in the response
    assert "user_id" in response_json
    clear_test_users()  

def test_create_user_success():
    '''Function to test the createUser route fails when intended'''
    
    username = "FAILTEST"
    # Make 2 post requests with the same username
    response1 = client.post(f"/createUser?username={username}")
    response2 = client.post(f"/createUser?username={username}")
    # Check the status code is 400 (Fail)
    assert response2.status_code == 400
    #Check Response Content
    response_json = response2.json()
    assert "User creation failed" in response_json["detail"]
    clear_test_users()
