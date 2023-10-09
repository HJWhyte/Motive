from fastapi import FastAPI, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
import pymongo
import logging
from app.db import db_connect, db_close

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

@app.get("/")
def root():
    """Basic API route test"""
    return {"Test" : "Route working!"}


@app.post("/createUser")
def createUser(username: str):
    '''User creation route'''
    logging.info(f'Username: {username}')
    try:
        client, users = db_connect()
        user_doc = users.insert_one({'username' : username})
        user_id = user_doc.inserted_id
        return {"message": "User created successfully",
                "username" : username,
                "user_id" : str(user_id)}
    except pymongo.errors.DuplicateKeyError as e:
        logging.error("Duplicate username, user creation failed")
        raise HTTPException(status_code=400, detail=f"User creation failed: {e}")
    # Add DB Connection exception
    finally:
        db_close(client)