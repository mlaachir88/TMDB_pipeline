import os
import requests
from dagster import asset
from dotenv import load_dotenv

# Charger la variable d’environnement
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


@asset
def fetch_popular_movies():
    """Récupère les films populaires sur plusieurs pages."""
    all_movies = []
    for page in range(1, 76):  # Ajuster le nombre de pages si besoin
        url = f"{BASE_URL}/movie/popular"
        params = {
            "api_key": API_KEY,
            "language": "fr-FR",
            "page": page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        all_movies.extend(data["results"])
    return all_movies


@asset(deps=[fetch_popular_movies])
def fetch_movie_details(fetch_popular_movies):
    """Récupère les détails complets de chaque film."""
    detailed_movies = []
    for movie in fetch_popular_movies:
        movie_id = movie["id"]
        url = f"{BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": API_KEY,
            "language": "fr-FR"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            detailed_movies.append(response.json())
    return detailed_movies


@asset(deps=[fetch_popular_movies])
def fetch_movie_reviews(fetch_popular_movies):
    """Récupère les avis utilisateurs pour chaque film."""
    movie_reviews = {}
    for movie in fetch_popular_movies:
        movie_id = movie["id"]
        url = f"{BASE_URL}/movie/{movie_id}/reviews"
        params = {
            "api_key": API_KEY,
            "language": "fr-FR"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            movie_reviews[movie_id] = response.json().get("results", [])
    return movie_reviews


@asset
def fetch_genres():
    """Récupère la liste des genres disponibles."""
    url = f"{BASE_URL}/genre/movie/list"
    params = {
        "api_key": API_KEY,
        "language": "fr-FR"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["genres"]



@asset
def fetch_now_playing_movies():
    """Récupère les films actuellement en salles."""
    all_movies = []
    for page in range(1, 4): 
        url = f"{BASE_URL}/movie/now_playing"
        params = {
            "api_key": API_KEY,
            "language": "fr-FR",
            "page": page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        all_movies.extend(response.json()["results"])
    return all_movies



@asset
def fetch_top_rated_movies():
    """Récupère les films les mieux notés."""
    all_movies = []
    for page in range(1, 4):
        url = f"{BASE_URL}/movie/top_rated"
        params = {
            "api_key": API_KEY,
            "language": "fr-FR",
            "page": page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        all_movies.extend(response.json()["results"])
    return all_movies
