from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.airport import router as airport_router
from app.api.flights import router as flight_router
from app.api.seat import router as seat_router
from app.api.booking import router as booking_router

app = FastAPI()

# @app.get('/')
# def get():
#     return {'message' : 'Hello'}

app.include_router(auth_router)
app.include_router(airport_router)
app.include_router(flight_router)
app.include_router(seat_router)
app.include_router(booking_router)
