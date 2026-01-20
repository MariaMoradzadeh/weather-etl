-- KPI 1) Row count per location
SELECT location_name, COUNT(*) AS rows
FROM weather_hourly
GROUP BY location_name
ORDER BY location_name;

-- KPI 2) Time range covered per location
SELECT
  location_name,
  MIN(ts) AS first_ts,
  MAX(ts) AS last_ts
FROM weather_hourly
GROUP BY location_name
ORDER BY location_name;

-- KPI 3) Temperature summary per location
SELECT
  location_name,
  ROUND(AVG(temperature_c)::numeric, 2) AS avg_temp_c,
  MIN(temperature_c) AS min_temp_c,
  MAX(temperature_c) AS max_temp_c
FROM weather_hourly
GROUP BY location_name
ORDER BY location_name;

-- KPI 4) Precipitation hours (how many hours had precipitation > 0)
SELECT
  location_name,
  SUM(CASE WHEN precipitation_mm > 0 THEN 1 ELSE 0 END) AS precip_hours
FROM weather_hourly
GROUP BY location_name
ORDER BY location_name;

-- KPI 5) Wind speed summary per location
SELECT
  location_name,
  ROUND(AVG(windspeed_ms)::numeric, 2) AS avg_wind_ms,
  MAX(windspeed_ms) AS max_wind_ms
FROM weather_hourly
GROUP BY location_name
ORDER BY location_name;
