from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supbase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPBASE_SERVICE_ROLE_KEY"],
)

def cleanup_old_positions() -> None:
    print("Cleanup old positions process initiated...")
    
    res = (
        supbase
        .table("flight_positions")
        .delete()
        .lt("last_seen", "now() - interval '7 days'")
        .execute()
    )
    
    print("Cleanup process completed.")
    