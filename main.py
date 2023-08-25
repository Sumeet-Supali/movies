import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US%27'.format(movie_id))
    data = response.json()
    #st.text(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

#reco fun
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    top_movies = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]


    reco = []
    for i in top_movies:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies['title'].iloc[i[0]]
        poster_url = fetch_poster(movie_id)
        reco.append({'title': title, 'poster_url': poster_url})

    return reco


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(stop_words = 'english', max_features=5000)
vectors = cv.fit_transform(movies['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

st.title("MOVIE RECOMMENDER SYSTEM")
selected_movie_name = st.selectbox('Search', movies['title'].values)

if st.button('recommend'):
    reco = recommend(selected_movie_name)

    num_columns = 5
    col_list = st.columns(num_columns)

    for i, col in enumerate(col_list):
        if i < len(reco):
            col.write(reco[i]['title'])
            col.image(reco[i]['poster_url'])

