from db import supabase
from generate import aircraft_generated_description
from typing import TypedDict, Optional, cast 
from postgrest import ApiResponse # type: ignore

class AircraftAICacheRow(TypedDict):
    description: str

def get_aircraft_description_cached(icao: str) -> str:
    icao = icao.upper()
    
    response: ApiResponse = ( # type: ignore[]
        supabase
        .table("aircraft_ai_descriptions") # type: ignore[]
        .select("description") 
        .eq("icao", icao)
        .maybe_single()
        .execute()
    )
    
    data = cast(Optional[AircraftAICacheRow], response.data) # type: ignore
    
    if data: 
        return data["description"]
    
    description = aircraft_generated_description(icao)
    
    supabase.table("aircraft_ai_descriptions").insert({ # type: ignore
        "icao": icao,
        "description":description, 
    }).execute()
    
    return description