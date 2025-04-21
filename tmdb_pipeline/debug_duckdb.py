import duckdb
con = duckdb.connect("tmdb_data.duckdb")

# Vérifier les valeurs manquantes
print(" Valeurs manquantes :")
print(con.sql("""
SELECT
    COUNT(*) FILTER (WHERE title IS NULL) AS missing_title,
    COUNT(*) FILTER (WHERE release_date IS NULL) AS missing_date,
    COUNT(*) FILTER (WHERE vote_average IS NULL) AS missing_vote,
    COUNT(*) FILTER (WHERE runtime IS NULL) AS missing_runtime,
    COUNT(*) FILTER (WHERE genre_names IS NULL OR array_length(genre_names) = 0) AS missing_genres
FROM clean_movies
""").fetchdf())

# Statistiques de base sur vote_average et profit
print("\n Statistiques :")
print(con.sql("""
SELECT
    MIN(vote_average) AS min_vote,
    MAX(vote_average) AS max_vote,
    AVG(vote_average) AS avg_vote,
    MIN(profit) AS min_profit,
    MAX(profit) AS max_profit,
    AVG(profit) AS avg_profit
FROM clean_movies
""").fetchdf())
