import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.db import get_connection, check_connection
from utils.analysis import get_movie_summary, get_genre_summary, get_rating_distribution
from utils.recommendations import popularity_recommendations, similar_genre_recommendations

st.set_page_config(page_title="Movie Ratings & Recommendations", page_icon="🎬", layout="wide")
st.title("🎬 Movie Ratings Analysis and Recommendation System")
st.caption("Explore ratings, compare genres, and discover movies using simple, explainable rules.")

connected, connection_message = check_connection()
if not connected:
    st.error("MySQL connection failed.")
    st.code(connection_message)
    st.markdown("""
    **Check these items:**
    1. MySQL Server is running.
    2. `.env` is beside `app.py`.
    3. `DB_USER`, `DB_PASSWORD`, and `DB_NAME` in `.env` are correct.
    4. Run `database/schema.sql` in MySQL Workbench to create the database and tables.
    """)
    st.stop()

conn = get_connection()
try:
    movies = pd.read_sql("""
        SELECT m.movie_id, m.title, m.release_year, m.genre,
               ROUND(AVG(r.rating), 2) AS average_rating,
               COUNT(r.rating_id) AS rating_count
        FROM movies m
        LEFT JOIN ratings r ON m.movie_id = r.movie_id
        GROUP BY m.movie_id, m.title, m.release_year, m.genre
        ORDER BY m.title
    """, conn)
    ratings = pd.read_sql("""
        SELECT r.rating_id, r.user_id, r.movie_id, r.rating, r.rated_at,
               m.title, m.genre
        FROM ratings r JOIN movies m ON m.movie_id = r.movie_id
        ORDER BY r.rated_at DESC, r.rating_id DESC
    """, conn)
    users = pd.read_sql("SELECT user_id, display_name FROM users ORDER BY user_id", conn)
finally:
    conn.close()

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Movies", "Rate a Movie", "Recommendations"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Movies", len(movies))
    c2.metric("Ratings", len(ratings))
    avg = ratings["rating"].mean() if not ratings.empty else 0
    c3.metric("Overall average", f"{avg:.2f}/5" if not ratings.empty else "No ratings yet")

    st.subheader("Top-rated movies")
    min_count = st.number_input("Minimum number of ratings", min_value=1, max_value=100, value=3, step=1,
                                help="A movie must have at least this many ratings to appear in the top-rated list.")
    summary = get_movie_summary(movies, min_count)
    if summary.empty:
        st.info("Not enough movies meet the selected minimum rating count. Add ratings or lower the threshold.")
    else:
        st.dataframe(summary[["title", "release_year", "genre", "average_rating", "rating_count"]],
                     use_container_width=True, hide_index=True)

    st.subheader("Average rating by genre")
    genre_summary = get_genre_summary(movies)
    if genre_summary.empty:
        st.info("Genre analysis will appear after movies have ratings.")
    else:
        st.bar_chart(genre_summary.set_index("genre")["average_rating"])
        st.dataframe(genre_summary, use_container_width=True, hide_index=True)

    st.subheader("Rating distribution")
    distribution = get_rating_distribution(ratings)
    if not distribution.empty:
        st.bar_chart(distribution.set_index("rating")["count"])
    else:
        st.info("No ratings available to chart yet.")

with tab2:
    st.subheader("Movie catalogue")
    st.dataframe(movies[["movie_id", "title", "release_year", "genre", "average_rating", "rating_count"]],
                 use_container_width=True, hide_index=True)
    with st.expander("Add a movie"):
        with st.form("add_movie_form"):
            title = st.text_input("Movie title")
            year = st.number_input("Release year", min_value=1888, max_value=2100, value=2024)
            genre = st.selectbox("Genre", ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama",
                                           "Fantasy", "Horror", "Romance", "Sci-Fi", "Thriller", "Other"])
            submitted = st.form_submit_button("Add movie")
        if submitted:
            if not title.strip():
                st.warning("Enter a movie title.")
            else:
                add_conn = get_connection()
                try:
                    with add_conn.cursor() as cur:
                        cur.execute("INSERT INTO movies (title, release_year, genre) VALUES (%s, %s, %s)",
                                    (title.strip(), int(year), genre))
                    add_conn.commit()
                    st.success("Movie added. Refresh the page to see it.")
                    st.rerun()
                except Exception as exc:
                    add_conn.rollback()
                    st.error(f"Could not add movie: {exc}")
                finally:
                    add_conn.close()

with tab3:
    st.subheader("Submit a rating")
    if movies.empty or users.empty:
        st.info("Add at least one movie and one user in MySQL before rating.")
    else:
        with st.form("rating_form"):
            user_options = {f"{row.display_name} (ID {row.user_id})": int(row.user_id)
                            for row in users.itertuples()}
            movie_options = {f"{row.title} (ID {row.movie_id})": int(row.movie_id)
                             for row in movies.itertuples()}
            selected_user = st.selectbox("User", list(user_options.keys()))
            selected_movie = st.selectbox("Movie", list(movie_options.keys()))
            rating_value = st.slider("Rating", min_value=1, max_value=5, value=4, step=1)
            rating_submit = st.form_submit_button("Save rating")
        if rating_submit:
            rate_conn = get_connection()
            try:
                with rate_conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)",
                        (user_options[selected_user], movie_options[selected_movie], rating_value)
                    )
                rate_conn.commit()
                st.success("Rating saved.")
                st.rerun()
            except Exception as exc:
                rate_conn.rollback()
                st.error(f"Could not save rating: {exc}")
            finally:
                rate_conn.close()
    st.subheader("Recent ratings")
    if ratings.empty:
        st.info("No ratings have been submitted yet.")
    else:
        st.dataframe(ratings[["title", "genre", "rating", "rated_at"]],
                     use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Popularity-based recommendations")
    st.write("Movies are ranked by average rating, with a minimum-rating-count rule to reduce the effect of one-off ratings.")
    rec_min = st.number_input("Minimum ratings for recommendations", min_value=1, max_value=100,
                              value=3, step=1, key="rec_min")
    recs = popularity_recommendations(movies, int(rec_min))
    if recs.empty:
        st.info("No movies meet this minimum rating count yet. Try a lower value or add more ratings.")
    else:
        st.dataframe(recs[["title", "release_year", "genre", "average_rating", "rating_count"]],
                     use_container_width=True, hide_index=True)

    st.subheader("Genre-based suggestions")
    available_genres = sorted(movies["genre"].dropna().unique().tolist()) if not movies.empty else []
    if available_genres:
        chosen_genre = st.selectbox("Choose a genre", available_genres)
        similar = similar_genre_recommendations(movies, chosen_genre, int(rec_min))
        if similar.empty:
            st.info("No rated movies are available for this genre at the selected threshold.")
        else:
            st.dataframe(similar[["title", "release_year", "genre", "average_rating", "rating_count"]],
                         use_container_width=True, hide_index=True)
    st.caption("Recommendations are educational, based on available ratings and transparent ranking rules. They do not guarantee personal preference.")
