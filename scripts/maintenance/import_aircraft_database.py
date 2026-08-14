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