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

def enrich_aircraft(icao24: str, typecode: str | None) -> str | None:
    aircraft = (
        supabase
        .table("aircraft_registry")
        .select("model")
        .eq("icao24", icao24)
        .limit(1)
        .execute()
    )
    
    if aircraft.data:
        row = cast(dict[str, str], aircraft.data[0])
        return row["model"]
    
    return aircraft_from_typecode(typecode)

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
    
    cache: dict[str, str | None] = {}
    
    for raw in flights:
        flight = cast(dict[str, Any], raw)
        
        icao24 = flight.get("icao24")
        date = flight.get("date")
        
        if not isinstance(icao24, str) or not date:
            continue
        
        found_in_registry = False
        
        if icao24 not in cache:
            registry = (
                supabase
                .table("aircraft_registry")
                .select("typecode")
                .eq("icao24", icao24)
                .limit(1)
                .execute()
            )
            
            if registry.data:
                row = cast(dict[str, Any], registry.data[0])
                cache[icao24] = row.get("typecode")
                found_in_registry = True
            else:
                cache[icao24] = fetch_aircraft_type(icao24, token)
            
        aircraft_type = cache[icao24]
        if aircraft_type is None:
            continue
        
        if not found_in_registry:
            supabase.table("aircraft_registry"). insert({
                "icao24": icao24,
                "typecode": aircraft_type,
            }, upsert=True).execute()
        
        aircraft_name = enrich_aircraft(icao24, aircraft_type)
        
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
            .eq("date", date)
            .execute()
        )
        
        print(f"{icao24} -> {aircraft_type} ({aircraft_name})")
        
if __name__ == "__main__":
    enrich_aircraft_types()
        
        