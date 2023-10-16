import pymongo
import re

def clear_test_users(users):
    substring = re.compile('TEST')
    filter = {"username": {"$regex" : substring}}
    users.delete_many(filter)
    return

def clear_test_events(events):
    substring = re.compile('TEST')
    filter = {"Motive Name": {"$regex" : substring}}
    events.delete_many(filter)
    return