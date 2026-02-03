def aircraft_prompt(icao:str) -> str:
    return f"""
Explain the aircraft type {icao} in a friendly, 
aviation-expert tone.

Include: 
- history of the aircraft
- what it is used for
- typical routes it flies
- which airlines that use it

keep it concise
"""