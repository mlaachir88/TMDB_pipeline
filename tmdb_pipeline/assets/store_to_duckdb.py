import duckdb
import pandas as pd
from dagster import asset
from tmdb_pipeline.assets.tmdb_api import fetch_movie_details

@asset(deps=[fetch_movie_details])
def save_movies_to_duckdb(fetch_movie_details):
    """Sauvegarde des films détaillés dans DuckDB."""
    df = pd.json_normalize(fetch_movie_details)

    # Création / connexion à la base locale DuckDB
    conn = duckdb.connect("tmdb_data.duckdb")
    conn.execute("CREATE OR REPLACE TABLE movies AS SELECT * FROM df")
    conn.close()

    return f"{len(df)} films enregistrés dans tmdb_data.duckdb"
