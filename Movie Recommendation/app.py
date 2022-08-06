import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommendations = sorted(list(enumerate(distances)), reverse=True, key = lambda x: x[1])

    L = []
    P = []
    for recommendation in recommendations[1:6]:
        movie_id = movies.iloc[recommendation[0]].id
        L.append(movies.iloc[recommendation[0]].title)
        P.append(fetch_poster(movie_id))

    return L, P


st.markdown("<h1 style='text-align: center'>Movie Recommendation System</h1>", unsafe_allow_html=True)

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values

choice = st.selectbox("Pick a Movie", movie_list)

if st.button("Recommend"):
    recommended_movies, posters = recommend(choice)
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        st.image(posters[0], width=200, caption=recommended_movies[0])
    with col2:
        st.image(posters[1], width=200, caption=recommended_movies[1])
    with col3:
        st.image(posters[2], width=200, caption=recommended_movies[2])