from db import supabase
from generate import aircraft_generated_description

def get_aircraft_description_chached(icao: str) -> str:
    icao = icao.upper()
    
    cached = (
        supabase
        .table("aircraft_ai_description")
        .select("description")
        .eq("icao", icao)
        .single()
        .execute()
    )