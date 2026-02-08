from fastapi import APIRouter, Depends, Query
from api.app.auth import verify_api_key
from api.app.rate_limit import rate_limit
from api.app.models.flight import FlightResponse, PaginatedFlights
from api.app.db.supaflights import fetch_paginated_flights


router = APIRouter(
    dependencies=[
        Depends(verify_api_key),
        Depends(rate_limit),
    ]
)

@router.get("/", response_model=PaginatedFlights) 
def list_flights(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0) 
) -> PaginatedFlights:
    total, flights = fetch_paginated_flights(
        limit=limit,
        offset=offset,
    )
    
    items = [FlightResponse(**flight) for flight in flights]
    
    return PaginatedFlights (
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )
