from typing import Any
from datetime import datetime, timezone

# Imports from components
from opensky.api import fetch_departure_airport
from opensky.geo import haversine_km
from opensky.builders import build_flight_row, build_position_row
from opensky.config import CENTER_LAT, CENTER_LON, RADIUS_KM, DEBUG
from db.supabase import upsert_flights, upsert_positions

# Defining of states w/timestamp, position & dep
def process_states(states: list[list[Any]], token: str) -> None: 
    end_ts = int(datetime.now(timezone.utc).timestamp())
    begin_ts = end_ts - 12 * 60 * 60
    
    
    now = datetime.now(timezone.utc).isoformat()
    today = datetime.now(timezone.utc).date().isoformat()
    
    rows: list[dict[str, Any]] = []
    position_rows: list[dict[str, Any]] = []
    
    departure_cache: dict[str, str | None] = {}
    departure_hits = 0
    departure_misses = 0

    # States defined
    for s in states:
        if len(s) < 14:
            continue
    
        icao24 = s[0]
        if not isinstance(icao24, str):
            continue
    
        lon = s[5]
        lat = s[6]
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            continue
    
        # Distance from set radius
        distance_km = haversine_km(
            CENTER_LAT,
            CENTER_LON,
            float(lat),
            float(lon),
        )
    
        if distance_km > RADIUS_KM:
            continue
    
        # Collect flight even if no icao24
        if icao24 not in departure_cache:
            departure_cache[icao24] = fetch_departure_airport(
                token,
                icao24,
                begin_ts,
                end_ts,
            )
        
        # Collecting dep_airport
        departure_airport = departure_cache[icao24]
        
        # If dep_airport collected
        if departure_airport:
            departure_hits += 1
        
        # If not collected    
        else:
            departure_misses += 1
        
        #  Flight row builder
        rows.append(
            build_flight_row(
                today=today,
                now=now,
                state=s,
                distance_km=distance_km,
            )
        )
        
        # Heading showing as null, if no data 
        heading = s[10] if isinstance(s[10], (int, float)) else None
        
        # Position row builder
        position_rows.append(
            build_position_row(
                now=now,
                state=s,
                lat=float(lat),
                lon=float(lon),
                heading=heading,
                departure_airport=departure_airport,
            )
        )
        
    # Push flight data to Supabase    
    if rows: 
        upsert_flights(rows)
    
    # Push position data to Supabase    
    if position_rows:
        upsert_positions(position_rows)
    
    # Console check        
    if DEBUG:
        print(
            f"Finito 🚀 rows={len(rows)}"
            f"dep_hits={departure_hits} dep_miss={departure_misses}"
        )