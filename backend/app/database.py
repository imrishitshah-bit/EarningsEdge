import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

# ------------------------------------
# Load .env locally (if it exists)
# ------------------------------------

env_path = Path(__file__).resolve().parents[2] / ".env"

if env_path.exists():
    load_dotenv(env_path)

# ------------------------------------
# Environment Variables
# ------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing.")

if not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_SERVICE_ROLE_KEY is missing.")

# ------------------------------------
# Supabase Client
# ------------------------------------

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)