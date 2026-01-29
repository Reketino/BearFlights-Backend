from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_flights():
    return {"message": "Flights endpoint is in the air✈️"}
