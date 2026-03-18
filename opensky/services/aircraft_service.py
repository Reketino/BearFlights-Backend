from typing import Any, cast
from supabase import client

from opensky.api import fetch_aircraft_type
from opensky.aircraft.aircraft import aircraft_from_typecode

