import time
from fastapi import Request, HTTPException, status
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

AI_REQUESTS_PER_WINDOW = 3
AI_WINDOW_SECONDS = 60

_store_ai_rate_limit: dict[str, tuple[int, float]] = {}

def ai_rate_limiter(
    limit: int = AI_REQUESTS_PER_WINDOW, 
    per: int = AI_WINDOW_SECONDS
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
    
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            request: Request | None = None
            
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
                
            if request is None: 
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if request is None:
                raise HTTPException(
                    status_code=500,
                    detail="Requested object is not found for rate-limiting",
                )
            
            client = request.client
            if client is None:
                raise HTTPException(
                    status_code=500,
                    detail="Client for IP rate limiting can't be determined"
                )
            
                
            client_ip = client.host
            now = time.time()
            
            count, window_start = _store_ai_rate_limit.get(client_ip, (0, now))
            
            if now - window_start > per:
                count = 0
                window_start = now
                
            count += 1
            _store_ai_rate_limit[client_ip] = (count, window_start)
            
            if count > limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many Requests for AI to process, cooldown in progress..."
                )
                
            return func(*args, **kwargs)
        
        return wrapper
    return decorator