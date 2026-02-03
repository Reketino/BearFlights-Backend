import time
from fastapi import requests, HTTPException, status
from functools import wraps

AI_REQUESTS_PER_WINDOW = 3
AI_WINDOW_SECONDS = 60

_store_ai_rate_limit: dict[str, tuple[int, float]] = {}

