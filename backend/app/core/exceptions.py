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