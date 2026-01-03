from __future__ import annotations

from dotenv import load_dotenv
load_dotenv

import requests
from typing import Any, cast

import os
from datetime import datetime, timezone
from supabase import create_client





FLIGHTS_BY_AIRCRAFT_URL = "https://opensky-network.org/api/flights/aircraft"


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
    
