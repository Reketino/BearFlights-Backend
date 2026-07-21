from pathlib import Path
from opensky.airline.airlines_icao import AIRLINES_BY_REGION

def sorted_airlines() -> None:
    path = Path(__file__).parent / "airlines_icao.py"
    
    lines: list[str] = []
    lines.append("#Callsign of airline companies defined\n")
    lines.append("AIRLINES_BY_REGION: dict[str, dict[str, str]] = {\n\n")
    
    for region in sorted(AIRLINES_BY_REGION):
        airlines = AIRLINES_BY_REGION[region]
        lines.append(f'     "{region}": {{\n')
        
        for code, name in sorted(
            airlines.items(), 
            key=lambda item: item[1].casefold(),
        ):
            lines.append(f'       "{code}": "{name}",\n')
            
        lines.append("    },\n\n")
        
    lines.append("}\n\n\n")
    
    lines.append(
        "ICAO_AIRLINES: dict[str, str] = {\n"
        "    code: name\n"
        "    for group in AIRLINES_BY_REGION.values()\n"
        "    for code, name in group.items()\n"
        "}\n"
    )
    
    path.write_text("".join(lines), encoding="utf-8")
    
    # Run script w/: python -m opensky.airline.utils
        
if __name__ == "__main__":
    sorted_airlines()