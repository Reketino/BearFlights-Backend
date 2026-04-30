import time
import requests
from .config import OPENSKY_CLIENT_ID, OPENSKY_CLIENT_SECRET

OAUTH_TOKEN_URL = (
    "https://auth.opensky-network.org/auth/realms/"
    "opensky-network/protocol/openid-connect/token"
)

def get_opensky_token() -> str:
    for attempt in range(3):
        try:
            res = requests.post(
                OAUTH_TOKEN_URL,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "client_credentials",
                    "client_id": OPENSKY_CLIENT_ID,
                    "client_secret": OPENSKY_CLIENT_SECRET,
                },
                timeout=10,
            )
    
            res.raise_for_status()
            data = res.json()
    
            if "access_token" not in data:
                raise RuntimeError(f"Missing access_token in response: {data}")
    
            token = data["access_token"]
    
            if not isinstance(token, str):
                raise RuntimeError("access_token is not a string")
    
            return token
        
        except requests.exceptions.RequestException as e:
            print(f"Retry {attempt+1}/3 failed: {e}")
            time.sleep(2)
            
    raise RuntimeError("Opensky token will not fetch, even w/ retries")