import pandas as pd

def get_movie_summary(movies: pd.DataFrame, minimum_ratings: int = 3) -> pd.DataFrame:
    if movies.empty:
        return movies.copy()
    result = movies[movies["rating_count"] >= minimum_ratings].copy()
    return result.sort_values(["average_rating", "rating_count"], ascending=[False, False])

def get_genre_summary(movies: pd.DataFrame) -> pd.DataFrame:
    rated = movies.dropna(subset=["average_rating"]).copy()
    if rated.empty:
        return pd.DataFrame(columns=["genre", "average_rating", "movie_count"])
    result = rated.groupby("genre", as_index=False).agg(
        average_rating=("average_rating", "mean"),
        movie_count=("movie_id", "count")
    )
    result["average_rating"] = result["average_rating"].round(2)
    return result.sort_values("average_rating", ascending=False)

def get_rating_distribution(ratings: pd.DataFrame) -> pd.DataFrame:
    if ratings.empty:
        return pd.DataFrame(columns=["rating", "count"])
    counts = ratings.groupby("rating").size().reindex([1, 2, 3, 4, 5], fill_value=0)
    return counts.rename("count").reset_index()
