from pathlib import Path
import pandas as pd

def run_quality_checks(processed_path: Path) -> None:
    df = pd.read_parquet(processed_path)

    required = ["location_name", "latitude", "longitude", "ts"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df["ts"].isna().any():
        raise ValueError("Null timestamps found")

    if df.duplicated(subset=["location_name", "ts"]).any():
        raise ValueError("Duplicate (location_name, ts) found")

    if len(df) == 0:
        raise ValueError("Dataset is empty after transform")
