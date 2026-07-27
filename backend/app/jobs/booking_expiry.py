from app.core.database import SessionLocal
from app.services.booking_service import BookingService


def run_expiry_job():

    db = SessionLocal()

    try:
        expired = BookingService.expire_stale_bookings(db)

        print(f"Expired {expired} bookings.")

    finally:
        db.close()