from opensky.airlines_icao import ICAO_AIRLINES

def airline_from_callsign(callsign: str) -> tuple [str, str] | None:
    if not callsign or len(callsign) < 3:
        return None
    
    icao = callsign[:3].upper()
    airline =ICAO_AIRLINES.get(icao)

    if not airline:
        return None

    return icao, airline