![Python](https://img.shields.io/badge/Python-3.x-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
## Architecture
```mermaid
flowchart LR
  A[Open-Meteo API] -->|HTTP JSON| B[Extract]
  B --> C[data/raw/*.json]
  C --> D[Transform]
  D --> E[data/processed/*.parquet]
  E --> F[Quality Checks]
  F -->|UPSERT / Incremental| G[(PostgreSQL)]
  G --> H[Analytics / SQL Queries]
```
![CI](https://github.com/MariaMoradzadeh/weather-etl/actions/workflows/ci.yml/badge.svg)
# Weather ETL Pipeline (Open-Meteo → Parquet → PostgreSQL)

An end-to-end data engineering mini project:
- Extracts hourly weather data from the Open-Meteo API
- Stores raw JSON in data/raw/
- Transforms and writes Parquet to data/processed/
- Runs basic data quality checks
- Loads into PostgreSQL using UPSERT (idempotent)
- Supports incremental load (only new rows)

## Quickstart
1) Start PostgreSQL:
docker compose up -d

2) Create venv and install:
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

3) Run:
python -m src.run_pipeline

## Verify
docker compose exec db psql -U etl -d etldb -c "SELECT location_name, COUNT(*) FROM weather_hourly GROUP BY location_name ORDER BY location_name;"

## Results

Verified the pipeline loads **168 hourly rows per location** into PostgreSQL (Helsinki & Vaasa).

Query:
```sql
SELECT location_name, COUNT(*)
FROM weather_hourly
GROUP BY location_name
ORDER BY location_name;
## Results

Loaded **168 hourly rows per location** into PostgreSQL (Helsinki & Vaasa).

Example query:
```bash
docker compose exec db psql -U etl -d etldb -c "SELECT location_name, COUNT(*) FROM weather_hourly GROUP BY location_name ORDER BY location_name;"
 location_name | count
---------------+-------
 Helsinki      |   168
 Vaasa         |   168

```
![Results Screenshot](screenshots/results.jpeg)


## Issues
- Tracking: https://github.com/MariaMoradzadeh/weather-etl/issues/1
