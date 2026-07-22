from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.seats import SeatResponse
from app.services.seat_service import SeatService
from app.core.exceptions import (
    FlightNotFoundError,
    FlightSeatsNotFoundError,
)

router = APIRouter(
    prefix="/flights",
    tags=["Seats"],
)


@router.get(
    "/{flight_id}/seats",
    response_model=list[SeatResponse],
    status_code=status.HTTP_200_OK,
)
def get_seats(
    flight_id: int,
    db: Session = Depends(get_db),
):
    try:
        return SeatService.get_seats_by_flight(
            db=db,
            flight_id=flight_id,
        )

    except FlightNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found.",
        )

    except FlightSeatsNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Flight exists but has no seats.",
        )