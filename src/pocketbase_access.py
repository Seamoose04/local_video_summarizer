from pocketbase import PocketBase

import os, subprocess
from dotenv import load_dotenv

PB_FOLDER = "pocketbase"

# Load environment variables from .env
load_dotenv()
POCKETBASE_URL = os.getenv("POCKETBASE_URL", "http://localhost/8090")
PB_ADMIN_EMAIL = os.getenv("PB_ADMIN_EMAIL", "")
PB_ADMIN_PASSWORD = os.getenv("PB_ADMIN_PASSWORD", "")

# Start and connect
subprocess.run([f"{PB_FOLDER}/pocketbase.exe"])

client = PocketBase(f"POCKETBASE_URL")
client.admins.auth_with_password("PB_ADMIN_EMAIL", "PB_ADMIN_PASSWORD")