from fastapi import FastAPI, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
import pymongo
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env file variables
load_dotenv()

# Assign DB connection string
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
# logging.info(f"CONNECTION_STRING: {CONNECTION_STRING}")  -- Not Sure If Ok

# Create MongoClient obj and Connect to the assigned DB 
client = pymongo.MongoClient(CONNECTION_STRING)
db = client['motive']

# Assign User collection
users = db['users']

# Create an index allowing only unique usernames
users.create_index('username', unique=True)


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
        user_doc = users.insert_one({'username' : username})
        user_id = user_doc.inserted_id
        return {"message": "User created successfully",
                "username" : username,
                "user_id" : str(user_id)}
    except pymongo.errors.DuplicateKeyError as e:
        logging.error("Duplicate username, user creation failed")
        raise HTTPException(status_code=400, detail=f"User creation failed: {e}")




# client.close()