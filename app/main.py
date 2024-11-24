"""
Main module for the FastAPI application.
"""
from fastapi import FastAPI
from app.routes import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def home():
    """
    Welcome message for the API.
    """
    return {"message": "Welcome to rental car API!"}
