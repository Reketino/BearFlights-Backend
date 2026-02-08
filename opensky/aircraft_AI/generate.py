
from google.genai import types
from .client import client
from .prompt import aircraft_prompt

def aircraft_generated_description(icao: str) -> str:
    response: types.GenerateContentResponse = client.models.generate_content( # type: ignore
        model="gemini-1.5-flash",
        contents=aircraft_prompt(icao)   
    )
    if not response.text: 
        raise RuntimeError("Zero response from from Gemini")
    
    
    return response.text.strip()