from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.airport import router as airport_router
from app.api.flights import router as flight_router
from app.api.seat import router as seat_router
from app.api.booking import router as booking_router
from app.api.payment import router as payment_router
from app.user.get_user import router as user_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs.booking_expiry import run_expiry_job
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "https://skyroute-flight-booking-system.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get('/')
# def get():
#     return {'message' : 'Hello'}

app.include_router(auth_router)
app.include_router(airport_router)
app.include_router(flight_router)
app.include_router(seat_router)
app.include_router(booking_router)
app.include_router(payment_router)
app.include_router(user_router)


scheduler = BackgroundScheduler()


@app.on_event("startup")
def start_scheduler():

    scheduler.add_job(
        run_expiry_job,
        trigger="interval",
        minutes=1,
    )

    scheduler.start()


@app.on_event("shutdown")
def stop_scheduler():

    scheduler.shutdown()