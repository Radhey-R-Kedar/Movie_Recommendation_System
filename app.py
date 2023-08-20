import streamlit as st
import pickle
import pandas as pd
import requests


movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values
movies = pd.DataFrame(movies_list,columns=['title'])

n=10;
similarity = pickle.load(open('similarity.pkl','rb'))


def fetch_poster(movies_name):
    response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=bfe8a7fb6704d91f746ebc0bef00456d&query={}'.format(movies_name))
    data = response.json()
    url = "https://image.tmdb.org/t/p/original" + data['results'][0]['poster_path']
    return url
    
def recommend(movie):
    movie_index = movies[movies['title']== movie ].index[0]
    distance = similarity[movie_index]
    recommended_list = sorted(enumerate(distance), reverse=True, key = lambda x: x[1])[1:(n+1)]
    
    recommended_movie_list = []
    recommended_movie_posters = []
    
    for i in recommended_list:
        recommended_movie_list.append(movies.iloc[i[0]].title)
        
    for i in recommended_movie_list:
        recommended_movie_posters.append(fetch_poster(i))
        
    return recommended_movie_list,recommended_movie_posters


st.title('Movie recommender System')

selected_movie_name = st.selectbox(
    'Movies',
    (movies_list)
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    
    columns = st.columns(5)
    
    for i in range(0,5):
        with columns[i % 5]:  # Use modulo to loop back to the first column
            st.text(names[i])
            st.image(posters[i])
            
    for i in range(5,10):
        with columns[i % 5]:  # Use modulo to loop back to the first column
            st.text(names[i])
            st.image(posters[i])
    
    # col1, col2, col3, col4, col5 = st.columns(5)
    
    # with col1:
    #     st.text(names[0])
    #     st.image(posters[0])
    
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1])

    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2])

    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])


    