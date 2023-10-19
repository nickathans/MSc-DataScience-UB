import streamlit as st
import requests
import pandas as pd
import os
import urllib
from streamlit_lottie import st_lottie
from src.models.recommender import get_recommendations

st.set_page_config(page_title="Your Movie Recomender", page_icon=":cinema:",layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:  # if request is successful the code should be 200
        return None
    return r.json()


lottie_animation = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_xcyjeP.json")
# HEADER
with st.container():
    st.subheader("Feed me some movies")
    st.write("Show me yours and I'll show you mine")
    url = "https://github.com/maciejkula/spotlight)"
    st.write("[More on how I work](%s)" % url)
    
@st.cache
def get_movies_data():
    #mnames = ['movie_id', 'title', 'genres']
    #df = pd.read_csv('movies.dat', sep='::', header=None, names=mnames,  engine='python', encoding='latin1')
    m_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url']
    movies = pd.read_csv('_test_data_ml-100k/u.item', sep='|', names=m_cols, usecols=range(5),
                     encoding='latin-1')
    return movies#.set_index("title")

@st.cache
def get_movie_ids(df,movies):
    ids = []
    for movie in movies:
        ids.append(df[df['title']==movie]['movie_id'].values[0])
    return ids

try:
    df = get_movies_data()
    movies = st.multiselect(
        "Choose movies", list(df['title']), ["Toy Story (1995)", "Babe (1995)"]
    )
    if not movies:
        st.error("Please select at least one movie.")
    else:
        if st.button('Get recommendations.'):
            with st.spinner("Looking for recommendations..."):
                movie_ids = get_movie_ids(df,movies)
                recommendations = get_recommendations(df,movie_ids)
                st.balloons()
                st.write(recommendations)

        #data = data.T.reset_index()
        #data = pd.melt(data, id_vars=["index"]).rename(
        #    columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        #)

except urllib.error.URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
    
with st.container():
    st.write("---")    #this actually builds a divider line
    left_column,right_column = st.columns(2)
    with left_column:
        st.header("What I do")
        st.write("##")
        st.write(
            """
            If you feed me some movies, chances are I'll give you some more to binge watch this weekend!
            Who really needs to do that linear algebra project anyways?
            """
            
            )
with right_column:
    st_lottie(lottie_animation, height=300, key="coding")