import pymongo
import os 
from dotenv import load_dotenv

# Load .env file variables
load_dotenv()

# Assign DB connection string
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

# Create MongoClient obj and Connect to the assigned DB 
client = pymongo.MongoClient(CONNECTION_STRING)
db = client['motive']

# Assign User collection
users = db['users']

# def clear_test_users():
#     users.delete_many({
#         "username" : {
#             $regex: 'TEST'
#         }
#     })