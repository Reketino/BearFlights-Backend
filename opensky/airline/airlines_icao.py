
# Callsign of airline companies defined
AIRLINES_BY_REGION: dict[str, dict[str, str]] = {
    
    "Nordic": {
    "FIN": "Finnair",
    "ICE": "Icelandair",
    "NOZ": "Norwegian Air Shuttle",
    "SAS": "Scandinavian Airlines",
    "WIF": "Widerøe",
    },
    "Europe": {
    "EIN": "Aer Lingus",
    "AFR": "Air France",
    "BAW": "British Airways",
    "KLM": "KLM Royal Dutch Airlines",
    "DLH": "Lufthansa",
    "RYR": "Ryanair",
    "THY": "Turkish Airlines",
    "BTI": "airBaltic",
    "EZY": "easyJet",
    },
    "Middle East": {
    "UAE": "Emirates",
    "ETD": "Etihad Airways",
    "QTR": "Qatar Airways", 
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