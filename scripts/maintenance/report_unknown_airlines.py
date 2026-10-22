from __future__ import annotations

import os
from collections import Counter
from typing import Any, cast

from dotenv import load_dotenv
from supabase import create_client

from opensky.airline.airlines_icao import ICAO_AIRLINES

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
) 