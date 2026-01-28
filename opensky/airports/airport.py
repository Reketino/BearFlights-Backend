from opensky.airports.airport_icao import AIRPORTS_BY_ICAO

def resvolve_airport_name(icao: str | None) -> str | None:
    if not icao:
        return None
    
    airport = AIRPORTS_BY_ICAO.get(icao.upper())
    if not airport:
        return None
    
    return airport["name"]