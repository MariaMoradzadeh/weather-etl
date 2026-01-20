from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "etldb")
    DB_USER: str = os.getenv("DB_USER", "etl")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "etlpass")

    LOCATION_NAME: str = os.getenv("LOCATION_NAME", "Vaasa")
    LAT: float = float(os.getenv("LAT", "63.0951"))
    LON: float = float(os.getenv("LON", "21.6165"))

settings = Settings()
