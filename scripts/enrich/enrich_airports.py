from typing import Any, cast
import os
from dotenv  import load_dotenv
from supabase import create_client

from opensky.airports.airport import resvolve_airport_name

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

def enrich_airports(limit: int = 100) -> None: