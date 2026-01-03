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


OAUTH_TOKEN_URL = (
    "https://auth.opensky-network.org/auth/realms/"
    "opensky-network/protocol/openid-connect/token"
)


OPENSKY_CLIENT_ID = os.environ["OPENSKY_CLIENT_ID"]
OPENSKY_CLIENT_SECRET = os.environ["OPENSKY_CLIENT_SECRET"]



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
    
    print(f"♻️ Enriching {len(flights)} flights...")
    
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
            print(f"🆘 {flight['icao24']}: route not ready yet")
            continue
        
        supabase.table("flights").update(
            {"route": f"{dep}-{arr}"}
        ).eq("icao24", flight["icao24"]) \
         .eq("date", flight["date"]) \
         .execute()
      
        
        print(f"💹 {flight['icao24']}: {dep}-{arr}")
         
def get_opensky_token() -> str:
    res = requests.post(
        OAUTH_TOKEN_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "client_credentials",
            "client_id": OPENSKY_CLIENT_ID,
            "client_secret": OPENSKY_CLIENT_SECRET,
        },
        timeout=20,
    )

    if res.status_code != 200:
        raise RuntimeError("OAuth failed")

    data = res.json()

    if "access_token" not in data:
        raise RuntimeError("Missing access_token in response")

    token = data["access_token"]

    if not isinstance(token, str):
        raise RuntimeError("access_token is not a string")

    return token         
         
if __name__ == "__main__":
    token = get_opensky_token()
    enrich_flights(token)   
      





        