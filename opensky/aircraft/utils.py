from opensky.aircraft.aircraft_names import AIRCRAFT_TYPES

def sorted_aircraft_types() -> None:
    for key, value in sorted(AIRCRAFT_TYPES.items()):
        print(f'"{key}": "{value}",')
        
        
if __name__ == "__main__":
    sorted_aircraft_types()