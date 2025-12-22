from dotenv import load_dotenv
load_dotenv()

import os
import requests
from datetime import datetime
from supabase import create_client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not all([SUPABASE_URL, 
            SUPABASE_SERVICE_ROLE_KEY
]):
    raise RuntimeError("Missing env vars")


supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

LAT = 62.39324
LON = 6.58026
RADIUS_KM = 50

url = f"https://api.adsb.lol/v2/lat/{LAT}/lon/{LON}/dist/{RADIUS_KM}"

print("Fetching ADSB (adsb.lol)…")
res = requests.get(
    url,
    headers={
        "User-Agent": "BearFlightIngest/1.0",
        "Accept": "application/json"
    },
    timeout=20
)

print("Status:", res.status_code)
res.raise_for_status()

data = res.json()
aircraft = data.get("ac")

print("Aircraft:", 0 if not aircraft else len(aircraft))



if not res.headers.get("Content-Type", "").startswith("application/json"):
    raise RuntimeError("Response is not JSON")

data = res.json()
aircraft = data.get("ac")


print("Aircraft:", 0 if not aircraft else len(aircraft))



if not aircraft:
    print("Dead sky, 0 aircraft")
    exit(0)
    
now = datetime.utcnow().isoformat()
today = datetime.utcnow().date().isoformat()


rows = []


for a in aircraft[:10]:
    rows.append({
        "date": today,
        "icao24": a.get("hex"),
        "callsign": a.get("flight"),
        "origin": a.get("from"),
        "first_seen": now,
        "last_seen":now,
        "max_altitude": a.get("alt_baro"),
        "max_speed": a.get("gs"),
        "distance_over_area": a.get("dst"),
        "observations": 1,
    })
    
    
supabase.table("flights").upsert(
    rows,
    on_conflict="icao24,date"
).execute()
    
    
print("FINITO")