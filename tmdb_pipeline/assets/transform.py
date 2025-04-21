import duckdb
import pandas as pd
from dagster import asset
import os

@asset
def clean_movies_data():
    """
    Nettoyage complet et sécurisé des films :
    - Lecture toujours fraîche de la table movies
    - Nettoyage des colonnes
    - Aucun filtre strict (on garde même les films sans budget/revenue)
    - Recréation sûre de la table clean_movies
    """
    db_path = "tmdb_data.duckdb"
    if not os.path.exists(db_path):
        raise FileNotFoundError(" La base DuckDB n'existe pas. L'asset movies doit être généré d'abord.")

    # Connexion à la base existante
    con = duckdb.connect(db_path)


    try:
        df = con.sql("SELECT * FROM movies").fetchdf()
    except Exception as e:
        raise RuntimeError(f" Impossible de lire la table 'movies' : {e}")


    if df.empty:
        raise ValueError(" La table 'movies' est vide. Veuillez materialiser les assets d'import d'abord.")


    keep_cols = [
        "id", "title", "overview", "release_date", "vote_average", "vote_count",
        "runtime", "genres", "budget", "revenue"
    ]
    df = df[[col for col in keep_cols if col in df.columns]]

    # Convertir la date
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year

    # Extraire les genres
    def extract_genres(genre_list):
        try:
            return [g["name"] for g in genre_list]
        except:
            return []

    df["genre_names"] = df["genres"].apply(extract_genres)
    df.drop(columns=["genres"], inplace=True)

    # Calculer le profit, même avec NaN
    df["profit"] = df["revenue"] - df["budget"]

    # Supprimer ancienne table pour éviter les doublons
    con.execute("DROP TABLE IF EXISTS clean_movies")

    # Sauvegarde propre
    con.execute("CREATE TABLE clean_movies AS SELECT * FROM df")
    con.close()

    return f" {len(df)} films enregistrés dans clean_movies (incluant les lignes avec NaN budget/revenue)"
