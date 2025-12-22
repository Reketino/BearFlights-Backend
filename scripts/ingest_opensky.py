from dotenv import load_dotenv
load_dotenv()

import os
import requests
from datetime import datetime, timezone
from supabase import create_client



# ENV 
OPENSKY_CLIENT_ID = os.getenv("OPENSKY_CLIENT_ID")
OPENSKY_CLIENT_SECRET = os.getenv("OPENSKY_CLIENT_SECRET")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not all([
    OPENSKY_CLIENT_ID,
    OPENSKY_CLIENT_SECRET,
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
]):
    raise RuntimeError("Missing env vars")



# CONNECTION TO SUPABASE
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)



#ENDPOINTS FOR OPENSKY
OAUTH_TOKEN_URL = (
    "https://auth.opensky-network.org/auth/realms/"
    "opensky-network/protocol/openid-connect/token"
)

STATES_URL = "https://opensky-network.org/api/states/all"



# AUTH
def get_opensky_token() -> str:
    res = requests.post(
        OAUTH_TOKEN_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "client_credentials",
            "client_id": OPENSKY_CLIENT_ID,
            "client_secret": OPENSKY_CLIENT_SECRET,
        },
        timeout=10,
    )

    print("TOKEN STATUS:", res.status_code)

    if res.status_code != 200:
        print(res.text)
        raise RuntimeError("OAuth failed")

    return res.json()["access_token"]



# DATA FETCHING
def fetch_states(token: str) -> list:
    res = requests.get(
        STATES_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=20,
    )

    if res.status_code != 200:
        raise RuntimeError(f"OpenSky fetch failed: {res.status_code} {res.text}")

    return res.json().get("states", [])



# RUN OPENSKY
print("Fetching OpenSky (OAuth2)…")

token = get_opensky_token()
states = fetch_states(token)

print("States:", len(states) if states else "NULL")

if not states:
    print("No data received")
    raise SystemExit(0)


now = datetime.now(timezone.utc).isoformat()
today = datetime.now(timezone.utc).date().isoformat()

rows = []

for s in states[:10]:  # ingest only 10 as of now
    rows.append({
        "date": today,
        "icao24": s[0],
        "callsign": s[1].strip() if s[1] else None,
        "origin": s[2],
        "first_seen": now,
        "last_seen": now,
        "max_altitude": s[13],
        "max_speed": s[9],
        "distance_over_area": None,
        "observations": 1,
    })


supabase.table("flights").upsert(
    rows,
    on_conflict="icao24,date"
).execute()

# IF CONNECTED AND DATA COLLECTED RETURN 👇🏻
print("FINITO 🚀")
