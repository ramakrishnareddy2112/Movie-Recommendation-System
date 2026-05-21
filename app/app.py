import streamlit as st
import pickle
import requests
import random

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide"
)

# ==============================
# CUSTOM CSS
# ==============================

st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.main {
    background-color: #0E1117;
}

h1 {
    text-align: center;
    color: #E50914;
    font-size: 55px;
    font-weight: bold;
}

h3 {
    text-align: center;
    color: white;
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    height: 3.2em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #ff1e1e;
    color: white;
}

div.stImage img {
    border-radius: 15px;
    transition: 0.3s;
}

div.stImage img:hover {
    transform: scale(1.05);
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("🎬 About Project")

st.sidebar.info(
    "This Movie Recommendation System suggests similar movies using Machine Learning and cosine similarity."
)

st.sidebar.markdown("## 🚀 Tech Stack")

st.sidebar.write("✔ Python")
st.sidebar.write("✔ Streamlit")
st.sidebar.write("✔ Machine Learning")
st.sidebar.write("✔ TMDB API")

# ==============================
# TITLE
# ==============================

st.title("🍿 Movie Recommendation System")

st.markdown(
    "<h3>Discover Similar Movies Instantly</h3>",
    unsafe_allow_html=True
)

# ==============================
# RANDOM MOVIE QUOTES
# ==============================

quotes = [
    "😂 Why so serious? — The Dark Knight",
    "🍿 May the Force be with you.",
    "🤣 I'm the king of the world! — Titanic",
    "🎬 Hasta la vista, baby.",
    "😎 Wakanda Forever!",
    "😂 Avengers... Assemble!",
    "🍕 With great power comes great responsibility.",
    "🤣 I see dead people.",
    "🚀 To infinity and beyond!",
    "🎥 Nobody puts Baby in a corner."
]

random_quote = random.choice(quotes)

st.markdown(
    f"""
    <div style='
        text-align:center;
        font-size:28px;
        color:#FFD700;
        font-weight:bold;
        padding:20px;
        margin-top:20px;
        margin-bottom:30px;
        background-color:#1E1E1E;
        border-radius:15px;
    '>
        {random_quote}
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================
# TMDB API KEY
# ==============================

API_KEY = "4a89d5e5873fb58fb8245d3fbc16b5ae"

# ==============================
# LOAD DATA
# ==============================

movies = pickle.load(open('models/movie_list.pkl', 'rb'))

similarity = pickle.load(open('models/similarity.pkl', 'rb'))

# ==============================
# FETCH POSTER
# ==============================

def fetch_poster(movie_id):

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

        response = requests.get(url, timeout=10)

        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:

            return "https://image.tmdb.org/t/p/w500/" + poster_path

        return "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"

    except:

        return "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"

# ==============================
# RECOMMENDATION FUNCTION
# ==============================

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:20]

    recommended_movies = []

    recommended_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        poster = fetch_poster(movie_id)

        # Skip missing posters
        if "No-Image" not in poster:

            recommended_movies.append(
                movies.iloc[i[0]].title
            )

            recommended_posters.append(poster)

        # Stop after 5 recommendations
        if len(recommended_movies) == 5:
            break

    return recommended_movies, recommended_posters

# ==============================
# MOVIE DROPDOWN
# ==============================

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "🎥 Type or Select a Movie",
    movie_list
)

# ==============================
# RECOMMEND BUTTON
# ==============================

if st.button('🎬 Show Recommendations'):

    with st.spinner('Fetching Recommendations...'):

        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        st.markdown("---")

        cols = st.columns(5)

        for idx, col in enumerate(cols):

            if idx < len(recommended_movie_names):

                with col:

                    st.image(
                        recommended_movie_posters[idx],
                        use_container_width=True
                    )

                    st.markdown(
                        f"""
                        <div style='
                            text-align:center;
                            font-size:18px;
                            font-weight:bold;
                            color:white;
                            padding-top:10px;
                            padding-bottom:20px;
                        '>

                            {recommended_movie_names[idx]}

                        </div>
                        """,
                        unsafe_allow_html=True
                    )