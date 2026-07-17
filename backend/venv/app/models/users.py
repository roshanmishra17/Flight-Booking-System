from sqlalchemy import Column, Integer, String, DateTime, Enum, text
from sqlalchemy.sql import func
from app.core.database import Base
import enum
from sqlalchemy.orm import relationship


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String(100), unique=True, index=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    full_name = Column(String(100), nullable=False)

    role = Column(
        Enum(
            UserRole,
            values_callable=lambda x: [e.value for e in x],
            name="user_role",
        ),
        nullable=False,
        default=UserRole.USER,
        server_default=text("'user'"),
    )
    
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    bookings = relationship(
        "Booking",
        back_populates="user",
    )
    searches = relationship(
        "Search",
        back_populates="user",
    )
    saved_flights = relationship(
        "SavedFlight",
        back_populates="user",
    )