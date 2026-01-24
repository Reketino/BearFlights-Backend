from typing import Any, cast
import os
from dotenv import load_dotenv
from supabase import create_client

from opensky.auth import get_opensky_token
from opensky.api import fetch_aircraft_type
from opensky.aircraft.aircraft import aircraft_from_typecode

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

def enrich_aircraft_types(limit: int = 100) -> None:
    res = (
        supabase
        .table("flights")
        .select("icao24")
        .is_("aircraft_type", None)
        .limit(limit)
        .execute()
    )
    
    print("aircraft_type enrichment is now ready for Take Off🛫")
    
    flights = res.data or []
    if not flights:
        print("No aircraft types collected (aircraft_type)")
        return
    
    print(f"enriching {len(flights)}")
    
    token = get_opensky_token()
    
    cache: dict[str, str | None] = {}
    
    for raw in flights:
        flight = cast(dict[str, Any], raw)
        icao24 = flight.get("icao24")
        
        if not isinstance(icao24, str):
            continue
        
        if icao24 not in cache:
            cache[icao24] = fetch_aircraft_type(icao24, token)
            
        aircraft_type = cache[icao24]
        if aircraft_type is None:
            continue
        
        aircraft_name = aircraft_from_typecode(aircraft_type)
        
        update_data = {
            "aircraft_type":  aircraft_type,
        }
        
        
        if aircraft_name:
            update_data["aircraft_name"] = aircraft_name 
        
        (
            supabase
            .table("flights")
            .update(update_data)
            .eq("icao24", icao24)
            .execute()
        )
        
        print(f"{icao24} -> {aircraft_type} ({aircraft_name})")
        
        
if __name__ == "__main__":
    enrich_aircraft_types()
        
        