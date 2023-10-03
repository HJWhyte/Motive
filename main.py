from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
import pymongo

# Load .env file variables
load_dotenv()

# Assign DB connection string
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

# Create MongoClient obj
client = pymongo.MongoClient(CONNECTION_STRING)

# Connect to the assigned DB 
db = client['motive']

# Assign User collection
users = db['users']

# Create FastAPI app
app = FastAPI()

@app.get("/")
def root():
    """Basic API route test"""
    return {"Test" : "Route working!"}