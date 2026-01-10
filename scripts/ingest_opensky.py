from opensky.auth import get_opensky_token
from opensky.api import fetch_states
from opensky.ingest import process_states

import sys
print("CWD:", __import__("os").getcwd())
print("SYSPATH:", sys.path)


def main() -> None:
    print("Fetching OpenSky (OAuth2)…")

    try:
        token = get_opensky_token()
        states = fetch_states(token)
        
        if not states:
            print("No data has been received")
            return
        
        process_states(states, token)
        
    except Exception as e:
        print("🛬 Ingest has failed its mission:", e)
        
        
if __name__ == "__main__":
    main()
