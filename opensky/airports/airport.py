from opensky.airports.airport_icao import AIRPORTS_BY_ICAO

def resolve_airport_name(icao: str | None) -> str | None:
    if not icao:
        return None
    
    airport = AIRPORTS_BY_ICAO.get(icao.upper())
    return airport["name"] if airport else None