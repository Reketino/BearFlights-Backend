from typing import Any, cast
from supabase import client

from opensky.api import fetch_aircraft_type
from opensky.aircraft.aircraft import aircraft_from_typecode

class AircraftService:
    def __init__(self, supabase: Client, token: str):
        self.supabase = supabase
        self.token = token
        self.cache: dict[str, tuple[str | None, str | None]] = {}
    
        
    def get_or_fetch_aircraft(self, icao24: str) -> tuple[str | None, str | None]:
        if icao24 in self.cache:
            return self.cache[icao24]