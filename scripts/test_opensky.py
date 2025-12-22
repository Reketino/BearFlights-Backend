import os
import requests
from dotenv import load_dotenv

load_dotenv()

res = requests.get(
    "https://opensky-network.org/api/states/all",
    auth=(os.getenv("OPENSKY_USER"), os.getenv("OPENSKY_PASS")),
    timeout=10,
)

print("STATUS:", res.status_code)
print(res.text[:200])