from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)
from app.core.database import get_db
from app.schemas.users import (
    Token,
    UserCreate,
    UserResponse,
    UserLogin
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """
    try:
        return AuthService.register(
            db=db,
            user_data=user_data,
        )

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return a JWT access token.
    """
    try:
        return AuthService.login(
            db=db,
            credentials=credentials,
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )