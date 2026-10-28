import pandas as pd
from utils.analysis import get_movie_summary

def popularity_recommendations(movies: pd.DataFrame, minimum_ratings: int = 3) -> pd.DataFrame:
    """Rank movies by average rating; require a minimum number of ratings."""
    return get_movie_summary(movies, minimum_ratings)

def similar_genre_recommendations(movies: pd.DataFrame, genre: str,
                                  minimum_ratings: int = 3) -> pd.DataFrame:
    if movies.empty:
        return movies.copy()
    selected = movies[movies["genre"].fillna("").str.casefold() == genre.casefold()].copy()
    return get_movie_summary(selected, minimum_ratings)
