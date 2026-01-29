from opensky.auth import get_opensky_token
from opensky.api import fetch_states
from opensky.ingest import process_states

# If debug -> True
DEBUG = True

def main() -> None:
    print("Fetching OpenSky (OAuth2)…")


    try:
        token = get_opensky_token()
        if DEBUG:
            print("Token received")
     
        
        states = fetch_states(token)
        if DEBUG:
            print(f"States received: {len(states) if states else 0}")
     
        
        if not states:
            if DEBUG:
                print("No data has been received")
                return
     
        
        process_states(states, token)
        if DEBUG:
            print("Processing complete")
     
        
    except Exception as e:
        if DEBUG:
            print("🛬 Ingest has failed its mission:", e)
            raise
        
        
if __name__ == "__main__":
    main()
