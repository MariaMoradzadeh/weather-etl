import json
from pathlib import Path
from datetime import datetime, timezone
import requests
from .config import settings

RAW_DIR = Path("data/raw")


def extract() -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": settings.LAT,
        "longitude": settings.LON,
        "hourly": "temperature_2m,precipitation,windspeed_10m",
        "timezone": "UTC",
    }

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    payload = r.json()

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = RAW_DIR / f"openmeteo_{settings.LOCATION_NAME.lower()}_{ts}.json"
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return out_path
