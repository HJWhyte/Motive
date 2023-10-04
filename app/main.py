from fastapi import FastAPI
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
    userObj = {'username' : username }
    try:
        userDoc = users.insert_one(userObj)
        return('User successfully created!', userDoc)
    except pymongo.errors.DuplicateKeyError as e:
        return f"Insertion failed: {e}"



# Close the DB client connection
# client.close()