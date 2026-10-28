# Movie Ratings Analysis and Basic Recommendation System

A beginner-friendly Python + Streamlit + MySQL project for managing movie ratings, analysing genres, and producing transparent recommendations.

## Features
- Movie catalogue and movie entry form
- User ratings from 1 to 5
- Average ratings and rating counts
- Top-rated movies with a configurable minimum rating count (default: 3)
- Genre average-rating chart and rating distribution chart
- Popularity-based and genre-based recommendations
- MySQL stores the data; Pandas performs aggregation; Streamlit displays the dashboard

Recommendations are educational suggestions based on the available ratings. They do not guarantee personal preference. The app does not display other users' private rating histories; the recent-ratings view shows movie and rating information without user IDs or names.

## Requirements
- Python 3.11+ recommended
- MySQL Server 8+
- VS Code (optional)

## Setup
1. Open MySQL Workbench and run `database/schema.sql`.
2. Optionally run `database/sample_data.sql` to insert demo movies, users, and ratings.
3. Copy `.env.example` to `.env` in the project root.
4. Edit `.env` and set your actual MySQL username and password. Never commit `.env`.
5. Open a terminal in this project folder.
6. Create and activate a virtual environment:

   Windows PowerShell:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

7. Install packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```

8. Run:
   ```powershell
   python -m streamlit run app.py
   ```
9. Open the local address printed in the terminal, usually `http://localhost:8501`.

## MySQL troubleshooting
- Error 1045 / `using password: NO`: ensure `.env` is beside `app.py`, `DB_PASSWORD` has a value, and the app was restarted after editing it.
- Access denied with password: verify the password and MySQL account permissions in MySQL Workbench.
- Unknown database: run `database/schema.sql`.
- Can't connect to server: start the MySQL80 service from Windows Services or open MySQL Workbench and confirm the server is running.

## GitHub
1. Create a new empty repository on GitHub. Do not add a README there if this folder already has one.
2. In this folder, run:
   ```powershell
   git init
   git add .
   git status
   git commit -m "Initial movie recommendation system"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/movie-recommendation-system.git
   git push -u origin main
   ```
3. Replace the remote URL with your repository URL. If Git asks you to sign in, complete the browser authentication.

Before committing, confirm `.env` is not listed by `git status`. Never push database passwords or real users' private data.
