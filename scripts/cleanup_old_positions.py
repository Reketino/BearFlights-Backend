from datetime import datetime, timedelta, timezone
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supbase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"],
)

def cleanup_old_positions() -> None:
    print("Cleanup old positions process initiated...")
    
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    
    res = (
        supbase
        .table("flight_positions")
        .delete()
        .lt("last_seen", cutoff.isoformat())
        .execute()
    )
    
    print("Cleanup process completed.")
    print("Rows Removed:", len(res.data)or [])
    
    
if __name__ == "__main__":
    cleanup_old_positions()
    