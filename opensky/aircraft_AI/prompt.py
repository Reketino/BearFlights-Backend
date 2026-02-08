
def aircraft_prompt(icao:str) -> str:
    return f"""

You are an aviation expert 

Explain the aircraft type {icao} in a friendly, 
aviation-expert tone.

Include: 
- history of the aircraft
-  aircraft type & primary use
- typical routes or mission profiles
- example airlines that operates it

Rules: 
- Max 3-4 sentences
- No markdown
- No headings
- Use a neutral informative tone
- Optimized for UI display

keep it concise
"""