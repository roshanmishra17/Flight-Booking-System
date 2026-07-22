# Authentication Exceptions

class EmailAlreadyExistsError(Exception):
    """Raised when a user tries to register with an existing email."""
    pass


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""
    pass

class AirportAlreadyExistsError(Exception):
    """Raised when an airport with the given IATA code already exists."""
    pass


#Airport Exceptions
class AirportNotFoundError(Exception):
    """Raised when the requested airport does not exist."""
    pass

class AirportInUseError(Exception):
    """Raised when an airport cannot be deleted because flights reference it."""
    pass

#Flight Exceptions
class FlightNotFoundError(Exception):
    pass


class FlightAlreadyExistsError(Exception):
    pass


class FlightInUseError(Exception):
    pass

class InvalidFlightRouteError(Exception):
    pass


class InvalidFlightScheduleError(Exception):
    pass


# Seats Exceptions
class SeatError(Exception):
    """Base exception for seat-related errors."""
    pass


class SeatNotFoundError(SeatError):
    """Raised when a seat does not exist."""
    pass


class FlightSeatsNotFoundError(SeatError):
    """Raised when a flight has no seats."""
    pass


class UnsupportedAircraftTypeError(SeatError):
    """Raised when no seat layout exists for the aircraft type."""
    pass


#Booking Exception
class BookingError(Exception):
    """Base booking exception."""


class BookingNotFoundError(BookingError):
    pass


class SeatAlreadyBookedError(BookingError):
    pass


class SeatNotBelongsToFlightError(BookingError):
    pass


class InvalidBookingStatusError(BookingError):
    pass


class BookingAlreadyCancelledError(BookingError):
    pass


class BookingAlreadyConfirmedError(BookingError):
    pass