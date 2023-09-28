from fastapi import FastAPI
import uvicorn

## Create FastAPI app
app = FastAPI()

@app.get("/")
def root():
    """Basic API route test"""
    return {"Test" : "Route working!"}