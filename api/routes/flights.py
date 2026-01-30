from fastapi import APIRouter, Depends
from api.app.auth import verify_api_key

router = APIRouter()

@router.get("/", dependencies=[Depends(verify_api_key)])
def list_flights():
    return {"message": "Flights endpoint is in the air✈️"}
