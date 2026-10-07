from __future__ import annotations

import csv
import io
import os
import zipfile

import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

AIRCRAFT_DATABASE_URL = (
    "https://s3.opensky-network.org/"
    "data-samples/metadata/aircraftDatabase.zip"
)

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

def download_aircraft_database() -> bytes:
    print("Downloading Opensky aircraft database...")

    response = requests.get(
        AIRCRAFT_DATABASE_URL,
        timeout=60,
    )

    response.raise_for_status()

    print(
        f"Downloaded {len(response.content) / 1024 / 1024:.1f} MB"
    )

    return response.content

def read_aircraft_database(
    content: bytes,
) -> list[dict[str, str | None]]:
    print("Reading aircraftDatabase.csv...")
    
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        csv_name = next(
            (
                name
                for name in archive.namelist()
                if name.endswith("aircraftDatabase.csv")
            ),
            None,
        )
        
        if csv_name is None:
            raise RuntimeError(
                "Could not find aircraftDatabase.csv in ZIP archive what a shame."
            )
            
        with archive.open(csv_name) as file:
            text_file = io.TextIOWrapper(
                file,
                encoding="utf-8",
                errors="replace",
            )
            
            reader = csv.DictReader(text_file)
        
            rows: list[dict[str, str | None]] = []
        
            for raw_row in reader:
                row = {
                    key: (
                        value.strip()
                        if isinstance(value, str) and value.strip()
                        else None
                    )
                    for key, value in raw_row.items()
                }
            
                rows.append(row)
            
            print(f"CSV rows read: {len(rows)}")
    
            return rows

def build_registry_rows(
    rows: list[dict[str, str | None]],
) -> list[dict[str, str | None]]:
    registry_rows: list[dict[str, str | None]] = []
    
    for row in rows:
        icao24 = row.get("icao24")
        
        if not icao24:
            continue
        
        registry_rows.append(
            {
                "icao24": icao24.lower(),
                "registration": row.get("registration"),
                "typecode": row.get("typecode"),
                "manufacturer": row.get("manufacturername"),
                "model": row.get("model"),
                "owner": row.get("owner"),
            }
        )
    return registry_rows

def import_aircraft_database(
    registry_rows: list[dict[str, str | None]],
) -> None:
    print( 
        f"Imporing {len(registry_rows)} aircraft into "
        "aircraft_registry..."
    )
     
    batch_size = 500
    
    total_batches = (
        len(registry_rows) + batch_size - 1
    ) // batch_size
    
    imported = 0
    
    
    for start in range(0, len(updates), batch_size):
        batch = updates[start:start + batch_size]
        
        (
            supabase
            .table("aircraft_registry")
            .upsert(
                batch,
                on_conflict="icao24",
            )
            .execute()
        )
        
        print(
            f"Imported batch "
            f"{start + 1}-{start + len(batch)} "
            f"of {len(updates)}"
        )
        
    print("Aircraft database import completed.")

        
def main() -> None:
    content = download_aircraft_database()

    rows = read_aircraft_database(content)
    
    print(f"\nTotal rows: {len(rows)}")
    
    valid_icao24 = 0
    with_typecode = 0
    with_model = 0
    with_manufacturer = 0
    
    for row in rows:
        icao24 = row.get("icao24")
        typecode = row.get("typecode")
        model = row.get("model")
        manufacturer = row.get("manufacturername") 
         
        if icao24:
            valid_icao24 += 1
            
        if typecode:
            with_typecode += 1
            
        if model:
            with_model += 1
            
        if manufacturer:
            with_manufacturer += 1
            
    print(f"Valid ICAO24: {valid_icao24}")
    print(f"With typecode: {with_typecode}")
    print(f"With model: {with_model}")
    print(f"With manufacturer: {with_manufacturer}")
    
    registry_rows = build_registry_rows(rows)
    
    print(f"\nRegistry rows built: {len(registry_rows)}")
    
    import_aircraft_database(registry_rows)
            
if __name__ == "__main__":
    main()
    