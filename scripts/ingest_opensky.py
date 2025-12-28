from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
import math
from typing import Any, List, TypedDict, cast
from datetime import datetime, timezone

import requests
from supabase import create_client



# ENV SETUP 
def require_env(name: str) -> str:
    value = os.getenv(name)
    if not isinstance(value, str) or value == "":
        raise RuntimeError(f"Missing env var: {name}")
    return value


OPENSKY_CLIENT_ID = require_env("OPENSKY_CLIENT_ID")
OPENSKY_CLIENT_SECRET = require_env("OPENSKY_CLIENT_SECRET")
SUPABASE_URL = require_env("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = require_env("SUPABASE_SERVICE_ROLE_KEY")



# SUPABASE CONNECTION
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


# OPENSKY API ENDPOINTS 
OAUTH_TOKEN_URL = (
    "https://auth.opensky-network.org/auth/realms/"
    "opensky-network/protocol/openid-connect/token"
)

STATES_URL = "https://opensky-network.org/api/states/all"


FLIGHTS_BY_AIRCRAFT_URL = "https://opensky-network.org/api/flights/aircraft"



# GEO FILTER AROUND SYKKYLVEN
CENTER_LAT = 62.392497
CENTER_LON = 6.578392

RADIUS_KM = 50.0
EARTH_RADIUS_KM = 6371.0



State = List[Any]


# GEO UTILS FOR SPECIFIC 50 KM
def haversine_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(dlon / 2) ** 2
    )
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return EARTH_RADIUS_KM * c


# DEFINED DEPARTURE COUNTRIES
def airport_to_country(icao: str | None) -> str | None:
    if not icao:
        return None

    if icao.startswith("EN"):
        return "Norway"
    if icao.startswith("ED"):
        return "Germany"
    if icao.startswith("LF"):
        return "France"
    if icao.startswith("EG"):
        return "United Kingdom"
    if icao.startswith("EH"):
        return "Netherlands"
    
    return "Unknown"
    


# AUTH FROM OPENSKY
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
        timeout=10,
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



# DATA FETCHING FROM OPENSKY
def fetch_states(token: str) -> list[State]:
    res = requests.get(
        STATES_URL,
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=20,
    )

    if res.status_code != 200:
        raise RuntimeError(
            f"OpenSky fetch failed: {res.status_code} {res.text}"
        )

    data: dict[str, Any] = res.json()
    raw_states = data.get("states")

    if not isinstance(raw_states, list):
        return []

    return cast(list[State], raw_states)




class OpenSkyFlight(TypedDict, total=False):
    estDepartureAirport: str | None
    estArrivalAirport: str | None



# COLLECTING FLIGHT ROUTE
def fetch_flight_route(
    token: str,
    icao24: str,
    begin: int,
    end: int,
) -> tuple[str | None, str | None]:
    
    res = requests.get(
        FLIGHTS_BY_AIRCRAFT_URL,
        headers={
            "Authorization": f"Bearer {token}",
        },
        params={
            "icao24": icao24,
            "begin": begin,
            "end": end,   
        },
        timeout=20,
    )
    
    
    if res.status_code != 200:
        return None, None
    
    
    raw_any = res.json()
    
    
    if not isinstance(raw_any, list) or not raw_any:
        return None, None
    
    
    raw = cast(list[dict[str, Any]], raw_any)
    
    
    raw_flights: list[dict[str, Any]] = raw
    
    
    flights: list[OpenSkyFlight] = [
        cast(OpenSkyFlight, f) for f in raw_flights
    ]
    
    if not flights:
        return None,None
    
    last_flight = flights[-1]
    
    
    dep = last_flight.get("estDepartureAirport")
    arr = last_flight.get("estArrivalAirport")
    

    dep_airport = dep if isinstance(dep, str) else None
    arr_airport = arr if isinstance(arr, str) else None
   
    return dep_airport, arr_airport


# RUN SCRIPT
print("Fetching OpenSky (OAuth2)…")

token = get_opensky_token()
states = fetch_states(token)

print("States:", len(states) if states else "NULL")

if not states:
    print("No data received")
    raise SystemExit("We have received zero data")


now = datetime.now(timezone.utc).isoformat()
today = datetime.now(timezone.utc).date().isoformat()


rows: list[dict[str, Any]] = []
position_rows: list[dict[str, Any]] = []


nearest_distance: float | None = None
nearest_flight: dict[str, Any] | None = None


longest_distance: float | None = None
longest_flight: dict[str, Any] | None = None



for s in states:
    if len(s) < 14:
        continue
    
    
    lon = s[5]
    lat = s[6]
    
    
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        continue
    
    
    distance_km = haversine_km(
        CENTER_LAT,
        CENTER_LON,
        float(lat),
        float(lon),
    )
    
    
    if distance_km > RADIUS_KM:
        continue
    
    
    callsign = s[1]
    
    # Nearest Flight Tracking
    if nearest_distance is None or distance_km < nearest_distance:
        nearest_distance = distance_km
        nearest_flight = {
            "icao24": s[0],
            "callsign": callsign.strip() if isinstance(callsign, str) else None,
            "origin": s[2],
            "distance_km": round(distance_km, 2),            
        }
        
    # Longest Flight Tracking    
    if longest_distance is None or distance_km > longest_distance:
        longest_distance = distance_km
        longest_flight = {
            "icao24": s[0],
            "callsign": callsign.strip() if isinstance(callsign, str) else None,
            "origin": s[2],
            "distance_km": round(distance_km, 2),   
        }
        
        
        
    # FLIGHT HISTORY
    rows.append({
        "date": today,
        "icao24": s[0],
        "callsign": callsign.strip() if isinstance(callsign, str) else None,
        "origin": s[2],
        "first_seen": now,
        "last_seen": now,
        "max_altitude": s[13],
        "max_speed": s[9],
        "distance_over_area": round(distance_km, 2),
        "observations": 1,
    })
    
    
    
    # DATA FOR MAP TABLE
    position_rows.append({
        "icao24": s[0],
        "callsign": callsign.strip() if isinstance(callsign, str) else None,
        "latitude": float(lat),
        "longitude": float(lon),
        "altitude": s[7],
        "velocity": s[9],
        "last_seen": now,
    })


    
# Writing Data To Supabase    
if rows:
    supabase.table("flights").upsert(
    rows,
    on_conflict="icao24,date",
    ).execute()
    

    
# WRITING DATA TO FLIGHT POSITION TABLE    
if position_rows:
    supabase.table("flight_positions"). upsert(
        position_rows,
        on_conflict="icao24",
    ).execute()
    
    
    
print("Enriching departure countries...")


end_ts = int(datetime.now(timezone.utc).timestamp())
begin_ts = end_ts - 12 * 60 * 60


unique_icao24s = {row["icao24"] for row in rows}


for icao24 in unique_icao24s:
    dep_airport, arr_airport = fetch_flight_route(
        token,
        icao24,
        begin_ts,
        end_ts,
    )
    
    dep_country = airport_to_country(dep_airport)
    arr_country = airport_to_country(arr_airport)
    
    
    update_data: dict[str, Any] = {}
    
    
    if dep_country:
        update_data["departure_country"] = dep_country
        
        
    if arr_country:
        update_data["arrival_country"] = arr_country
        
    
    if not update_data:
        continue
    
    
    supabase.table("flights").update(update_data) \
        .eq("icao24", icao24) \
        .eq("date", today) \
        .execute()
    
  
# CONFIRM SCRIPT IS WORKING  
print("FINITO 🚀")
