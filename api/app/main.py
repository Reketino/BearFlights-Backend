from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.app.routes.aircraft import router as aircraft_router

app = FastAPI(title="BearFlights AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    aircraft_router,
    prefix="/aircraft",
)

@app.get("/health")
def health():
    return {"status": "BearAI is operating"}
