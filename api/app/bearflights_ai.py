from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from api.app.routes.aircraft import router as aircraft_router

app = FastAPI("BearFlights AI")

app.include_router(
    aircraft_router,
    prefix="/aircraft",
    tags=["Aircratf"],
)

app.get("/health")
def health():
    return {"status": "BearAI is operating"}
