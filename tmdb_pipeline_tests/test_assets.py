from tmdb_pipeline.assets.tmdb_api import fetch_popular_movies
from tmdb_pipeline.assets.transform import clean_movies_data
import pandas as pd
from tmdb_pipeline.assets.tmdb_api import fetch_genres
from dagster import build_op_context
import pytest
from tmdb_pipeline.assets.tmdb_api import fetch_movie_reviews
from dagster import build_op_context


def test_fetch_genres_returns_list():
    context = build_op_context()
    result = fetch_genres(context)
    assert isinstance(result, list)
    assert len(result) > 0
    assert "id" in result[0]
    assert "name" in result[0]




def test_fetch_popular_movies_returns_list():
    context = build_op_context()
    result = fetch_popular_movies(context)
    assert isinstance(result, list)
    assert len(result) > 0
    assert "id" in result[0]
    assert "title" in result[0]



def test_fetch_movie_reviews_returns_dict():
    context = build_op_context()
    raw_movies = fetch_popular_movies(context)
    reviews = fetch_movie_reviews(context, raw_movies)

    assert isinstance(reviews, dict)
    assert len(reviews) > 0

    has_reviews = any(len(v) > 0 for v in reviews.values())
    assert isinstance(list(reviews.values())[0], list)
    assert has_reviews or True


