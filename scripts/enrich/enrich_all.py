from scripts.enrich.enrich_aircraft_types import enrich_aircraft_types
from scripts.enrich.enrich_airlines import enrich_airlines

def main() -> None:
    enrich_airlines(limit=100)
    enrich_aircraft_types(limit=100)
    

if __name__ == "__main__":
    main()