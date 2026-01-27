
AIRCRAFT_TYPES_BY_MANUFACTURER: dict[str, dict[str, str]] = {
    
    "Airbus": {
    "A388": "Airbus A380-800",
    "A320": "Airbus A320",
    "A333": "Airbus A330",
    "A332": "Airbus A330-200",
    "A321": "Airbus A321",
    "A340": "Airbus A340-200",
    "A342": "Airbus A340-200",
    "A400": "Airbus A400",
    "A21N": "Airbus A321neo",
    "A20N": "Airbus A320neo",
    "A359": "Airbus A350-900",
    "A35K": "Airbus A350-1000",
    "BCS3": "Airbus A220-300",
    "A319": "Airbus A319",
    },
     
    "Boeing": {
    "B789": "Boeing 787",
    "B788": "Boeing 787-8 Dreamliner",
    "B77L": "Boeing 777",
    "B77W": "Boeing 777-300ER",
    "B748": "Boeing 747-8",
    "B39M": "Boeing 737 MAX 9",
    "B38M": "Boeing 737 MAX 8",
    "B738": "Boeing 737-800",
    "C17": "Boeing C-17 Globemaster"
    },
    
    "Bombardier": {
    "GL7T": "Bombardier Global 7500",
    },
    
    "Beechcraft": {
     "BE20": "Beechcraft Super King Air",   
    },
    
    "Cessna": { 
    "C25A": "Cessna 525A CJ2",
    "C56X": "Cessna Citation Excel",
    },
    
    "De Havilland Canada": {
    "DH8D": "De Havilland Canada DHC-8-400",
    "DH8A": "De Havilland Canada Dash 8", 
    },
    
    "Embraer": {
    "E290": "Embraer E190-E2",
    "E55P": "Embraer Phenom 300",
    "E195": "Embraer 195",
    "E190": "Embraer 190",
    },
}


AIRCRAFT_TYPES: dict[str, str] = {
    code: name
    for group in AIRCRAFT_TYPES_BY_MANUFACTURER.values()
    for code, name in group.items()
}