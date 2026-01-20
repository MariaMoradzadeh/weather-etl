import json
from pathlib import Path
import pandas as pd
from .config import settings

PROCESSED_DIR = Path("data/processed")


def transform(raw_path: Path) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    payload = json.loads(raw_path.read_text(encoding="utf-8"))
    hourly = payload.get("hourly", {})
    times = hourly.get("time", [])

    df = pd.DataFrame(
        {
            "location_name": settings.LOCATION_NAME,
            "latitude": payload.get("latitude"),
            "longitude": payload.get("longitude"),
            "ts": pd.to_datetime(times, utc=True),
            "temperature_c": hourly.get("temperature_2m", []),
            "precipitation_mm": hourly.get("precipitation", []),
            "windspeed_ms": hourly.get("windspeed_10m", []),
        }
    )

    df = df.dropna(subset=["ts"]).drop_duplicates(subset=["location_name", "ts"])
    df.loc[
        (df["temperature_c"] < -60) | (df["temperature_c"] > 60), "temperature_c"
    ] = pd.NA
    df.loc[
        (df["precipitation_mm"] < 0) | (df["precipitation_mm"] > 300),
        "precipitation_mm",
    ] = pd.NA
    df.loc[(df["windspeed_ms"] < 0) | (df["windspeed_ms"] > 70), "windspeed_ms"] = pd.NA

    out_path = PROCESSED_DIR / (raw_path.stem + ".parquet")
    df.to_parquet(out_path, index=False)
    return out_path
