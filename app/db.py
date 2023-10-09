from dotenv import load_dotenv
import os 
import pymongo
import logging


def db_connect():
    '''Creates DB connection client'''
    try:
        # Load .env file variables
        load_dotenv()
        # Assign DB connection string
        CONNECTION_STRING = os.getenv('CONNECTION_STRING')
        # Create MongoClient obj and Connect to the assigned DB 
        client = pymongo.MongoClient(CONNECTION_STRING)
        db = client['motive']
        # Assign User collection
        users = db['users']
        # Index allowing only unique usernames
        users.create_index('username', unique=True)
        return client, users
    except pymongo.errors.ConnectionError as e:
        return logging.error(f"DB connection failed: {e}")


def db_close(client):
    '''Closes DB connection'''
    client.close()
    return