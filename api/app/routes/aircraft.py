from fastapi import APIRouter, HTTPException, Request
from opensky.aircraft_ai.generate import aircraft_generated_description
from app.ai_rate_limiter import ai_rate_limiter

router = APIRouter(
    prefix="/aircraft",
    tags=["Aircraft"],
)

@router.get(
    "/{icao}/ai",
    summary="Generate AI description for aircraft type",
    description="This AI model generates a live description for a give aircraft IACO type. w/ rate-limit.",
)

@ai_rate_limiter(limit=3, per=60)
def ai_aircraft_description(
    icao: str,
    request: Request,
):
    _ = request
     
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