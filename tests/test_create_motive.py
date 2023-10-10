import sys
import os 
from dotenv import load_dotenv
import pymongo
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from utils import clear_test_users

sys.path.append('..')
from app.main import app
from app.db import db_connect, db_close