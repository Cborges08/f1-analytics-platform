import os
from dotenv import load_dotenv

load_dotenv()

# API endpoints
OPENF1_BASE_URL = os.getenv("OPENF1_BASE_URL", "https://api.openf1.org/v1")
ERGAST_BASE_URL = os.getenv("ERGAST_BASE_URL", "https://ergast.com/api/f1")

# Database
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "database": os.getenv("POSTGRES_DB", "f1_analytics"),
    "user": os.getenv("POSTGRES_USER", "f1_user"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
}

DATABASE_URL = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)