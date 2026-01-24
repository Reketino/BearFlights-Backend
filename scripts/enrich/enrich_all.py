from scripts.enrich.enrich_aircraft_types import enrich_aircraft_types
from scripts.enrich.enrich_airlines import enrich_airlines

def main():
    try:
        enrich_airlines(limit=100)
    except Exception as e:
        print("[WARN] enrichment of airlines failed, skip🦘:", e)
        
    try:
        enrich_aircraft_types(limit=100)
    except Exception as e:
        print("[WARN] enrichment of aircrafts failed, skip🦘:", e)
    

if __name__ == "__main__":
    main()