from typing import TypedDict



class Flightrow(TypedDict):
    icao24: str
    callsign: str | None
    distance_over_area: float
    observations: int
    
    
class DailyFlightPayLoad(TypedDict):
    date: str
    totalt_flights: int
    closest_icao24: str
    closest_callsign: str | None
    closest_distance_km: float
    longest_icao24: str
    longest_callsign: str | None
    longest_distance_km: float
    observations: int
    fun_fact: str
    