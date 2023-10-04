import sys
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append('..')
from app.main import app 

client = TestClient(app)

@pytest.mark.parametrize("username", ["user1", "user2", "user3"])
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
    
