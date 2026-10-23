# scripts/seed.py
import random
from datetime import date, datetime, timedelta

from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.models import Airport
from app.models.flights import Flight
from app.models.recommendation_weights import (
    RecommendationMode,
    RecommendationWeight,
)
from app.services.seat_service import SeatService

START_DATE = date(2026, 10, 24)
DAYS = 7  # increase for more data (each day adds ~140 flights, ~25k seats)
SLOT_HOURS = [6, 9, 13, 17, 21]  # 5 flights per route per day

rng = random.Random(42)  # deterministic: same values on every run

AIRPORTS = [
    ("BOM", "Chhatrapati Shivaji Maharaj International Airport", "Mumbai"),
    ("DEL", "Indira Gandhi International Airport", "New Delhi"),
    ("BLR", "Kempegowda International Airport", "Bengaluru"),
    ("HYD", "Rajiv Gandhi International Airport", "Hyderabad"),
    ("MAA", "Chennai International Airport", "Chennai"),
    ("CCU", "Netaji Subhas Chandra Bose International Airport", "Kolkata"),
    ("GOI", "Dabolim Airport", "Goa"),
    ("PNQ", "Pune Airport", "Pune"),
    ("AMD", "Sardar Vallabhbhai Patel International Airport", "Ahmedabad"),
]

# (airport A, airport B, typical duration in minutes, typical base price in INR)
ROUTE_PAIRS = [
    ("BOM", "DEL", 130, 5500),
    ("BOM", "BLR", 100, 4200),
    ("BOM", "HYD", 90, 3800),
    ("BOM", "GOI", 70, 3000),
    ("BOM", "MAA", 115, 4300),
    ("BOM", "CCU", 165, 6200),
    ("BOM", "AMD", 70, 2800),
    ("DEL", "BLR", 170, 6000),
    ("DEL", "HYD", 135, 5200),
    ("DEL", "MAA", 175, 6300),
    ("DEL", "CCU", 135, 5000),
    ("DEL", "PNQ", 125, 4600),
    ("BLR", "MAA", 65, 2800),
    ("BLR", "HYD", 80, 3000),
]

AIRLINES = [
    ("Air India", "AI"),
    ("IndiGo", "6E"),
    ("SpiceJet", "SG"),
    ("Vistara", "UK"),
    ("Akasa Air", "QP"),
]

RECOMMENDATION_WEIGHTS = [
    (RecommendationMode.CHEAPEST, "0.70", "0.10", "0.20"),
    (RecommendationMode.FASTEST, "0.10", "0.70", "0.20"),
    (RecommendationMode.BALANCED, "0.40", "0.30", "0.30"),
]


def seed_airports(db):
    airport_map = {}
    for code, name, city in AIRPORTS:
        airport = db.query(Airport).filter(Airport.iata_code == code).first()
        if not airport:
            airport = Airport(iata_code=code, name=name, city=city, country="India")
            db.add(airport)
            db.flush()
        airport_map[code] = airport
    db.commit()
    return airport_map


def seed_recommendation_weights(db):
    for mode, price_w, duration_w, stops_w in RECOMMENDATION_WEIGHTS:
        exists = (
            db.query(RecommendationWeight)
            .filter(RecommendationWeight.mode == mode)
            .first()
        )
        if exists:
            continue
        db.add(
            RecommendationWeight(
                mode=mode,
                price_weight=price_w,
                duration_weight=duration_w,
                stops_weight=stops_w,
            )
        )
    db.commit()


def build_route_templates():
    """One template per (directional route, slot). Same flight number runs daily."""
    templates = []
    route_idx = 0
    for a, b, base_duration, base_price in ROUTE_PAIRS:
        for origin, dest in ((a, b), (b, a)):
            for slot, hour in enumerate(SLOT_HOURS):
                airline, prefix = AIRLINES[(route_idx + slot) % len(AIRLINES)]
                minute = rng.choice([0, 15, 30, 45])

                duration = base_duration + rng.randint(-8, 12)
                price = base_price * (0.9 + rng.random() * 0.3)
                stops = 0

                # roughly 1 in 7 flights is a slower, cheaper one-stop service
                if (route_idx + slot) % 7 == 0:
                    stops = 1
                    duration += 70
                    price *= 0.85

                if base_duration <= 80:
                    aircraft = "ATR 72" if slot % 2 == 0 else "Airbus A320"
                else:
                    aircraft = "Airbus A320" if slot % 2 == 0 else "Boeing 737"

                templates.append(
                    {
                        "flight_number": f"{prefix}{100 + route_idx * 10 + slot}",
                        "airline": airline,
                        "origin": origin,
                        "dest": dest,
                        "hour": hour,
                        "minute": minute,
                        "duration": duration,
                        "price": int(round(price / 50.0) * 50),
                        "stops": stops,
                        "aircraft": aircraft,
                    }
                )
            route_idx += 1
    return templates


def seed_flights(db, airport_map):
    templates = build_route_templates()
    created = skipped = 0

    for day_offset in range(DAYS):
        day = START_DATE + timedelta(days=day_offset)

        for t in templates:
            # small per-day price variation so ranking has something to compare
            day_price = int(round(t["price"] * (0.95 + rng.random() * 0.10) / 50.0) * 50)

            departure = datetime.combine(day, datetime.min.time()).replace(
                hour=t["hour"], minute=t["minute"]
            )
            arrival = departure + timedelta(minutes=t["duration"])

            exists = (
                db.query(Flight)
                .filter(
                    Flight.flight_number == t["flight_number"],
                    Flight.departure_time == departure,
                )
                .first()
            )
            if exists:
                skipped += 1
                continue

            flight = Flight(
                flight_number=t["flight_number"],
                airline=t["airline"],
                origin_airport_id=airport_map[t["origin"]].id,
                destination_airport_id=airport_map[t["dest"]].id,
                departure_time=departure,
                arrival_time=arrival,
                duration_minutes=t["duration"],
                base_price=day_price,
                aircraft_type=t["aircraft"],
                stops=t["stops"],
            )

            try:
                db.add(flight)
                db.flush()
                SeatService.generate_for_flight(db, flight)
                db.commit()
                created += 1
            except IntegrityError:
                db.rollback()
                skipped += 1
            except Exception as e:
                db.rollback()
                print(f"Skipped {t['flight_number']} on {day}: {e}")

        print(f"{day}: done (created so far: {created})")

    return created, skipped


def main():
    db = SessionLocal()
    try:
        print("Seeding airports...")
        airport_map = seed_airports(db)

        print("Seeding recommendation weights...")
        seed_recommendation_weights(db)

        print(f"Seeding flights + seats from {START_DATE} for {DAYS} days...")
        created, skipped = seed_flights(db, airport_map)

        print(f"Done. Created {created} flights, skipped {skipped} existing.")
        print(f"Total flights in DB: {db.query(Flight).count()}")
    finally:
        db.close()


if __name__ == "__main__":
    main()