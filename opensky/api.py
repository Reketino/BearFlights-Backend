import requests
from dotenv import load_dotenv
from typing import Any, List, cast, TypedDict

load_dotenv()

# States defined as "any"
State = List[Any]

class AircraftMetadata(TypedDict):
    typecode: str | None
    model: str | None
    manufacturer: str | None

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
def fetch_aircraft_metadata(
    icao24: str, 
    token: str
    ) -> AircraftMetadata:
    try:
        res = requests.get(
            f"{AIRCRAFT_META_URL}/{icao24}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )
    except requests.exceptions.RequestException:
        return {
            "typecode": None,
            "model": None,
            "manufacturer": None,
        }
    
    if res.status_code!= 200:
        return {
            "typecode": None,
            "model": None,
            "manufacturer": None,
        }
    
    data = res.json()
    
    typecode = data.get("typecode")
    model = data.get("model")
    manufacturer = data.get("manufacturerName")
    
    if isinstance(typecode, str):
        typecode = typecode.strip()
        
    if isinstance(model, str):
        model = model.strip()
        
    if isinstance(manufacturer, str):
        manufacturer = manufacturer.strip()
              
    return {
        "typecode": typecode or None,
        "model": model or None,
        "manufacturer": manufacturer or None,
    }

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
    
  

  
