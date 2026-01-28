from typing import Any


def build_flight_row(
    *,
    today: str,
    now: str,
    state: list[Any],
    distance_km: float,
    departure_airport: str | None,
    arrival_airport: str | None,
) -> dict[str, Any]:
    callsign = state[1]
    
    return {
        "date": today,
        "icao24": state[0],
        "callsign": callsign.strip() if isinstance(callsign, str) else None,
        "origin_country": state[2],
        "first_seen": now,
        "last_seen": now,
        "max_altitude": state[13],
        "max_speed": state[9],
        "distance_over_area": round(distance_km, 2),
        "observations": 1,
        "departure_airport": departure_airport,
        "arrival_airport": arrival_airport,
    }   
    
    
def build_position_row(
    *,
    now: str,
    state: list[Any],
    lat: float,
    lon: float,
    heading: float | None,
    departure_airport: str | None,
    arrival_airport: str | None,
) -> dict[str, Any]:
    callsign = state[1]
    
    return {
        "icao24": state[0],
        "callsign": callsign.strip() if isinstance(callsign, str) else None,
        "latitude": float(lat),
        "longitude": float(lon),
        "altitude": state[7],
        "velocity": state[9],
        "heading": heading,
        "departure_airport": departure_airport,
        "arrival_airport": arrival_airport,
        "last_seen": now,
    }
