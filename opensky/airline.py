from opensky.airlines_icao import ICAO_AIRLINES

# Airline function w/ input intake 
def airline_from_callsign(callsign: str) -> tuple [str, str] | None:
    if not callsign or len(callsign) < 3:
        return None
    
    icao = callsign[:3].upper() # Collecting ICAO code
    airline = ICAO_AIRLINES.get(icao) # Check ICAO_AIRLINES for names
    
    # Returning nothing if no Airline is found
    if not airline:
        return None

    return icao, airline