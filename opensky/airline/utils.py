from opensky.airline.airlines_icao import AIRLINES_BY_REGION

def sorted_airlines() -> None:
    for region, airlines in AIRLINES_BY_REGION.items():
        print(f"# {region}")
        for code, name in sorted (airlines.items(), key=lambda x: x[1]):
            print(f'"{code}": "{name}",')
        print()
        
if __name__ == "__main__":
    sorted_airlines()