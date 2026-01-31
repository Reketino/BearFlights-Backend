import time
from fastapi import Request, HTTPException, status

Request_PER_WINDOW = 100
WINDOW_SECONDS = 60


_rate_limit_store: dict[str, tuple[int, float]] = {}

def rate_limit(requests: Request):
    api_key = requests.headers.get("x-api-key")
    
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    
    now = time.time()
    
    count, window_start = _rate_limit_store.get(api_key, (0, now))
    
    if now - window_start > WINDOW_SECONDS:
        count = 0
        window_start = now
        
    count += 1
    _rate_limit_store[api_key] = (count, window_start)
    
    if count > Request_PER_WINDOW:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )