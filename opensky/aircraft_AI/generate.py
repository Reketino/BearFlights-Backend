from .client import client
from .prompt import aircraft_prompt

def aircraft_generated_description(icao: str) -> str:
    response = client.responses.generate_content(
        model="gemini-1.5 flash",
        input= aircraft_prompt(icao),
    )
    if not response.text: 
        raise RuntimeError("Zero response from from Gemini")
    
    return response.text.strip()