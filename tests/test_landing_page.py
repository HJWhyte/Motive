import requests
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append('..')
from app.main import app

client = TestClient(app)