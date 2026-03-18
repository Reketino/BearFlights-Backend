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
        
        registry = (
            self.supabase
            .table("aircraft_registry")
            .select("typecode, model")
            .eq("icao24", icao24)
            .limit(1)
            .execute()
        )
        
        typecode = None
        model = None
        
        if registry.data:
            row = cast(dict[str, Any], registry.data[0])
            typecode = row.get("typecode")
            model = row.get("model")
            
        if not typecode:
            typecode = fetch_aircraft_type(icao24, self.token)
            
        if typecode:
            self.supbase.table("aircraft_registry").upsert({
                "icao24": icao24,
                "typecode": typecode,
            }).execute()
            
        self.cache[icao24] = (typecode, model)
        return self.cache[icao24]
    
    def get_aircraft_name(self, typecode: str | None, model: str | None) -> None:
        if model:
            return model
        return aircraft_from_typecode(typecode)