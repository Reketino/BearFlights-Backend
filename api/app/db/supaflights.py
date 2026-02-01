from typing import Any, cast
from api.app.db.supabase import supabase

def fetch_flights(limit: int = 50) -> list[dict[str, Any]]:
    res = (
        supabase
        .table("flights")
        .select(
            "icao24,"
            "callsign,"
            "aircraft_name,"
            "departure_airport,"
            "arrival_airport,"
            "arrival_airport_name,"
            "distance_over_area"
        )
        .order("first_seen", desc=True)
        .limit(limit)
        .execute()
    )
    
    return cast(list[dict[str, Any]], res.data or [])


def fetch_paginated_flights(
    *,
    limit: int,
    offset: int,
) -> tuple[int, list[dict[str, Any]]]:
    
    total_res = (
        supabase
        .table("flights")
        .select("id", count=cast(Any, "exact"),)
        .execute()
    )
    total = total_res.count or 0
    
    res = (
        supabase
        .table("flights")
        .select(
            "icao24,"
            "callsign,"
            "aircraft_name,"
            "departure_airport,"
            "arrival_airport,"
            "arrival_airport_name,"
            "distance_over_area"
        )
        .order("first_seen", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    
    return total, cast(list[dict[str, Any]], res.data or [])
    