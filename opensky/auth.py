import requests
from .config import OPENSKY_CLIENT_ID, OPENSKY_CLIENT_SECRET

OAUTH_TOKEN_URL = (
    "https://auth.opensky-network.org/auth/realms/"
    "opensky-network/protocol/openid-connect/token"
)

def get_opensky_token() -> str:
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
        timeout=20,
    )
    
    res.raise_for_status()
    data = res.json()
    
    if "access_token" not in data:
        raise RuntimeError(f"Missing access_token in response: {data}")
    
    token = data["access_token"]
    
    if not isinstance(token, str):
        raise RuntimeError("access_token is not a string")
    
    return token