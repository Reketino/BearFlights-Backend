
# Callsign of airline companies defined
AIRLINES_BY_REGION: dict[str, dict[str, str]] = {
    
    "Nordic": {
    "SAS": "Scandinavian Airlines",
    "NOZ": "Norwegian Air Shuttle",
    "WIF": "Widerøe",
    "FIN": "Finnair",
    "ICE": "Icelandair",
    },
    "Europe": {
    "THY": "Turkish Airlines",
    "EZY": "easyJet",
    "BAW": "British Airways",
    "DLH": "Lufthansa",
    "KLM": "KLM Royal Dutch Airlines",
    "AFR": "Air France",
    "BTI": "airBaltic",
    "EIN": "Aer Lingus",
    "RYR": "Ryanair",
    },
    "Middle East": {
    "QTR": "Qatar Airways",
    "UAE": "Emirates", 
    "ETD": "Etihad Airways",   
    },
    "Military / State": {
    "RRR": "UK Royal Air Force",    
    } 
}

ICAO_AIRLINES: dict[str, str] = {
    code: name
    for group in AIRLINES_BY_REGION.values()
    for code, name in group.items()
}