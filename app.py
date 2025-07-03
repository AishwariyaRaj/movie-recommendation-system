import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "your_omdb_api_key_here")
PLACEHOLDER_IMAGE_URL = "https://via.placeholder.com/300x450?text=No+Poster"

# Genre to emoji/icon mapping
GENRE_ICONS = {
    'Action': '🔫',
    'Adventure': '🧭',
    'Animation': '🎬',
    'Biography': '👤',
    'Comedy': '😂',
    'Crime': '🕵️',
    'Drama': '🎭',
    'Family': '👨‍👩‍👧',
    'Fantasy': '🧙',
    'History': '📜',
    'Horror': '👻',
    'Music': '🎵',
    'Mystery': '🕵️‍♂️',
    'Romance': '❤️',
    'Sci-Fi': '👽',
    'Thriller': '🔪',
    'War': '⚔️',
    'Western': '🤠',
}

# Load movie data
movies = pd.read_csv("movies.csv")

# Helper to fetch poster from OMDb
@st.cache_data(show_spinner=False)
def fetch_poster(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]
        else:
            return PLACEHOLDER_IMAGE_URL
    except Exception:
        return PLACEHOLDER_IMAGE_URL

# Get all unique genres
all_genres = set()
for genres in movies["genres"]:
    for genre in genres.split("|"):
        all_genres.add(genre.strip())
all_genres = sorted(list(all_genres))

# --- Custom CSS for modern look (light mode only) ---
st.markdown(f"""
    <style>
    body {{
        background: #f7f7f7;
        color: #22223b;
    }}
    .main-header {{
        text-align: center;
        color: #22223b;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.2em;
        letter-spacing: 1px;
    }}
    .subtitle {{
        text-align: center;
        color: #4a4e69;
        font-size: 1.2rem;
        margin-bottom: 1.5em;
    }}
    .accent-bar {{
        height: 5px;
        background: linear-gradient(90deg, #9f86c0 0%, #5e60ce 100%);
        border-radius: 3px;
        margin-bottom: 2em;
    }}
    .movie-card {{
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(100, 100, 150, 0.08);
        padding: 1em 0.5em 0.7em 0.5em;
        margin-bottom: 0.5em;
        transition: box-shadow 0.2s;
        text-align: center;
        border: 1px solid #eee;
    }}
    .movie-card:hover {{
        box-shadow: 0 4px 24px rgba(94, 96, 206, 0.18);
    }}
    .movie-title {{
        font-weight: 700;
        font-size: 1.1rem;
        color: #22223b;
        margin-top: 0.7em;
        margin-bottom: 0.2em;
    }}
    .movie-year {{
        color: #4a4e69;
        font-size: 0.95rem;
        margin-bottom: 0.2em;
    }}
    .genre-icons {{
        font-size: 1.2rem;
        margin-bottom: 0.3em;
    }}
    .footer {{
        text-align: center;
        color: #888;
        font-size: 0.95rem;
        margin-top: 2em;
        margin-bottom: 0.5em;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'><b>Movie Recommender System</b></div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Discover movies by genre. Enjoy posters and a modern look!</div>", unsafe_allow_html=True)
st.markdown("<div class='accent-bar'></div>", unsafe_allow_html=True)

# Genre select with icons
genre_options = [f"{GENRE_ICONS.get(g, '')} {g}" for g in all_genres]
genre_map = dict(zip(genre_options, all_genres))
selected_genre_label = st.selectbox("Choose a genre:", genre_options)
selected_genre = genre_map[selected_genre_label]

# Recommend movies from selected genre
genre_movies = movies[movies["genres"].str.contains(selected_genre, case=False)]

st.markdown(f"<h3 style='margin-bottom:1.5em;'>Top {min(12, len(genre_movies))} {selected_genre} Movies:</h3>", unsafe_allow_html=True)

# Responsive grid: 4 columns on desktop, 2 on mobile/tablet
display_count = min(12, len(genre_movies))
num_cols = min(4, display_count)
rows = (display_count + num_cols - 1) // num_cols  # Ceiling division

movie_list = list(genre_movies.head(display_count).iterrows())
for row_idx in range(rows):
    cols = st.columns(num_cols)
    for col_idx in range(num_cols):
        movie_idx = row_idx * num_cols + col_idx
        if movie_idx < display_count:
            _, row = movie_list[movie_idx]
            with cols[col_idx]:
                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                st.image(fetch_poster(row['title']), width=160)
                # Show genre icons for this movie
                movie_genres = [g.strip() for g in row['genres'].split('|')]
                icons = ' '.join([GENRE_ICONS.get(g, '') for g in movie_genres if g in GENRE_ICONS])
                st.markdown(f"<div class='genre-icons'>{icons}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='movie-title'><b>{row['title']}</b></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='movie-year'><b>{row['year']}</b></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<div class='footer'>Made with ❤️ using Streamlit | Movie data: OMDb API & sample dataset</div>", unsafe_allow_html=True)