from typing import Any, TypedDict, cast
from pyopensky.rest import REST  # type: ignore

rest = REST()  # type: ignore

# RouteResponse classified as Typedict
class RouteResponse(TypedDict, total=False):
    route: list[str]

# Defining data for supabase
def fetch_estimated_route_from_callsign(
    callsign: str,
) -> str | None:
    try:
        raw: Any = rest.routes(callsign)  # type: ignore
        
        if not isinstance(raw, dict):
            return None
        
        # Cast for validating script 
        data = cast (RouteResponse, raw)  
        route = data.get("route")

        if route and len(route) == 2:
            return f"{route[0]}-{route[1]}"

    except Exception:
        return None

    return None


