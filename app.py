import pickle
import pandas as pd
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=b19aed9893064bd5b4ff4f33624db992&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Enhanced UI with Streamlit
st.set_page_config(page_title="Movie Magic: Your Personalized Recommendation Engine", page_icon="️")

st.title('Dive into the World of Cinema with Movie Magic')
st.subheader('Discover your next cinematic adventure with personalized recommendations!')

st.markdown("""
Ever felt overwhelmed by the sheer number of movies available?
Struggling to decide what to watch next?

Movie Magic is here to help! We'll use your movie preferences to suggest hidden gems and captivating classics that you're sure to love.
""")

movies = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movies = pd.DataFrame(movies)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Tell us, what movie has recently sparked your imagination?",
    movie_list,
    key="movie_selectbox"  # Streamlit optimization
)

if st.button('🪄 Unveil Your Movie Magic', key="recommend_button"):  # Streamlit optimization
    st.markdown("---")

    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
