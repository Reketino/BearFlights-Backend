from typing import Optional, Tuple
from opensky.airline.airline import airline_from_callsign


class AirlineService:
    def get_airlines(self, callsign: str) -> Optional[Tuple[str, str]]:
        if not callsign:
            return None
        
    