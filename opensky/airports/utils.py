from pathlib import Path
from opensky.airports.airport_icao import AIRPORTS_BY_ICAO

def sorted_airports() -> None:
    path = Path(__file__).parent / "airports_icao.py"
    
    content = path.read_text(encoding="utf-8")
    
    namespace: dict[str, object] = {}
    exec(content,namespace)
    
    airports = namespace["AIRPORTS_BY_ICAO"]
    
    if not isinstance(airports, dict):
        raise ValueError("AIRPORTS_BY_ICAO is not a dict in the source file.")
    
    lines: list[str] = []
    lines.append("# Airports sorted by country & name\n")
    lines.append("AIRPORTS_BY_ICAO: dict[str, dict[str, str]] = {\n")
    
    sorted_airports = sorted(
        AIRPORTS_BY_ICAO.items(),
        key=lambda item: (item[1]["country"], item[1]["name"]),
    )
    
    assert all(
        isinstance(v, dict) and all(isinstance(x, str) for x in v.values())
        for  _, v in sorted_airports
    ), "AIRPORTS_BY_ICAO contains non-str values"
    
    current_country: str | None = None
    
    for icao, airport in sorted_airports:
        country = airport["country"]
        
        if country != current_country:
            lines.append(f"\n    # {country}\n")
            current_country = country
            
        lines.append(
            f'    "{icao}": {{\n'
            f'        "name": "{airport["name"]}",\n'
            f'        "country": "{airport["country"]}",\n'
            f'        "iata": "{airport["iata"]}",\n'
            f"   }},\n"
        )
        
    lines.append("}\n")
    
    path.write_text("".join(lines), encoding="utf-8")
    
if __name__ == "__main__":
    sorted_airports()