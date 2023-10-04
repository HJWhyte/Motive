from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
import pymongo
import uuid

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
    user_id = uuid.uuid4()
    userObj = { username : user_id } 
    return userObj



# Close the DB client connection
client.close()