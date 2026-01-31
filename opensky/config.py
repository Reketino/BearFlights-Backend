import os
from dotenv import load_dotenv
load_dotenv()

# Center of Radius Aka "Sykkylven"
CENTER_LAT = 62.392497
CENTER_LON = 6.578392
RADIUS_KM = 50
EARTH_RADIUS_KM = 6371.0
DEBUG = True

# Definiton of require env w/ Guard clause
def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing env var: {name}")
    return value

# API Keys
OPENSKY_CLIENT_ID = require_env("OPENSKY_CLIENT_ID")
OPENSKY_CLIENT_SECRET = require_env("OPENSKY_CLIENT_SECRET")
SUPABASE_URL = require_env("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = require_env("SUPABASE_SERVICE_ROLE_KEY")