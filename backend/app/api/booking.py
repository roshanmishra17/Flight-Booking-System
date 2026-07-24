from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.users import User, UserRole
from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
)
from app.services.booking_service import BookingService
from app.core.exceptions import BookingNotFoundError, FlightNotFoundError, SeatAlreadyBookedError, SeatNotBelongsToFlightError, SeatNotFoundError

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        booking = BookingService.create_booking(
            db=db,
            current_user=current_user,
            booking_data=booking_data,
        )
        return BookingResponse.model_validate(booking)

    except (FlightNotFoundError, SeatNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except SeatNotBelongsToFlightError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except SeatAlreadyBookedError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get(
    "/me",
    response_model=list[BookingResponse],
)
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookings = BookingService.get_my_bookings(
        db,
        current_user,
    )

    return [
        BookingResponse.model_validate(booking)
        for booking in bookings
    ]

@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        booking = BookingService.get_booking_by_id(
            db=db,
            booking_id=booking_id,
            current_user=current_user,
        )

        return BookingResponse.model_validate(booking)

    except BookingNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
