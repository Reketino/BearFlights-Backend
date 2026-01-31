from typing import Any
from datetime import datetime, timezone

# Imports from components
from opensky.api import fetch_flight_airport
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
    
    if DEBUG:
        valid_states = sum(
            1 for s in states 
            if len(s) >= 7
        )
        print(f"[CHECK] valid state rows: {valid_states}/{len(states)}")
    
    rows: list[dict[str, Any]] = []
    position_rows: list[dict[str, Any]] = []
    
    airport_cache: dict[str, tuple[str | None, str | None]] = {}
    departure_hits = 0
    departure_misses = 0
    arrival_hits = 0
    arrival_misses = 0
    
    
    inside_radius: int = 0

    # States defined
    for s in states:
        if len(s) < 14:
            continue
    
        icao24 = s[0]
        lon = s[5]
        lat = s[6]
        
        if (
            not isinstance(icao24, str)        
            or not isinstance(lat, (int, float)) 
            or not isinstance(lon, (int, float))
            
        ): 
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
        
        inside_radius += 1
    
        # Cache check for dep airport
        if icao24 not in airport_cache:
            if token:
                    airport_cache[icao24] = fetch_flight_airport(
                        token, icao24, begin_ts, end_ts
                        )
                    
            else:
                airport_cache[icao24] = (None, None)
        
        departure_airport, arrival_airport = airport_cache[icao24]
        
        if departure_airport:
            departure_hits += 1   
        else:
            departure_misses += 1
            
        if arrival_airport:
            arrival_hits += 1
        else:
            arrival_misses += 1
        
        #  Flight row builder
        rows.append(
            build_flight_row(
                today=today,
                now=now,
                state=s,
                distance_km=distance_km,
                departure_airport=departure_airport,
                arrival_airport=arrival_airport,
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
                arrival_airport= arrival_airport,
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
            f"Finito 🚀 rows={len(rows)} | "
            f"inside_radius={inside_radius} | "
            f"dep_hits={departure_hits} dep_miss={departure_misses}"
            f"arr_hits={arrival_hits} arr_miss={arrival_misses}"
        )