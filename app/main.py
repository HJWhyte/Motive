from fastapi import FastAPI, HTTPException, Query
import uvicorn
import os
import json
from bson import json_util
from dotenv import load_dotenv
import pymongo
import logging
from typing import Tuple
from datetime import date, datetime
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

@app.get("/motive")
def home():
    """Home Page - refer to user / event creation"""
    return {"Message" : "Welcome to Motive!",
            "Create a user" : "/createUser",
            "Create an event" : "/createMotive"}


@app.post("/createUser")
def createUser(username: str):
    """User creation route"""
    logging.info(f'Username: {username}')
    try:
        client, users, events = db_connect()
        user_doc = users.insert_one({'username' : username})
        user_id = user_doc.inserted_id
        return {"message": "User created successfully",
                "username" : username,
                "user_id" : str(user_id)}
    except pymongo.errors.DuplicateKeyError as e:
        logging.error("Duplicate username, user creation failed")
        raise HTTPException(status_code=400, detail=f"User creation failed: {e}")
    except pymongo.errors.PyMongoError as e:
        logging.error("DB connection failed")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    finally:
        db_close(client)

@app.post("/createMotive")
def createMotive(motive_name : str, start_date: str, end_date: str, description: str = ''):
    """Event object creation route - NOTE all dates must follow the y-m-d format"""
    logging.info(f'Motive Name: {motive_name}, Date Range: {start_date} - {end_date}, Event Description: {description}')
    try:
        client, users, events = db_connect()
        date_format = "%Y-%m-%d"  # Year-month-day format
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date,date_format)

        eventObj = {"Motive Name" : motive_name,
                    "Date Range"  : [start_date, end_date],
                    "Event Description" : description,
                    "User Votes" : []}
        event_doc = events.insert_one(eventObj)
        event_id = event_doc.inserted_id
        return {"Message" : "Motive event created successfully",
                "Motive Name" : motive_name,
                "Date Range"  : [start_date, end_date],
                "Event Description" : description,
                "Event ID" : str(event_id)}
    except pymongo.errors.DuplicateKeyError as e:
        logging.error("Duplicate event name, event creation failed")
        raise HTTPException(status_code=400, detail=f"Event creation failed: {e}")
    except pymongo.errors.PyMongoError as e:
        logging.error("DB connection failed")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    finally:
        db_close(client)

@app.get('/view/{motive_name}')
def motive_view(motive_name: str):
    """Show the current state of the event"""
    logging.info(f'Motive Name: {motive_name}')
    try:
        client, users, events = db_connect()
        motive = events.find_one({'Motive Name' : motive_name})
        logging.info(f"Event Found: {motive}")
        jsonObj = json_util.dumps(motive)
        parsed_json = json.loads(jsonObj)
        return parsed_json
    except pymongo.errors.PyMongoError as e:
        logging.error("DB connection failed")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    finally:
        db_close(client)

@app.post('/vote/{motive_name}')
def motive_vote(motive_name: str, username: str, availability: list = Query(..., title="List of available dates")):
    """Event vote submission route"""
    logging.info(f'Motive Name: {motive_name}')
    try:
        client, users, events = db_connect()
        check_event = events.find_one({'Motive Name' : motive_name})
        check_user = users.find_one({"username": username})
        username_filter = {'Motive Name': motive_name, 'User Votes': {'$elemMatch': {username: {'$exists': True}}}}
        existing_vote = events.find_one(username_filter)
        if check_event == None:
                logging.error("Event not found")
                raise HTTPException(status_code=404, detail=f"A valid event could not be found.")
        if check_user == None:
            logging.error("User not found")
            raise HTTPException(status_code=404, detail=f"A valid username could not be found.")
        if existing_vote:
            logging.error("Username already voted for this event")
            raise HTTPException(status_code=400, detail="User has already voted for this event.")
        voteObj = {username: availability}
        filter = {'Motive Name': motive_name}
        update = {"$push" : { 'User Votes' : voteObj}}
        events.update_one(filter, update)
        return {f"{username}" : f"Availablity succesfully added to {motive_name}"}
    except pymongo.errors.PyMongoError as e:
        logging.error("DB connection failed")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    finally:
        db_close(client)

@app.get('/output/{motive_name}')
def output(motive_name: str):
    """Show the optimal event dates"""
    logging.info(f'Motive Name: {motive_name}')
    try:
        client, users, events = db_connect()
        check_event = events.find_one({'Motive Name' : motive_name})




