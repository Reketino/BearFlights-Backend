from fastapi import FastAPI
from api.app.routes import flights

app = FastAPI(title="BearFlights API")

app.include_router(
    flights.router,
    prefix="/flights",
    tags=["flights"],   
)

@app.get("/health")
def health():
    return{"status": "ok, we are healthy"}