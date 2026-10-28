import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

# Load .env from the project root, regardless of the terminal's current folder.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

def get_connection():
    required = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing = [key for key in required if os.getenv(key) is None]
    if missing:
        raise RuntimeError(
            "Missing environment setting(s): " + ", ".join(missing) +
            ". Check the .env file in the same folder as app.py."
        )
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

def check_connection():
    try:
        connection = get_connection()
        connection.close()
        return True, "Connected"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"
