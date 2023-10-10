from fastapi import FastAPI, HTTPException, Query
import uvicorn
import os
from dotenv import load_dotenv
import pymongo
import logging
from typing import Tuple
from datetime import date, datetime
from db import db_connect, db_close

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
    except pymongo.errors.ConnectionError as e:
        logging.error("DB connection failed")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
    except pymongo.errors.PyMongoError as e:
        logging.error(f"MongoDB error: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected database error occurred: {e}")
    finally:
        db_close(client)

@app.post("/createMotive")
def createMotive(motive_name : str, start_date: str, end_date: str, description: str = ''):
    '''Event object creation route'''
    logging.info(f'Motive Name: {motive_name}, Date Range: {start_date} - {end_date}, Event Description: {description}')
    try:
        client, users, events = db_connect()
        date_format = "%Y-%m-%d"  # Year-month-day format
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date,date_format)

        eventObj = {"Motive name" : motive_name,
                    "Date Range"  : [start_date, end_date],
                    "Event Description" : description}
        event_doc = events.insert_one(eventObj)
        event_id = event_doc.inserted_id
        return
    except:
        return





# client, users = db_connect()
# check_user = users.find_one({"username": username})
# if check_user == None:
#     logging.error("User not found")
#     raise HTTPException(status_code=404, detail=f"A valid username could not be found.")