from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    AirportAlreadyExistsError,
    AirportInUseError,
    AirportNotFoundError,
)
from app.models.airport import Airport
from app.repositories.airport_repository import AirportRepository
from app.schemas.airport import AirportCreate, AirportUpdate


class AirportService:

    @staticmethod
    def create_airport(db: Session, airport_data: AirportCreate) -> Airport:
        existing = AirportRepository.get_by_iata_code(db, airport_data.iata_code)
        if existing:
            raise AirportAlreadyExistsError(
                f"Airport with IATA code {airport_data.iata_code} already exists."
            )

        try:
            return AirportRepository.create(
                db,
                iata_code=airport_data.iata_code,
                name=airport_data.name,
                city=airport_data.city,
                country=airport_data.country,
            )
        except IntegrityError as e:
            raise AirportAlreadyExistsError(
                f"Airport with IATA code {airport_data.iata_code} already exists."
            ) from e

    @staticmethod
    def get_airport(db: Session, airport_id: int) -> Airport:
        airport = AirportRepository.get_by_id(db, airport_id)
        if not airport:
            raise AirportNotFoundError(f"Airport with id {airport_id} not found.")
        return airport

    @staticmethod
    def get_airports(db: Session) -> list[Airport]:
        return AirportRepository.get_all(db)

    @staticmethod
    def update_airport(
        db: Session,
        airport_id: int,
        updates: AirportUpdate,
    ) -> Airport:
        airport = AirportRepository.get_by_id(db, airport_id)
        if not airport:
            raise AirportNotFoundError(
                f"Airport with id {airport_id} not found."
            )
        if (
            updates.iata_code is not None
            and updates.iata_code != airport.iata_code
        ):
            existing = AirportRepository.get_by_iata_code(db, updates.iata_code)

            if existing:
                raise AirportAlreadyExistsError(
                    f"Airport with IATA code {updates.iata_code} already exists."
                )

        update_data = updates.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(airport, field, value)

        try:
            return AirportRepository.update(db, airport)
        except IntegrityError as e:
            raise AirportAlreadyExistsError(
                f"Airport with IATA code {updates.iata_code} already exists."
            ) from e

    @staticmethod
    def delete_airport(db: Session, airport_id: int) -> None:
        airport = AirportRepository.get_by_id(db, airport_id)
        if not airport:
            raise AirportNotFoundError(f"Airport with id {airport_id} not found.")

        try:
            AirportRepository.delete(db, airport)
        except IntegrityError as e:
            raise AirportInUseError(
                "Cannot delete airport with existing flights referencing it."
            ) from e