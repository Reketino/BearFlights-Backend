from fastapi import APIRouter, HTTPException, Request
from opensky.aircraft_AI.generate import aircraft_generated_description


router = APIRouter(
    prefix="/aircraft",
    tags=["Aircraft"],
)

@router.get(
    "/{icao}/ai",
    summary="Generate AI description for aircraft type",
    description="This AI model generates a live description for a give aircraft IACO type. w/ rate-limit.",
)

@rate_limit(limit=3, per=60)
def ai_aircraft_description(
    icao: str,
    request: Request,
):
    try:
        description = aircraft_generated_description(icao.upper())
        return {
            "icao": icao.upper(),
            "description": description,
        }
        
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="We have failed to generate aircraft description",
        )