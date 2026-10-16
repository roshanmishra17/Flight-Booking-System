from datetime import date, datetime, time, timedelta

from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.models.airport import Airport
from app.models.flights import Flight
from app.services.seat_service import SeatService


# Departures start on 17 October 2026 and cover 30 calendar days, inclusive.
START_DATE = date(2026, 10, 17)
DAYS_TO_SEED = 30
FLIGHTS_PER_ROUTE_PER_DAY = 5

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

# Directed routes from the previous seed file.
ROUTES = [
    ("BOM", "DEL"), ("DEL", "BOM"),
    ("BOM", "BLR"), ("BLR", "BOM"),
    ("DEL", "BLR"), ("BLR", "DEL"),
    ("BOM", "HYD"), ("DEL", "HYD"),
    ("BOM", "GOI"), ("BLR", "MAA"),
    ("DEL", "PNQ"), ("MAA", "HYD"),
]

# Five departures per route per day.
DEPARTURE_TIMES = [
    time(6, 0),
    time(9, 0),
    time(12, 0),
    time(16, 0),
    time(20, 0),
]


def seed_airports(db):
    """Create missing airports and return a mapping keyed by IATA code."""
    airport_map = {}

    for airport_data in AIRPORTS:
        airport = (
            db.query(Airport)
            .filter(Airport.iata_code == airport_data["iata_code"])
            .first()
        )

        if airport is None:
            airport = Airport(**airport_data)
            db.add(airport)
            db.flush()

        airport_map[airport_data["iata_code"]] = airport

    db.commit()
    return airport_map


def seed_flights(db, airport_map):
    """Create 5 flights per route per day, including seats.

    Flight numbers and departure times are deterministic, so rerunning this
    script skips already-seeded flights rather than duplicating them.
    Existing database records are not deleted or updated.
    """
    created_count = 0
    skipped_count = 0

    for route_index, (origin_code, destination_code) in enumerate(ROUTES):
        origin = airport_map[origin_code]
        destination = airport_map[destination_code]

        for day_offset in range(DAYS_TO_SEED):
            travel_day = START_DATE + timedelta(days=day_offset)

            for slot, departure_clock in enumerate(DEPARTURE_TIMES):
                airline = AIRLINES[(route_index + slot) % len(AIRLINES)]
                flight_number = f"{airline['prefix']}{100 + route_index * 10 + slot:03d}"
                departure_time = datetime.combine(travel_day, departure_clock)

                existing = (
                    db.query(Flight)
                    .filter(
                        Flight.flight_number == flight_number,
                        Flight.departure_time == departure_time,
                    )
                    .first()
                )
                if existing is not None:
                    skipped_count += 1
                    continue

                # Reproducible values make repeat runs consistent.
                duration_minutes = 60 + ((route_index * 17 + slot * 23) % 151)
                arrival_time = departure_time + timedelta(minutes=duration_minutes)
                base_price = 3000 + ((route_index * 431 + slot * 275) % 5001)
                aircraft_type = AIRCRAFT_TYPES[(route_index + slot) % len(AIRCRAFT_TYPES)]

                flight = Flight(
                    flight_number=flight_number,
                    airline=airline["name"],
                    origin_airport_id=origin.id,
                    destination_airport_id=destination.id,
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    duration_minutes=duration_minutes,
                    base_price=base_price,
                    aircraft_type=aircraft_type,
                    stops=0,
                )

                try:
                    db.add(flight)
                    db.flush()  # Ensure flight.id exists before creating seats.
                    SeatService.generate_for_flight(db, flight)
                    db.commit()
                    created_count += 1
                    print(
                        f"Created {flight_number}: {origin_code} -> {destination_code} "
                        f"on {departure_time:%Y-%m-%d %H:%M}"
                    )
                except IntegrityError:
                    db.rollback()
                    skipped_count += 1
                    print(
                        f"Skipped duplicate/conflicting flight {flight_number} "
                        f"at {departure_time:%Y-%m-%d %H:%M}"
                    )
                except Exception as exc:
                    db.rollback()
                    print(
                        f"Failed {flight_number} ({origin_code}->{destination_code}, "
                        f"{departure_time:%Y-%m-%d %H:%M}): {exc}"
                    )

    expected_count = len(ROUTES) * DAYS_TO_SEED * FLIGHTS_PER_ROUTE_PER_DAY
    print("\nFlight seeding summary")
    print(f"Expected flight slots in this date window: {expected_count}")
    print(f"New flights created: {created_count}")
    print(f"Existing/conflicting flights skipped: {skipped_count}")


def main():
    db = SessionLocal()
    try:
        print("Seeding airports...")
        airport_map = seed_airports(db)

        print(
            f"Seeding flights and seats from {START_DATE.isoformat()} "
            f"for {DAYS_TO_SEED} days..."
        )
        seed_flights(db, airport_map)
        print("Seeding finished.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
