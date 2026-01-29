from __future__ import annotations

from datetime import date
from supabase import create_client
from typing import Any, TypedDict, cast
import os

from dotenv import load_dotenv
load_dotenv()


class FlightRow(TypedDict):
    icao24: str
    callsign: str | None
    distance_over_area: float
    observations: int
    
    
class DailyFlightPayLoad(TypedDict):
    date: str
    total_flights: int
    closest_icao24: str
    closest_callsign: str | None
    closest_distance_km: float
    longest_icao24: str
    longest_callsign: str | None
    longest_distance_km: float
    observations: int
    fun_fact: str

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

today = date.today().isoformat()

existing = supabase.table("daily_flights") \
    .select("date") \
    .eq("date", today) \
    .limit(1) \
    .execute()

if existing.data:
    print("Daily summary already up to date, skip🦘")
    raise SystemExit()

res = supabase.table("flights") \
    .select("icao24, callsign, distance_over_area, observations") \
    .eq("date", today) \
    .execute()
    
raw_rows = res.data or []

rows: list[FlightRow] = [
    cast(FlightRow, r)
    for r in raw_rows
    if isinstance(r, dict)
    and r.get("distance_over_area") is not None
]

if not rows:
    print("No Flights Today Aye")
    raise SystemExit()


total_flights = len({r["icao24"] for r in rows})

closest = min(rows, key=lambda r: r["distance_over_area"])
longest = max(rows, key=lambda r: r["distance_over_area"])

payload: DailyFlightPayLoad = {
    "date": today,
    "total_flights":total_flights,
    "closest_icao24": closest["icao24"],
    "closest_callsign": closest["callsign"],
    "closest_distance_km": closest["distance_over_area"],
    "longest_icao24": longest["icao24"],
    "longest_callsign": longest["callsign"],
    "longest_distance_km": longest["distance_over_area"],
    "observations": sum(r["observations"] for r in rows),
    "fun_fact": f"{closest['callsign']} buzzed closest today🐝",
}

supabase.table("daily_flights") \
    .upsert(cast(Any, payload), on_conflict="date") \
        .execute()
        
print("Daily summary picked up and delivered📨")