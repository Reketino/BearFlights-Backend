from pathlib import Path
from opensky.aircraft.aircraft_names import AIRCRAFT_TYPES_BY_MANUFACTURER

def sorted_aircraft_types() -> None:
    path = Path(__file__).parent / "aircraft_names.py"
    
    lines: list[str] = []
    lines.append("AIRCRAFT_TYPES_BY_MANUFACTURER: dict[str, dict[str, str]] = {\n}")
    
    for manufacturer, aircrafts in AIRCRAFT_TYPES_BY_MANUFACTURER.items():
        lines.append(f'    "{manufacturer}": {{\n')
        
        for code, name in sorted(aircrafts.items(), key=lambda x: x[0]):
            lines.append(f'        "{code}": "{name}",\n')
        
        
if __name__ == "__main__":
    sorted_aircraft_types()