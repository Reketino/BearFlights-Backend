from pydantic import BaseModel
from typing import List

class FlightResponse(BaseModel):
    icao24: str
    callsign: str | None
    aircraft_name: str | None
    departure_airport: str | None
    departure_airport_name: str | None
    arrival_airport: str | None
    arrival_airport_name: str | None
    distance_over_area: float | None
    
    
class PaginatedFlights(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[FlightResponse]