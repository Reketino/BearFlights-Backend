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
            
            
        lines.append("    },\n\n")
        
    lines.append("\n\n\n")
    
    lines.append(
        "AIRCRAFT_TYPES: dict[str, str] = {\n"
        "    code: name\n"
        "    for group in AIRCRAFT_TYPES_BY_MANUFACTURER.values()\n"
        "    for code, name in group.items()\n"
        "}\n"
    )
    
    path.write_text("".join(lines), encoding="utf-8")
        
        
if __name__ == "__main__":
    sorted_aircraft_types()