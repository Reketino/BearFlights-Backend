from .client import client
from prompt import aircraft_prompt

def aircraft_generated_description(icao: str) -> str:
    response = client.responses.create(
        model="chatgpt-4o-latest",
        input= aircraft_prompt(icao)
    )
    return response.output_text.strip()