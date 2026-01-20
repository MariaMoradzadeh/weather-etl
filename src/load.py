from pathlib import Path
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from .config import settings
from .logger import get_logger

log = get_logger()

def _conn():
    return psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
    )

def _get_last_ts(conn) -> object:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT MAX(ts) FROM weather_hourly WHERE location_name = %s;",
            (settings.LOCATION_NAME,)
        )
        return cur.fetchone()[0]

def load(processed_path: Path) -> int:
    df = pd.read_parquet(processed_path)

    with _conn() as conn:
        last_ts = _get_last_ts(conn)
        if last_ts is not None:
            before = len(df)
            df = df[df["ts"] > pd.Timestamp(last_ts)]
            log.info(f"Incremental filter: last_ts={last_ts} | kept {len(df)}/{before} rows")
        else:
            log.info("No existing rows found for this location. Full load.")

        if len(df) == 0:
            log.info("No new rows to load. Skipping insert.")
            return 0

        rows = list(df.itertuples(index=False, name=None))

        sql = """
        INSERT INTO weather_hourly
          (location_name, latitude, longitude, ts, temperature_c, precipitation_mm, windspeed_ms)
        VALUES %s
        ON CONFLICT (location_name, ts)
        DO UPDATE SET
          temperature_c = EXCLUDED.temperature_c,
          precipitation_mm = EXCLUDED.precipitation_mm,
          windspeed_ms = EXCLUDED.windspeed_ms;
        """

        with conn.cursor() as cur:
            execute_values(cur, sql, rows, page_size=1000)
        conn.commit()

    return len(rows)
