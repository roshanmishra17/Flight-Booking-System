from sqlalchemy import Column, Integer, String, CheckConstraint
from backend.app.core.database import Base
from sqlalchemy.orm import relationship

class Airport(Base):
    __tablename__ = "airports"

    __table_args__ = (
        CheckConstraint("iata_code = UPPER(iata_code)", name="ck_airport_iata_uppercase"),
    )

    id = Column(Integer, primary_key=True)

    iata_code = Column(
        String(3),
        unique=True,
        index=True,
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    city = Column(
        String(100),
        nullable=False
    )

    country = Column(
        String(100),
        nullable=False
    )

    origin_flights = relationship(
        "Flight",
        foreign_keys="Flight.origin_airport_id",
        back_populates="origin_airport",
    )

    destination_flights = relationship(
        "Flight",
        foreign_keys="Flight.destination_airport_id",
        back_populates="destination_airport",
    )
    origin_searches = relationship(
        "Search",
        foreign_keys="Search.origin_airport_id",
        back_populates="origin_airport",
    )

    destination_searches = relationship(
        "Search",
        foreign_keys="Search.destination_airport_id",
        back_populates="destination_airport",
    )