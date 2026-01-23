from opensky.aircraft.aircraft_names import AIRCRAFT_TYPES

def aircraft_from_typecode(typecode: str) -> str | None:
    if not typecode: 
        return None
    
    return AIRCRAFT_TYPES.get(typecode.upper())