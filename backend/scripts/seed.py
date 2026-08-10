from datetime import datetime, timedelta
import random

from app.core.database import SessionLocal
from app.models.airport import Airport
from app.models.flights import Flight
from app.services.seat_service import SeatService
from sqlalchemy.exc import IntegrityError

AIRPORTS = [
    {"iata_code": "BOM", "name": "Chhatrapati Shivaji Maharaj International Airport", "city": "Mumbai", "country": "India"},
    {"iata_code": "DEL", "name": "Indira Gandhi International Airport", "city": "Delhi", "country": "India"},
    {"iata_code": "BLR", "name": "Kempegowda International Airport", "city": "Bangalore", "country": "India"},
    {"iata_code": "HYD", "name": "Rajiv Gandhi International Airport", "city": "Hyderabad", "country": "India"},
    {"iata_code": "MAA", "name": "Chennai International Airport", "city": "Chennai", "country": "India"},
    {"iata_code": "GOI", "name": "Goa International Airport", "city": "Goa", "country": "India"},
    {"iata_code": "PNQ", "name": "Pune Airport", "city": "Pune", "country": "India"},
]

AIRLINES = [
    {"name": "Air India", "prefix": "AI"},
    {"name": "IndiGo", "prefix": "6E"},
    {"name": "SpiceJet", "prefix": "SG"},
    {"name": "Vistara", "prefix": "UK"},
]

AIRCRAFT_TYPES = ["Airbus A320", "Boeing 737", "ATR 72"]


def seed_airports(db):
    airport_map = {}
    for a in AIRPORTS:
        existing = db.query(Airport).filter(Airport.iata_code == a["iata_code"]).first()
        if existing:
            airport_map[a["iata_code"]] = existing
            continue
        airport = Airport(**a)
        db.add(airport)
        db.flush()
        airport_map[a["iata_code"]] = airport
    db.commit()
    return airport_map


def seed_flights(db, airport_map):
    routes = [
        ("BOM", "DEL"), ("DEL", "BOM"),
        ("BOM", "BLR"), ("BLR", "BOM"),
        ("DEL", "BLR"), ("BLR", "DEL"),
        ("BOM", "HYD"), ("DEL", "HYD"),
        ("BOM", "GOI"), ("BLR", "MAA"),
        ("DEL", "PNQ"), ("MAA", "HYD"),
    ]

    today = datetime.utcnow().date()

    for origin_code, dest_code in routes:
        origin = airport_map[origin_code]
        destination = airport_map[dest_code]

        # 3-5 flights per route, spread across the next 14 days
        for _ in range(random.randint(3, 5)):
            airline = random.choice(AIRLINES)
            flight_number = f"{airline['prefix']}{random.randint(100, 999)}"
            days_out = random.randint(1, 14)
            departure_hour = random.randint(5, 22)
            departure_time = datetime.combine(
                today + timedelta(days=days_out),
                datetime.min.time(),
            ) + timedelta(hours=departure_hour)

            duration_minutes = random.randint(60, 210)
            arrival_time = departure_time + timedelta(minutes=duration_minutes)

            existing = (
                db.query(Flight)
                .filter(
                    Flight.flight_number == flight_number,
                    Flight.departure_time == departure_time,
                )
                .first()
            )
            if existing:
                continue

            flight = Flight(
                flight_number=flight_number,
                airline=airline["name"],
                origin_airport_id=origin.id,
                destination_airport_id=destination.id,
                departure_time=departure_time,
                arrival_time=arrival_time,
                duration_minutes=duration_minutes,
                base_price=random.randint(3000, 8000),
                aircraft_type=random.choice(AIRCRAFT_TYPES),
                stops=0,
            )

            try:
                db.add(flight)
                db.flush()
                SeatService.generate_for_flight(db, flight)
                db.commit()
                print(f"Seeded {flight_number}: {origin_code} -> {dest_code} on {departure_time}")
            except IntegrityError:
                db.rollback()
            except Exception as e:
                db.rollback()
                print(f"Skipped {flight_number}: {e}")


def main():
    db = SessionLocal()
    try:
        print("Seeding airports...")
        airport_map = seed_airports(db)

        print("Seeding flights + seats...")
        seed_flights(db, airport_map)

        print("Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()