from typing import Any, cast
import os
from dotenv import load_dotenv
from supabase import create_client
from opensky.auth import get_opensky_token
from opensky.services.aircraft_service import AircraftService

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

def enrich_aircraft_types(limit: int = 100) -> None:
    res = (
        supabase
        .table("flights")
        .select("icao24, date, aircraft_type, aircraft_name")
        .or_("aircraft_name.is.null,aircraft_name.eq.")
        .order("first_seen", desc=True)
        .limit(limit)
        .execute()
    )
    
    print(f"Found {len(res.data or [])} Flight has gone missing, can't seem to find him")
    
    flights = res.data or []
    if not flights:
        print("No aircraft types collected (aircraft_type)")
        return
    
    print(f"enriching {len(flights)}")
    
    token = get_opensky_token()
    
    service = AircraftService(supabase, token)
    
    for flight_data in flights:
        flight = cast(dict[str, Any], flight_data)
        
        icao24 = flight.get("icao24")
        date = flight.get("date")
        
        if not isinstance(icao24, str) or not date:
            continue
        
        aircraft_type, model = service.get_or_fetch_aircraft(icao24)
        
        existing_type = flight.get("aircraft_type")
        
        if aircraft_type is None and isinstance(existing_type, str):
            aircraft_type = existing_type
                
        if aircraft_type is None:
            continue
        
        aircraft_name = service.get_aircraft_name(aircraft_type, model)
        
        update_data: dict[str, str] = {
            "aircraft_type": aircraft_type,
        }
        if aircraft_name:
            update_data["aircraft_name"] = aircraft_name 
        
        (
            supabase
            .table("flights")
            .update(update_data)
            .eq("icao24", icao24)
            .eq("date", date)
            .execute()
        )
       
        print(f"{icao24} -> {aircraft_type} ({aircraft_name})")
        
        
# Run script w/ python -m scripts.enrich.enrich_aircraft_types
if __name__ == "__main__":
    enrich_aircraft_types()
        
        