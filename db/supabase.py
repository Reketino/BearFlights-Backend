from typing import Any
from supabase import create_client
from skyopen.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)

def upsert_flights (rows: list[dict[str, Any]]) -> None:
    supabase.table("flights").upsert(
        rows,
        on_conflict="icao24,date",
    ).execute()
    

def upsert_positions(rows: list[dict[str, Any]]) -> None:
    supabase.table("flight_positions"). upsert(
        rows,
        on_conflict="icao24",
    ).execute()