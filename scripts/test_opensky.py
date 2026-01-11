import requests
from opensky.auth import get_opensky_token

# Token described
token = get_opensky_token()

# Error if token is missing
if not token:
    raise RuntimeError("Access Token is missing")

# Test token at Opensky
res = requests.get(
    "https://opensky-network.org/api/states/all",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)

# Consol logging
print("STATUS:", res.status_code)
print(res.text[:200])