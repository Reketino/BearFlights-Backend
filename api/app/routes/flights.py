from fastapi import APIRouter, Depends
from api.app.auth import verify_api_key
from api.app.rate_limit import rate_limit
from api.app.models.flight import FlightResponse
from api.app.db.supaflights import fetch_flights


router = APIRouter(
    dependencies=[
        Depends(verify_api_key),
        Depends(rate_limit),
    ]
)

@router.get("/", response_model=list[FlightResponse]) 
def list_flights():
    flights_from_supabase = fetch_flights(limit=50)
    return flights_from_supabase
