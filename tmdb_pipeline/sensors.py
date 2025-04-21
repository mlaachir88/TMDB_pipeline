from dagster import sensor, RunRequest
import duckdb
import requests
import os

@sensor(job_name="clean_movies_job")
def new_movies_sensor():
    """Déclenche le nettoyage si de nouveaux films sont disponibles dans TMDB"""
    api_key = os.getenv("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1"

    try:
        response = requests.get(url)
        data = response.json()
        tmdb_ids = [movie["id"] for movie in data["results"]]

        con = duckdb.connect("tmdb_data.duckdb")
        existing_ids = con.sql("SELECT id FROM movies").fetchdf()["id"].tolist()

        # Si un nouveau film n'existe pas en base, déclenche un run
        if any(tmdb_id not in existing_ids for tmdb_id in tmdb_ids):
            return [RunRequest(run_key=None, run_config={})]

    except Exception as e:
        print("Erreur dans le sensor TMDB:", e)

    return []