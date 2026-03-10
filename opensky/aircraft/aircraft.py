from opensky.aircraft.aircraft_names import AIRCRAFT_TYPES

def aircraft_from_typecode(typecode: str | None) -> str | None:
    if not typecode: 
        return None
    
    code = typecode.strip().upper()
    
    aircraft = AIRCRAFT_TYPES.get(code)
    
    if not aircraft:
        print(f"Unknown aircraft type: {code}")
    
    return aircraft or code