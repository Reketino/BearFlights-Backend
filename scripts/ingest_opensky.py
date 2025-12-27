from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
import math
from typing import Any, List, cast
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


FUN_FACTS = {
    "Germany": "Germany has one of the largest aviation networks in Europe.",
    "United Kingdom": "London is served by six major airports.",
    "Norway": "Norway operates one of the world's shortest commercial runways.",
}


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



# COLLECTING DEPARTURE COUNTRY FOR TABLE
def fetch_departure_country(
    token: str,
    icao24: str,
    begin: int,
    end: int,
) -> str | None:
    
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
        return None
    
    
    raw_any = res.json()
    
    if not isinstance(raw_any, list) or not raw_any:
        return None
    
    raw = cast (list[Any], raw_any)
    
    flights: list[dict[str, Any]] = [
        f for f in raw if isinstance(f, dict)
    ]
    
    if not flights:
        return None
    
    last_flight = flights[-1]
    
    
    dep_airport = last_flight.get("estDepartureAirport")
    
    if not isinstance(dep_airport, str):
        return None
    
    return airport_to_country(dep_airport)


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
    dep_country = fetch_departure_country(
        token,
        icao24,
        begin_ts,
        end_ts,
    )
    
    if not dep_country:
        continue
    
    
    supabase.table("flights").update(
        {"departure_country": dep_country}
    ).eq("icao24", icao24).eq("date", today).execute()



# Daily Summary Of Flights    
    supabase.table("daily_flights").upsert(
        {
            "date": today,
            
            
            "closest_icao24": nearest_flight["icao24"] if nearest_flight else None,
            "closest_callsign": nearest_flight["callsign"] if nearest_flight else None,
            "closest_distance_km": nearest_flight["distance_km"] if nearest_flight else None,
            
            
            "longest_icao24": longest_flight["icao24"] if longest_flight else None,
            "longest_callsign": longest_flight["callsign"] if longest_flight else None,
            "longest_distance_km": longest_flight["distance_km"] if longest_flight else None,
            
            
            "origin_country": longest_flight["country"]if longest_flight else None,
            
            "fun_fact": ( 
                FUN_FACTS.get(
                    longest_flight["origin"],
                    "No Flights detected in Sykkylven Today."
                )                
             
                if longest_flight 
                else "No flights detected in Sykkylven Today."
            ),
        
            "total_flights": len(rows),
        },
        on_conflict="date",
    ).execute()
    
    
# CONFIRM SHIPPING ROWS TO SUPABASE    
print("FINITO 🚀")
