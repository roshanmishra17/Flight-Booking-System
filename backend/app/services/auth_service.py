from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.users import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.core.exceptions import EmailAlreadyExistsError, InvalidCredentialsError

class AuthService:

    @staticmethod
    def register(
        db: Session,
        user_data: UserCreate,
    ) -> UserResponse:

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise EmailAlreadyExistsError("Email already registered.")

        hashed_password = hash_password(
            user_data.password
        )

        try:
            user = UserRepository.create(
                db=db,
                email=user_data.email,
                full_name=user_data.full_name,
                hashed_password=hashed_password,
            )

        except IntegrityError:
            raise EmailAlreadyExistsError("Email already registered.")

        return UserResponse.model_validate(user)

@staticmethod
def login(
    db: Session,
    credentials: UserLogin,
) -> Token:
    user = UserRepository.get_by_email(
        db,
        credentials.email,
    )

    if not user:
        raise InvalidCredentialsError("Invalid email or password.")

    if not verify_password(
        credentials.password,
        user.password_hash,
    ):
        raise InvalidCredentialsError("Invalid email or password.")

    token = create_access_token(user.id)

    return Token(
        access_token=token,
    )