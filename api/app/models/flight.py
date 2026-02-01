from pydantic import BaseModel
from typing import Optional, List

class FlightResponse(BaseModel):
    icao24: str
    callsign: Optional[str]
    aircraft_name: Optional[str]
    
    departure_airport: Optional[str]
    departure_airport_name: Optional[str]
    
    arrival_airport: Optional[str]
    arrival_airport_name: Optional[str]
    
    distance_over_area: float
    
class PaginatedFlights(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[FlightResponse]