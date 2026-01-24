from __future__ import annotations
from typing import Any, cast
from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client
from opensky.airline.airline import airline_from_callsign

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

# Enrichment script w/ limit of enriching 100 flights
def enrich_airlines(limit: int = 100) -> None: # Wanna enrich more or less flights?, adjust int number. 
    res = (
        supabase
        .table("flights")
        .select("icao24, callsign, date")
        .is_("airline", None)
        .limit(limit)
        .execute()
    )
    
    # Flights defined as default value
    flights = res.data or []
    
    if not flights:
        print("Zero flights to enrich w/ airlines")
        return
    
    print(f"enriching {len(flights)} flights (airlines)")
    
    for raw in flights:
        flight = cast(dict[str, Any], raw)
        callsign = flight.get("callsign")
        
        # Return nothing if there is no callsign
        if not isinstance(callsign, str):
            continue
        
        
        result = airline_from_callsign(callsign)
        if not result:
            continue
        
        airline_icao, airline = result
        
        
        (
            supabase
            .table("flights")
            .update({
                "airline": airline,
                "airline_icao": airline_icao,
            })
            .eq("icao24", flight["icao24"])
            .eq("date", flight["date"])
            .execute()
        )
        
        print(f"{callsign}-> {airline}")
        
if __name__ == "__main__":
    enrich_airlines()