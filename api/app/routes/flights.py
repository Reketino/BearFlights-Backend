from fastapi import APIRouter, Depends
from api.app.auth import verify_api_key
from api.app.rate_limit import rate_limit

router = APIRouter(
    dependencies=[
        Depends(verify_api_key),
        Depends(rate_limit),
    ]
)

@router.get("/") 
def list_flights():
    return {"message": "Flights endpoint is in the air✈️"}
