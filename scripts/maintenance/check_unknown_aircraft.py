from __future__ import annotations

import os
from typing import Any, cast

from dotenv import load_dotenv
from supabase import create_client

from opensky.aircraft.aircraft import AIRCRAFT_TYPES

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

def main() -> None:
    res = (
        supabase
        .table("aircraft_registry")
        .select("typecode, manufacturer, model")
        .execute()
    )
    
    rows = cast(list[dict[str, Any]], res.data or [])
    
    unknown: dict[str, tuple[str | None, str |None]] = {}
    
    for row in rows:
        typecode = row.get("typecode")
        manufacturer = row.get("manufacturer")
        model = row.get("model")
        
        if not isinstance(typecode, str):
            continue
        
        typecode = typecode.strip()
        
        if not typecode:
            continue
        
        if typecode in AIRCRAFT_TYPES:
            continue
        
        unknown[typecode] = (
            manufacturer if isinstance(manufacturer, str) else None,
            model if isinstance(model, str) else None,
        )
        
        if not unknown:
            print("Zero unknown aircraft types.")
            
        
        print("\nUnkown airrcraft types\n")
        print("-" * 80)
        
        for typecode in sorted(unknown):
            manufacturer, model = unknown[typecode]
            
            print(
                f"{typecode:<8}"
                f"{manufacturer or '-':<25}"
                f"{model or '-'}"
            )
            
        print("-" * 80)
        print(f"Total: {len(unknown)}")
        
if __name__ == "__main__":
    main() 
    