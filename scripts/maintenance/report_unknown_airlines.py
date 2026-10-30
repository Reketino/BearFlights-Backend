from __future__ import annotations

import os
from collections import Counter
from typing import Any, cast

from dotenv import load_dotenv
from supabase import create_client

from opensky.airline.airlines_icao import ICAO_AIRLINES

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
) 

def report_unknown_airlines() -> None:
    """Report flights with missing or unknown airline mappings."""
    
    response = (supabase .table("flights") .select("callsign, airline") .execute())
    
    flights = response.data or []
    unknown_prefixes: Counter[str] = Counter()
    empty_callsigns = 0
    missing_airline = 0
    
    for flight_data in flights:
        flight = cast(dict[str, Any], flight_data)
        
        airline = flight.get("airline")
        if isinstance(airline, str) and airline.strip():
            continue
        
        missing_airline += 1
        callsign = flight.get("callsign")
        
        if not isinstance(callsign, str) or not callsign.strip():
            empty_callsigns += 1
            continue
        
        if len(callsign) < 3:
            unknown_prefixes[callsign] += 1
            continue
        
        
    
