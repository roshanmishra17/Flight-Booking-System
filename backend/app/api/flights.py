from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_admin
from app.core.exceptions import (
    AirportNotFoundError,
    FlightAlreadyExistsError,
    FlightInUseError,
    FlightNotFoundError,
    InvalidFlightRouteError,
    InvalidFlightScheduleError,
)
from app.models.users import User
from app.schemas.flights import (
    FlightCreate,
    FlightResponse,
    FlightUpdate,
)
from app.services.flight_service import FlightService

router = APIRouter(
    prefix="/flights",
    tags=["Flights"],
)


@router.post(
    "",
    response_model=FlightResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_flight(
    flight: FlightCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    try:
        return FlightService.create_flight(db, flight)

    except AirportNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except FlightAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    except (InvalidFlightRouteError, InvalidFlightScheduleError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
    except Exception:
        db.rollback()
        raise

@router.get(
    "/search",
    response_model=list[FlightResponse],
)
def search_flights(
    origin: str = Query(min_length=3, max_length=3),
    destination: str = Query(min_length=3, max_length=3),
    departure_date: date = Query(...),
    db: Session = Depends(get_db),
):
    try:
        return FlightService.search_flights(
            db,
            origin,
            destination,
            departure_date,
        )

    except AirportNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[FlightResponse],
)
def get_flights(
    db: Session = Depends(get_db),
):
    return FlightService.get_flights(db)


@router.get(
    "/{flight_id}",
    response_model=FlightResponse,
)
def get_flight(
    flight_id: int,
    db: Session = Depends(get_db),
):
    try:
        return FlightService.get_flight(db, flight_id)

    except FlightNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{flight_id}",
    response_model=FlightResponse,
)
def update_flight(
    flight_id: int,
    updates: FlightUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    try:
        return FlightService.update_flight(db, flight_id, updates)

    except FlightNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except AirportNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except FlightAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    except (InvalidFlightRouteError, InvalidFlightScheduleError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.delete(
    "/{flight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    try:
        FlightService.delete_flight(db, flight_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except FlightNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except FlightInUseError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )