from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import requests
from typing import Any, cast

import os
from datetime import datetime, timezone
from supabase import create_client


FLIGHTS_BY_AIRCRAFT_URL = "https://opensky-network.org/api/flights/aircraft"




supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)




def fetch_flight_route(
    token: str,
    icao24: str,
    observed_at: int,
) -> tuple[str | None, str | None]:
    
    begin = observed_at - 3 * 3600
    end = observed_at + 8 * 3600
    
    params: dict[str, int | str] = {
            "icao24": icao24.lower(),
            "begin": begin,
            "end": end,   
        }
    
    res = requests.get(
        FLIGHTS_BY_AIRCRAFT_URL,
        headers={
            "Authorization": f"Bearer {token}",
        },
        params=params,
        
        timeout=20,
    )
    
    
    if res.status_code != 200:
        return None, None
    
    
    data = res.json()
    
    if not isinstance(data, list) or not data:
        return None, None
    
    
    last_flight: dict[str, Any] = cast(dict[str, Any], data[-1])
    
       
    dep = cast(str | None, last_flight.get("estDepartureAirport", None))
    arr = cast(str | None, last_flight.get("estArrivalAirport", None))
    
    return (
        dep if isinstance(dep, str) else None,
        arr if isinstance(arr, str) else None,
    )
    
    return dep, arr
    

def enrich_flights(token: str) -> None:
    res = (
        supabase
        .table("flights")
        .select("icao24, first_seen, date")
        .is_("route", None)
        .limit(50)
        .execute()
    )
    
    flights = res.data or []
    
    
    if not flights:
        print("Zero flights to enrich🛬")
        return
    
    
    
    for flight_any in flights:
        flight = cast(dict[str, Any], flight_any)
        observed_at = int(
            datetime
            .fromisoformat(flight["first_seen"])
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
        
        
        dep, arr = fetch_flight_route(
            token=token,
            icao24=flight["icao24"],
            observed_at=observed_at,
        )
        
        
        if not dep or not arr:
            continue
        
        supabase.table("flights").update(
            {"route": f"{dep}-{arr}"}
        ).eq("icao24", flight["icao24"]) \
         .eq("date", flight["date"]) \
         . execute()
         
         
         
if __name__ == "__main__":
    from opensky_auth import get_opensky_token
    
    token = get_opensky_token()
    enrich_flights   
      




        