#Callsign of airline companies defined
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
        "EJU": "Easyjet Europe",
        "ENT": "Enter Air",
        "KLM": "KLM Royal Dutch Airlines",
        "DLH": "Lufthansa",
        "RYR": "Ryanair",
        "SRN": "Sprint Air",
        "TOM": "TUI Airways",
        "THY": "Turkish Airlines",
        "BTI": "airBaltic",
        "EZY": "easyJet",
    },

     "Middle East": {
        "AIC": "Air India",
        "HZ": "Alpha Star",
        "UAE": "Emirates",
        "ETD": "Etihad Airways",
        "QTR": "Qatar Airways",
        "RJA": "Royal Jordanian",
    },

     "Military / State": {
        "RRR": "UK Royal Air Force",
    },

}


ICAO_AIRLINES: dict[str, str] = {
    code: name
    for group in AIRLINES_BY_REGION.values()
    for code, name in group.items()
}
