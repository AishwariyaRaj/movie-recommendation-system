import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
            movie_id))
    data = response.json()

    # Check if there is a poster path in the response
    if data['poster_path']:
        return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return None  # Return None if there's no poster


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster)
    return recommended_movies, recommended_movies_posters


# Loading the pickled movie data
movies_list_dict = pickle.load(open("C:\\Users\\ASUS\\artificats\\movie_list.pkl", 'rb'))
movies = pd.DataFrame(movies_list_dict)
similarity = pickle.load(open("C:\\Users\\ASUS\\artificats\\similarity.pkl", 'rb'))

# Streamlit UI
st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie to get recommendations:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Create columns dynamically using `st.columns` instead of `st.beta_columns`
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(names[i])
        if posters[i]:
            col.image(posters[i])
        else:
            col.text("No poster available")