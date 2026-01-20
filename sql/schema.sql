CREATE TABLE IF NOT EXISTS weather_hourly (
  id BIGSERIAL PRIMARY KEY,
  location_name TEXT NOT NULL,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL,
  ts TIMESTAMPTZ NOT NULL,
  temperature_c DOUBLE PRECISION,
  windspeed_ms DOUBLE PRECISION,
  precipitation_mm DOUBLE PRECISION,
  load_date DATE NOT NULL DEFAULT CURRENT_DATE,
  UNIQUE (location_name, ts)
);

CREATE INDEX IF NOT EXISTS idx_weather_hourly_ts ON weather_hourly(ts);
