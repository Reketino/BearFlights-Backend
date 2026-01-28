from typing import Any, cast
import os
from dotenv  import load_dotenv
from supabase import create_client

from opensky.airports.airport import resolve_airport_name

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

def enrich_airports(limit: int = 100) -> None:
    res = (
        supabase
        .table("flights")
        .select(
            "icao24, date, departure_airport, arrival_airport"
        )
        .or_(
            "departure_airport_name.is.null,"
            "arrival_airport_name.is.null"
        )
        .limit(limit)
        .execute()
    )
    
    flights = res.data or []
    if not flights:
        print("Huston we can't find any flights to enrich")
        
    print(f"enriching {len(flights)} flights (airport)")
    
    for raw in flights:
        flight = cast(dict[str, Any], raw)
        
        dep_icao = flight.get("departure_airport")
        arr_icao = flight.get("arrival_airport")
        
        dep_name = resolve_airport_name(dep_icao)
        arr_name = resolve_airport_name(arr_icao)
        
        if not dep_name and not arr_name:
            continue
        
        update_data: dict[str, Any] = {}
        
        if dep_name:
            update_data["departure_airport_name"] = dep_name
        if arr_name:
            update_data["arrival_airport_name"] = arr_name
            
        (
            supabase
            .table("flights")
            .update(update_data)
            .eq("icao24", flight["icao24"])
            .eq("date", flight["date"])
            .execute()
        )
        
        print(
            f"{flight['icao24']} | "
            f"{dep_icao}->{dep_name} | "
            f"{arr_icao}->{arr_name}"
        )
        
if __name__ == "__main__":
    enrich_airports()