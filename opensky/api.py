import requests
from dotenv import load_dotenv
from typing import Any, cast

load_dotenv()

# States defined as "any"
State = list[Any]

# URL for data collection
STATES_URL = "https://opensky-network.org/api/states/all"
FLIGHTS_BY_AIRCRAFT_URL = "https://opensky-network.org/api/flights/aircraft"

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
    
  

  
