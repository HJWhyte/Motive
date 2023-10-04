import pymongo
import os 
from dotenv import load_dotenv
import re

# Load .env file variables
load_dotenv()

# Assign DB connection string
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

# Create MongoClient obj and Connect to the assigned DB 
client = pymongo.MongoClient(CONNECTION_STRING)
db = client['motive']

# Assign User collection
users = db['users']

def clear_test_users():
    substring = re.compile('TEST')
    filter = {"username": {"$regex" : substring }}
    users.delete_many(filter)
    return

