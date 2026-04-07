AIRCRAFT_TYPES_BY_MANUFACTURER: dict[str, dict[str, str]] = {
    "Aeroprakt": {
        "AP32": "Aeroprakt A-32",
    },

    "Airbus": {
        "BCS3": "Airbus A220-300",
        "A319": "Airbus A319",
        "A320": "Airbus A320",
        "A20N": "Airbus A320neo",
        "A321": "Airbus A321",
        "A21N": "Airbus A321neo",
        "A333": "Airbus A330",
        "A332": "Airbus A330-200",
        "A342": "Airbus A340-200",
        "A340": "Airbus A340-300",
        "A35K": "Airbus A350-1000",
        "A359": "Airbus A350-900",
        "A388": "Airbus A380-800",
        "A400": "Airbus A400",
    },

    "Beechcraft": {
        "BE20": "Beechcraft Super King Air",
    },

    "Boeing": {
        "B38M": "Boeing 737 MAX 8",
        "B39M": "Boeing 737 MAX 9",
        "B738": "Boeing 737-800",
        "B748": "Boeing 747-8",
        "B752": "Boeing 757-200",
        "B762": "Boeing 767-200",
        "B763": "Boeing 767-300",
        "B77L": "Boeing 777",
        "B77W": "Boeing 777-300ER",
        "B789": "Boeing 787",
        "B788": "Boeing 787-8 Dreamliner",
        "C17": "Boeing C-17 Globemaster",
    },

    "Bombardier": {
        "CRJ9": "Bombardier CRJ900",
        "GL7T": "Bombardier Global 7500",
    },

    "Cessna": {
        "C177": "Cessna 177 Cardinal",
        "C25A": "Cessna 525A CJ2",
        "C56X": "Cessna Citation Excel",
        "C68A": "Cessna Citation Latitude",
    },

    "De Havilland Canada": {
        "DH8D": "De Havilland Canada DHC-8-400",
        "DH8A": "De Havilland Canada Dash 8",
    },

    "Embraer": {
        "E190": "Embraer 190",
        "E195": "Embraer 195",
        "E75L": "Embraer E175",
        "E290": "Embraer E190-E2",
        "E55P": "Embraer Phenom 300",
    },

    "Learjet": {
        "LJ45": "Learjet 45",
    },

    "Lockheed Martin": {
        "C30J": "Lockheed Martin C-130J Super Hercules",
    },

    "SAAB": {
        "SF34": "Saab 340A",
    },

    "Van's Aircraft": {
        "RV14": "Van's Aircraft RV-14",
    },

}

AIRCRAFT_TYPES: dict[str, str] = {
    code: name
    for group in AIRCRAFT_TYPES_BY_MANUFACTURER.values()
    for code, name in group.items()
}
