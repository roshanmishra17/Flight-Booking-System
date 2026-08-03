from fastapi import APIRouter, Depends, FastAPI

from app.schemas.users import UserResponse
from app.models.users import User
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/me", response_model=UserResponse)
def get_current_user_details(
    current_user: User = Depends(get_current_user),
):
    return current_user