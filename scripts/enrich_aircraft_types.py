from typing import Any, cast
import os
from dotenv import load_dotenv
from supabase import create_client

from opensky.api import fetch_aircraft_type

load_dotenv()

supabase = create_client(
    os.environ[""]
)