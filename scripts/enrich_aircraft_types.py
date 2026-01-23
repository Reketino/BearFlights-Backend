from typing import Any, cast
import os
from dotenv import load_dotenv
from supabase import create_client

from opensky.api import fetch_aircraft_type

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
    
    flights = res.data or []
    if not flights:
        print("No aircraft types collected (aircraft_type)")
        return
    
    print(f"enriching {len(flights)}")