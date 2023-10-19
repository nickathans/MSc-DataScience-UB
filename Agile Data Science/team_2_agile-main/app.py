import streamlit as st
import requests
import pandas as pd
import os
import time
import urllib
from streamlit_lottie import st_lottie
from src.models.sequential_recommender import get_recommendations
from src.models.explicit_recommender import get_user_recommendations
from skimage.io import imread
def base_path(subdir = None):
    path = os.path.dirname(os.path.abspath(__file__))
    if subdir:
        path = f'{path}/{subdir}'
    return path
# Add a custom style for the tabs
custom_style = """
<style>
.sidebar-menu .sidebar-menu-item {
  font-size: 30px;
}
</style>
"""

st.set_page_config(page_title="Your Movie Recommender", page_icon=":movie_camera:",layout="wide")


# Add the custom style to the sidebar
st.sidebar.markdown(custom_style, unsafe_allow_html=True)

# Add some tabs to the sidebar
st.sidebar.markdown("# Lights, camera,... action! :movie_camera:")

tab_1 = st.sidebar.radio(" ", ["Look for recommendations", "Upload your ratings", "About us"])
#tab_2 = st.sidebar.radio("About us", ["Who are we?", "Our mission"])


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:  # if request is successful the code should be 200
        return None
    return r.json()

@st.cache
def get_movies_data():
    #mnames = ['movie_id', 'title', 'genres']
    #df = pd.read_csv('movies.dat', sep='::', header=None, names=mnames,  engine='python', encoding='latin1')
    m_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url']
    movies = pd.read_csv('data/external/u.item', sep='|', names=m_cols, usecols=range(5),
                     encoding='latin-1')
    return movies#.set_index("title")

@st.cache(allow_output_mutation=True)
def get_ratings_data():
    r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings = pd.read_csv('data/external/u.data', sep='\t', names=r_cols,
                      encoding='latin-1')
    return ratings

@st.cache
def get_movies_poster():
    poster_cols = ['movie_id', 'cover_link']
    posters = pd.read_csv('data/external/movie_poster.csv', names=poster_cols,
                      encoding='latin-1')
    return posters

@st.cache
def get_mean_rating(df,movie):
    mean_rating = df[df['movie_id']==movie]['rating'].mean()
    return mean_rating

@st.cache
def get_movie_ids(df,movies):
    ids = []
    for movie in movies:
        ids.append(df[df['title']==movie]['movie_id'].values[0])
    return ids

@st.cache
def get_movies_rated(df,user):
    movies_rated = df[df['user_id']==user]['movie_id'].values
    return movies_rated

@st.cache
def get_rating(df,user,movie):
    ratings_user = df[df['user_id']==user]
    rating = ratings_user[ratings_user['movie_id']==movie]['rating'].values[0]
    return rating

@st.cache
def get_ratings_number(df,user):
    ratings_number = df[df['user_id']==user].shape[0]
    return ratings_number

def print_stars(rating_col,stars):
    if stars==1:
        rating_col.markdown(":star:")
    elif stars==2:
        rating_col.markdown(":star::star:")
    elif stars==3:
        rating_col.markdown(":star::star::star:")
    elif stars==4:
        rating_col.markdown(":star::star::star::star:")
    else:
        rating_col.markdown(":star::star::star::star::star:")


lottie_animation = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_xcyjeP.json")
lottie_animation1 = load_lottieurl("https://assets6.lottiefiles.com/private_files/lf30_bb9bkg1h.json")
lottie_animation2 = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_bcjfw1k6.json")
lottie_animation3 = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_hqe5kv5s.json")
user_id = 944
#user_id = 1

df_movies = get_movies_data()
df_posters = get_movies_poster()
#tab1,tab2 = st.tabs(["Recommendations","Add ratings"])

# HEADER
try:
    if tab_1 == "Look for recommendations":
        left_column,right_column,exterior_column,exterior_column1 = st.columns(4)
        with left_column:
           st.subheader("Feed me some movies")
           st.write("Show me yours and I'll show you mine")
           st.write("[More on how I work]({s})".format(s="https://github.com/maciejkula/spotlight"))
          
        with exterior_column1:
            st_lottie(lottie_animation, width=100, height=200, key="coding")
            
        movies = st.multiselect(
            "Choose movies", list(df_movies['title']), ["Toy Story (1995)", "Babe (1995)"]
        )
        if not movies:
            st.error("Please select at least one movie.")
        else:
            if st.button('Get recommendations'):
                with st.spinner("Looking for recommendations..."):
                    movie_ids = get_movie_ids(df_movies,movies)
                    recommendations = get_recommendations(df_movies,movie_ids)
                    #st.dataframe(recommendations)
    
                    names = recommendations['title'].values
                    posters = recommendations['cover_link'].values
                    mean_rating = recommendations['mean_rating'].values
                    url = recommendations['imdb_url'].values
    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        
                        #st.write(names[0])        
                        original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[0] + '</p>'
                        st.markdown(original_title, unsafe_allow_html=True)

                        response = requests.get(posters[0])
                        if response.status_code == 404:
                            st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                        else:
                            st.image(posters[0])
                        st.write("Mean rating: {m:3.2f}".format(m=mean_rating[0]))
                        st.write("IMDB [link]({u})".format(u=url[0]))
        
    
                    with col2:
                        #st.write(names[1])
                        original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[1] + '</p>'
                        st.markdown(original_title, unsafe_allow_html=True)
                        response = requests.get(posters[1])
                        if response.status_code == 404:
                            st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                        else:
                            st.image(posters[1])
                        st.write("Mean rating: {m:3.2f}".format(m=mean_rating[1]))
                        st.write("IMDB [link]({u})".format(u=url[1]))
                    with col3:
                        #st.write(names[2])
                        original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[2] + '</p>'
                        st.markdown(original_title, unsafe_allow_html=True)
                        response = requests.get(posters[2])
                        if response.status_code == 404:
                            st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                        else:
                            st.image(posters[2])
                        st.write("Mean rating: {m:3.2f}".format(m=mean_rating[2]))
                        st.write("IMDB [link]({u})".format(u=url[2]))
                    with col4:
                        #st.write(names[3])
                        original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[3] + '</p>'
                        st.markdown(original_title, unsafe_allow_html=True)
                        response = requests.get(posters[3])
                        if response.status_code == 404:
                            st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                        else:
                            st.image(posters[3])
                        st.write("Mean rating: {m:3.2f}".format(m=mean_rating[3]))
                        st.write("IMDB [link]({u})".format(u=url[3]))
                    with col5:
                        #st.write(names[4])
                        original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[4] + '</p>'
                        st.markdown(original_title, unsafe_allow_html=True)
                        response = requests.get(posters[4])
                        if response.status_code == 404:
                            st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                        else:
                            st.image(posters[4])
                        st.write("Mean rating: {m:3.2f}".format(m=mean_rating[4]))
                        st.write("IMDB [link]({u})".format(u=url[4]))
    
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
            st_lottie(lottie_animation1, height=300, key="cod")

            
    if tab_1=="Upload your ratings":
        df_ratings = get_ratings_data()
        movies_rated = get_movies_rated(df_ratings,user_id)
        
        st.subheader("Feed me some ratings")
        title = st.selectbox(
            "Choose one movie to rate", list(df_movies['title'])
        )
        movie_id = get_movie_ids(df_movies,[title])[0]
        
        poster = df_posters[df_posters['movie_id']==movie_id]["cover_link"].values[0]
        mean_rating = get_mean_rating(df_ratings, movie_id)
        url = df_movies[df_movies['movie_id']==movie_id]["imdb_url"].values[0]
        
        info_col, rating_col = st.columns(2)
        
        original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + title + '</p>'
        info_col.markdown(original_title, unsafe_allow_html=True)

        response = requests.get(poster)
        if response.status_code == 404:
            info_col.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER',width=250)
        else:
            info_col.image(poster,width=250)
        #info_col.image(poster,width=250)
        
        info_col.write("Mean rating: {m:3.2f}".format(m=mean_rating))
        # info_col.write("more [link]({u})".format(u=url))
        
        if movie_id in movies_rated:
            rating_col.write("Thanks for rating this movie!")
            stars = get_rating(df_ratings,user_id,movie_id)
            print_stars(rating_col,stars)
        else:
            stars = rating_col.radio(
                "Your rating:", ["1","2","3","4","5"]
            )
            stars = int(stars)
            print_stars(rating_col,stars)
            
            if rating_col.button('Send rating'):
                new_rating = {'user_id':user_id,'movie_id':movie_id,'rating':stars,'unix_timestamp':int(time.time())}
                df_ratings.loc[len(df_ratings.index)] = new_rating
                df_ratings.to_csv('data/external/u.data',sep='\t',header=False,index=False)
                st.experimental_rerun()
        
    if tab_1=="Upload your ratings":
            ratings_number = get_ratings_number(df_ratings, user_id)
            st.subheader("Recommendations")
            with st.spinner("Looking for recommendations..."):
                #os.system("dvc repro")
                recommendations = get_user_recommendations(df_movies,user_id)
                #st.dataframe(recommendations)

                names = recommendations['title'].values
                posters = recommendations['cover_link'].values
                mean_rating = recommendations['mean_rating'].values
                url = recommendations['imdb_url'].values

                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                        
                    #st.write(names[0])        
                    original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[0] + '</p>'
                    st.markdown(original_title, unsafe_allow_html=True)

                    response = requests.get(posters[0])
                    if response.status_code == 404:
                        st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                    else:
                        st.image(posters[0])
                    st.write("Mean rating: {m:3.2f}".format(m=mean_rating[0]))
                    st.write("IMDB [link]({u})".format(u=url[0]))
        
    
                with col2:
                    #st.write(names[1])
                    original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[1] + '</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    response = requests.get(posters[1])
                    if response.status_code == 404:
                        st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                    else:
                        st.image(posters[1])
                    st.write("Mean rating: {m:3.2f}".format(m=mean_rating[1]))
                    st.write("IMDB [link]({u})".format(u=url[1]))
                with col3:
                    #st.write(names[2])
                    original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[2] + '</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    response = requests.get(posters[2])
                    if response.status_code == 404:
                        st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                    else:
                        st.image(posters[2])
                    st.write("Mean rating: {m:3.2f}".format(m=mean_rating[2]))
                    st.write("IMDB [link]({u})".format(u=url[2]))
                with col4:
                    #st.write(names[3])
                    original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[3] + '</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    response = requests.get(posters[3])
                    if response.status_code == 404:
                        st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                    else:
                        st.image(posters[3])
                    st.write("Mean rating: {m:3.2f}".format(m=mean_rating[3]))
                    st.write("IMDB [link]({u})".format(u=url[3]))
                with col5:
                    #st.write(names[4])
                    original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + names[4] + '</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    response = requests.get(posters[4])
                    if response.status_code == 404:
                        st.image('https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
                    else:
                        st.image(posters[4])
                    st.write("Mean rating: {m:3.2f}".format(m=mean_rating[4]))
                    st.write("IMDB [link]({u})".format(u=url[4]))
                    
            with st.container():
                st.write("---")    #this actually builds a divider line
                left_column,right_column = st.columns(2)
                with left_column:
                    st.header("Store your ratings")
                    st.write("##")
                    st.write(
                        """
                        Let others know what you thought about movies you've watched!
                        Select a movie and rate it!
                        """
                        
                        )
            with right_column:
                st_lottie(lottie_animation2, height=300, key="cod1")

    if tab_1 == ("About us"):
        tab_1 = ""
        st.header("Meet the team members that made this app possible")
        st.write("---")  # this actually builds a divider line
        left_column, right_column = st.columns(2)
        with left_column:
            st.write("We are so happy to see you here!!"
                     "We take care of you and we don't want you to get bored. So please make us happy having fun while using our app. "
                     "It's raining outside? Do you need a break after working in that project without end?"
                     "If so, you have made the best possible choice by selecting our product. We have developed this product with you and your needs in mind.  "
                     "We really hope you enjoy your time with us and that we see you back soon.")
        with right_column:
            st_lottie(lottie_animation3, height=300, key="cod3")

        column_Marg, column_Nikos, column_Celine, column_Sergio, column_MM, column_Zoltan = st.columns(6)
        with column_Marg:
            # st.write(names[0])
            text = 'Margarida Gonçalves'
            original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + text + '</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            text = "Margarida"
            path_reference = f'{base_path()}/imagenes_reshape/{text}.jpeg'
            input = imread(path_reference)
            st.image(input)
            text = "This is Margarida. \n She's a 21-year-old student from Portugal. She likes cats, and reading books. Does not like Algebra, even though she majored in Mathematics. " \
                   "Moved abroad at the ripe age of 19. Her current goal in life is to get Spanish people not to call her Margarina in Starbucks.\n  Was involved in the front-end development of this project, and also gave her contribution to the initial handling of the data."
            description = '<p style="font-family:sans-serif; color:White; font-size: 10px;">' + text + '</p>'
            st.markdown(description, unsafe_allow_html=True)

        with column_Nikos:
            text = "Nikolaos Athanasopoulos"
            original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + text + '</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            text = "Nikos"
            path_reference = f'{base_path()}/imagenes_reshape/{text}.jpeg'
            input = imread(path_reference)
            st.image(input)
            text = "Hey, this is Nikolaos from Greece , Athens. A 27 year old electrical engineering " \
                   "graduate who worked as a Backend Developer. I find very attractive the creation of web applications " \
                   "using new technologies, mostly the backend part. Though, I have also created some websites, " \
                   "so the frontend part also interests me. In this project i mainly managed to make the given code " \
                   "working for everyone, created a function to get movie recommendations and regarding the frontend " \
                   "I helped a little bit Zoltan to display the images for every movie."
            description = '<p style="font-family:sans-serif; color:White; font-size: 10px;">' + text + '</p>'
            st.markdown(description, unsafe_allow_html=True)

        with column_Celine:
            text = "Celine Odding"
            original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + text + '</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            text = "Celine"
            path_reference = f'{base_path()}/imagenes_reshape/{text}.jpeg'
            input = imread(path_reference)
            st.image(input)
            text = "This is Celine (Su-lien), the scrum master of the project. She came all the way from the Netherlands" \
                   " to do her masters in Barcelona. She is 24 years old and her background is Artificial Intelligence. The best thing about Spain she thinks is pan con tomate"
            description = '<p style="font-family:sans-serif; color:White; font-size: 10px;">' + text + '</p>'
            st.markdown(description, unsafe_allow_html=True)

        with column_Sergio:
            text = "Sergio Hernández"
            original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + text + '</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            text = "Sergio"
            path_reference = f'{base_path()}/imagenes_reshape/{text}.jpeg'
            input = imread(path_reference)
            st.image(input)
            text = "Sergio is a graduated with honors computer sciencist that has coursed postgraduates in Artificial Intelligence, " \
                   "Quantum Computing and Data Science. In his free time, he loves to swim and hike. As much as reading " \
                   "a good book or listening to music.He has played an important role introducing the recommendation models " \
                   "in the app and with the MLOps part."
            description = '<p style="font-family:sans-serif; color:White; font-size: 10px;">' + text + '</p>'
            st.markdown(description, unsafe_allow_html=True)
        with column_MM:
            text = "Maria Magdalena Pol"
            original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + text + '</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            text = "MM"
            path_reference = f'{base_path()}/imagenes_reshape/{text}.jpg'
            input = imread(path_reference)
            st.image(input)
            text = "This is Maria Magdalena. She is 24 years old and is from Mallorca. " \
                   "She is a Mathematician and has been living in Barcelona for the last two years. " \
                   "She loves traveling and sleeping but since she is working and studying she has no time for neither of them... " \
                   "In this project, she was involved in the front-end development working hand by hand with Margarida. "
            description = '<p style="font-family:sans-serif; color:White; font-size: 10px;">' + text + '</p>'
            st.markdown(description, unsafe_allow_html=True)
        with column_Zoltan:
            text = "Zoltan Kunos"
            original_title = '<p style="font-family:sans-serif; color:White; font-size: 12px;">' + text + '</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            text = "Zoltan"
            path_reference = f'{base_path()}/imagenes_reshape/{text}.jpeg'
            input = imread(path_reference)
            st.image(input)
            text = "This is Zoltan. "
            description = '<p style="font-family:sans-serif; color:White; font-size: 10px;">' + text + '</p>'
            st.markdown(description, unsafe_allow_html=True)

except urllib.error.URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
    

