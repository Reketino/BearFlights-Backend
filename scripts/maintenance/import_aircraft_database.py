from __future__ import annotations

import csv
import io
import os
import zipfile
from typing import Any, cast

import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

AIRCRAFT_DATABASE_URL = (
    "https://s3.opensky-network.org/"
    "data-samples/metadata/aircraftDatabase.zip"
)

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

def download_aircraft_database() -> bytes:
    print("Downloading Opensky aircraft database...")

    response = requests.get(
        AIRCRAFT_DATABASE_URL,
        timeout=60,
    )

    response.raise_for_status()

    print(
        f"Downloaded {len(response.content) / 1024 / 1024:.1f} MB"
    )

    return response.content

def read_aircraft_database(
    content: bytes,
) -> list[dict[str, str | None]]:
    print("Reading aircraftDatabase.csv...")
    
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        csv_name = next(
            (
                name
                for name in archive.namelist()
                if name.endswith("aircraftDatabase.csv")
            ),
            None,
        )