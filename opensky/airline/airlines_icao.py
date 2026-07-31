#Callsign of airline companies defined
AIRLINES_BY_REGION: dict[str, dict[str, str]] = {

     "Canada": {
        "ACA": "Air Canada",
        "CGS": "Air-JPL",
        "CJT": "Cargojet Airways",
    },

     "Europe": {
        "EIN": "Aer Lingus",
        "AFR": "Air France",
        "BTI": "airBaltic",
        "BNJ": "ASL Group",
        "AAN": "Atmospherica Aviation",
        "BNO": "Babcock Scandinavian Airambulance",
        "BBB": "Blackbird Air Charter",
        "BAW": "British Airways",
        "CFG": "Condor Flugdienst",
        "EZY": "easyJet",
        "EJU": "easyjet Europe",
        "ENT": "Enter Air",
        "SVW": "Global Jet Luxembourg",
        "TCI": "IC Holding",
        "KLM": "KLM Royal Dutch Airlines",
        "DLH": "Lufthansa",
        "NJE": "NetJets Europe",
        "RYR": "Ryanair",
        "SKV": "Skyside Aviation",
        "SRN": "Sprint Air",
        "SWR": "Swiss International Air Lines",
        "TOM": "TUI Airways",
        "THY": "Turkish Airlines",
        "VJT": "VistaJet",
        "QGA": "Windrose Air Jetcharter",
        "WZZ": "Wizz Air",
        "WUK": "Wizz Air UK",
    },

     "Middle East": {
        "AIC": "Air India",
        "STT": "Alpha Star",
        "ELY": "El Al Israel Airlines",
        "UAE": "Emirates",
        "ETD": "Etihad Airways",
        "MFX": "My Freighter Airlines",
        "PIA": "Pakistan International Airlines",
        "QTR": "Qatar Airways",
        "RJA": "Royal Jordanian",
    },

     "Military / State": {
        "SVF": "Swedish Armed Forces",
        "RRR": "UK Royal Air Force",
        "RCH": "United States Air Force Air Mobility Command",
    },

     "Nordic": {
        "LED": "Blom Geomatics",
        "CFL": "Bromma Air Maintenance",
        "FIN": "Finnair",
        "ICE": "Icelandair",
        "NOZ": "Norwegian Air Shuttle",
        "NSZ": "Norwegian Air Sweden",
        "SAS": "Scandinavian Airlines",
        "ABF": "Scanwings",
        "VKG": "Sunclass Airlines",
        "WIF": "Widerøe",
    },

     "The United States of America": {
        "DAL": "Delta Air Lines, Inc",
        "FJO": "FlexJet",
        "UAL": "United Airlines",
    },

}


ICAO_AIRLINES: dict[str, str] = {
    code: name
    for group in AIRLINES_BY_REGION.values()
    for code, name in group.items()
}
