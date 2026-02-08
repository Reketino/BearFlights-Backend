from db import supabase
from generate import aircraft_generated_description
from typing import TypedDict, Optional, cast, Any

class AircraftAICacheRow(TypedDict):
    description: str

def get_aircraft_description_cached(icao: str) -> str:
    icao = icao.upper()
    
    cached: Any = (
        supabase
        .table("aircraft_ai_descriptions") # type: ignore[]
        .select("description") 
        .eq("icao", icao)
        .single()
        .execute()
    )
    
    data = cast(Optional[AircraftAICacheRow], cached.data)
    
    if data is not None: 
        return data["description"]
    
    description = aircraft_generated_description(icao)
    
    supabase.table("aircraft_ai_descriptions").insert({ # type: ignore
        "icao": icao,
        "description":description, 
    }).execute()
    
    return description