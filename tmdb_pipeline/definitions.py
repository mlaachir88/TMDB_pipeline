from dagster import Definitions, load_assets_from_modules
from tmdb_pipeline.assets import tmdb_api, store_to_duckdb, transform
from tmdb_pipeline.schedules import daily_clean_schedule
from tmdb_pipeline.sensors import new_movies_sensor

all_assets = load_assets_from_modules([
    tmdb_api,
    store_to_duckdb,
    transform
])

defs = Definitions(
    assets=all_assets,
    schedules=[daily_clean_schedule],
    sensors=[new_movies_sensor]
)
