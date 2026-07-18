from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import (
    AirportAlreadyExistsError,
    AirportInUseError,
    AirportNotFoundError,
)
from app.dependencies.auth import get_current_admin
from app.models.users import User
from app.schemas.airport import (
    AirportCreate,
    AirportResponse,
    AirportUpdate,
)
from app.services.airport_service import AirportService

router = APIRouter(
    prefix="/airports",
    tags=["Airports"],
)


@router.post(
    "",
    response_model=AirportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_airport(
    airport_data: AirportCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    try:
        return AirportService.create_airport(db, airport_data)
    except AirportAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.get(
    "",
    response_model=list[AirportResponse],
)
def get_airports(
    db: Session = Depends(get_db),
):
    return AirportService.get_airports(db)


@router.get(
    "/{airport_id}",
    response_model=AirportResponse,
)
def get_airport(
    airport_id: int,
    db: Session = Depends(get_db),
):
    try:
        return AirportService.get_airport(db, airport_id)
    except AirportNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put(
    "/{airport_id}",
    response_model=AirportResponse,
)
def update_airport(
    airport_id: int,
    updates: AirportUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    try:
        return AirportService.update_airport(
            db=db,
            airport_id=airport_id,
            updates=updates,
        )
    except AirportNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except AirportAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.delete(
    "/{airport_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_airport(
    airport_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    try:
        AirportService.delete_airport(db, airport_id)
    except AirportNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except AirportInUseError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e