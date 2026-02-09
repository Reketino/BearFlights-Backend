from typing import Any
from datetime import datetime, timezone

# Imports from components
from opensky.api import fetch_flight_airport
from opensky.geo import haversine_km
from opensky.builders import build_flight_row, build_position_row
from opensky.config import CENTER_LAT, CENTER_LON, RADIUS_KM, DEBUG
from db.supabase import upsert_flights, upsert_positions

# Defining of states w/timestamp, position & dep
def is_valid_state(state: list[Any]) -> bool:
    return (
        len(state) >= 14
        and isinstance(state[0], str)
        and isinstance(state[5], (int, float))
        and isinstance(state[6], (int, float))   
    )

    
def is_inside_radius(lat: float, lon: float) -> tuple[bool, float]:
    distance_km = haversine_km(
        CENTER_LAT,
        CENTER_LON,
        lat,
        lon,
    )
    return distance_km <= RADIUS_KM, distance_km


def get_airports(
    icao24: str,
    cache: dict[str, tuple[str | None, str | None]],
    token: str,
    begin_ts: int,
    end_ts: int
) -> tuple[str | None, str | None]:
    
    if icao24 not in cache:
        cache[icao24] = (
            fetch_flight_airport(token, icao24, begin_ts, end_ts)
            if token
            else (None, None)
        )
            
    return cache[icao24]
            

def process_states(states: list[list[Any]], token: str) -> None: 
    end_ts = int(datetime.now(timezone.utc).timestamp())
    begin_ts = end_ts - 12 * 60 * 60
    
    now = datetime.now(timezone.utc).isoformat()
    today = datetime.now(timezone.utc).date().isoformat()
    
    rows: list[dict[str, Any]] = []
    position_rows: list[dict[str, Any]] = []
    
    airport_cache: dict[str, tuple[str | None, str | None]] = {}
    
    departure_hits = 0
    departure_misses = 0
    arrival_hits = 0
    arrival_misses = 0
    inside_radius = 0
    
    if DEBUG:
        valid_states = sum(1 for s in states if is_valid_state(s))
        print(f"[CHECK] valid state rows: {valid_states}/{len(states)}")

    # States defined
    for state in states:
        if not is_valid_state(state):
            continue
    
        icao24 = state[0]
        lon = float(state[5])
        lat = float (state[6])
        
        inside, distance_km = is_inside_radius(lat, lon)
        if not inside:
            continue
        
        inside_radius += 1
        
        departure_airport, arrival_airport = get_airports(
            icao24=icao24,
            cache=airport_cache,
            token=token,
            begin_ts=begin_ts,
            end_ts=end_ts,
        )
        
        departure_hits += bool(departure_airport)   
        departure_misses += not bool(departure_airport)
        arrival_hits += bool(arrival_airport)
        arrival_misses += not bool(arrival_airport)
        
        #  Flight row builder
        rows.append(
            build_flight_row(
                today=today,
                now=now,
                state=state,
                distance_km=distance_km,
                departure_airport=departure_airport,
                arrival_airport=arrival_airport,
            )
        )
        
        # Position row builder
        position_rows.append(
            build_position_row(
                now=now,
                state=state,
                lat=float(lat),
                lon=float(lon),
                heading=state[10] if isinstance(state[10], (int, float)) else None,
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