from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

from typing import Any, cast
from supabase import create_client

from opensky.enrich import fetch_estimated_route_from_callsign


# Supbase Connection
supabase = create_client(
    SUPABASE_URL := __import__("os").environ["SUPABASE_URL"],
    SUPABASE_SERVICE_ROLE_KEY := __import__("os").environ["SUPABASE_SERVICE_ROLE_KEY"],
)

# Logic behind enrichment
def enrich_routes(limit: int = 50) -> None:
    res = (
        supabase
        .table("flights")
        .select("icao24, callsign, date")
        .is_("route", None)
        .limit(limit)
        .execute()
    )
    
    flights = res.data or []
    
    
    if not flights:
        print("Zero flights to enrich")
        return
    
    print(f"enriching {len(flights)} flights (estimated routes)")
    
    for flight_any in flights:
        flight = cast(dict[str, Any], flight_any)
        
        callsign = flight.get("callsign")
        if not isinstance(callsign,str):
            continue
        
        
        route = fetch_estimated_route_from_callsign(callsign)
        if not route:
            print(f" {callsign}: no route found")
            continue
        
        (
            supabase
            .table("flights")
            .update({
                "route": route,
                "route_confidence": "estimated",    
            })
            .eq("icao24", flight["icao24"])
            .eq("date", flight["date"])
            .execute()
        )
        
        print(f" {callsign}: {route}")
        
        
if __name__ == "__main__":
    enrich_routes()