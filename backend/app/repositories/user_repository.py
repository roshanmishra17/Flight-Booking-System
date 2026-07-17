from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session

from app.models.users import User


class UserRepository:

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        email: str,
        full_name: str,
        hashed_password: str,
    ) -> User:
        user = User(
            email=email,
            full_name=full_name,
            password_hash=hashed_password,
        )

        try:

            db.add(user)
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise

        return user