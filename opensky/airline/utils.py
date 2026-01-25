from opensky.airline.airlines_icao import ICAO_AIRLINES

def sorted_airlines() -> None:
    for key, value in sorted(ICAO_AIRLINES.items()):
        print(f'"{key}": "{value}",')
        
if __name__ == "__main__":
    sorted_airlines()