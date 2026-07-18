from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.airport import Airport


class AirportRepository:
    @staticmethod
    def get_by_id(db: Session, airport_id: int) -> Airport | None:
        return db.query(Airport).filter(Airport.id == airport_id).first()

    @staticmethod
    def get_by_iata_code(db: Session, iata_code: str) -> Airport | None:
        return db.query(Airport).filter(Airport.iata_code == iata_code).first()

    @staticmethod
    def get_all(db: Session) -> list[Airport]:
        return db.query(Airport).order_by(Airport.city).all()

    @staticmethod
    def create(
        db: Session,
        *,
        iata_code: str,
        name: str,
        city: str,
        country: str,
    ) -> Airport:
        new_airport = Airport(
            iata_code=iata_code,
            name=name,
            city=city,
            country=country,
        )
        db.add(new_airport)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(new_airport)
        return new_airport

    @staticmethod
    def update(db: Session, airport: Airport) -> Airport:
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(airport)
        return airport

    @staticmethod
    def delete(db: Session, airport: Airport) -> None:
        db.delete(airport)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise