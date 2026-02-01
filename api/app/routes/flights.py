from fastapi import APIRouter, Depends
from typing import Any
from api.app.auth import verify_api_key
from api.app.rate_limit import rate_limit
from api.app.models.flight import FlightResponse


router = APIRouter(
    dependencies=[
        Depends(verify_api_key),
        Depends(rate_limit),
    ]
)

@router.get("/", response_model=list[FlightResponse]) 
def list_flights():
    return flights_from_db
