import requests
from dotenv import load_dotenv
from typing import Any, List,  cast

load_dotenv()

# States defined as "any"
State = List[Any]

# URL for data collection
STATES_URL = "https://opensky-network.org/api/states/all"
FLIGHTS_BY_AIRCRAFT_URL = "https://opensky-network.org/api/flights/aircraft"
AIRCRAFT_META_URL = "https://opensky-network.org/api/metadata/aircraft/icao"

# Collecting States
def fetch_states(token: str) -> list[State]:
    res = requests.get(
        STATES_URL,
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=20,
    )
    res.raise_for_status()
    return cast(list[State], res.json().get("states", []))

# COLLECTING AIRCRAFT TYPES
def fetch_aircraft_type(icao24: str, token: str) -> str | None:
    res = requests.get(
        f"{AIRCRAFT_META_URL}/{icao24}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=10,
    )
    
    if res.status_code!= 200:
        return None
    
    data = res.json()
    typecode = data.get("typecode")
    return typecode if isinstance(typecode, str) else None

# Collecting Dep airport 
def fetch_flight_airport(
    token: str, 
    icao24: str, 
    begin: int, 
    end: int,
    ) -> tuple[str | None, str | None]:
    res = requests.get(
        FLIGHTS_BY_AIRCRAFT_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={"icao24": icao24, "begin": begin, "end": end},
        timeout=15,
    )  
    if res.status_code != 200:
        return None, None
    
    flights = res.json()
    if not flights:
        return None, None
    
    last = flights [-1]
    
    dep = last.get("estDepartureAirport")
    arr = last.get("estArrivalAirport")
    return( 
        dep if isinstance(dep, str) else None,
        arr if isinstance(arr, str) else None,
        )
    
  

  
