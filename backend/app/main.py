from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.airport import router as airport_router
app = FastAPI()

# @app.get('/')
# def get():
#     return {'message' : 'Hello'}

app.include_router(auth_router)
app.include_router(airport_router)