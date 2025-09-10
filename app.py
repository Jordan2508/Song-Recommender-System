import streamlit as st
import pickle
import requests
import pandas
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify Auth
sp=spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="311943dff1914bfa9f044dfc77eab0d8",
    client_secret="472cb6b630b64d73bd1a8acca725f98b",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-library-read"
))

def fetch_poster(song_name):
    try:
        results=sp.search(q=song_name, type="track", limit=1)
        if results['tracks']['items']:
            return results['tracks']['items'][0]['album']['images'][0]['url']
    except Exception:
        pass
    return "https://via.placeholder.com/150"  # fallback image

def recommend(song_name):
    song_index = songs[songs['SongName'] == song_name].index[0]
    distances=sorted(list(enumerate(similarity[song_index])),reverse=True,key=lambda x:x[1])
    recommended_songs=[]
    recommended_posters=[]
    for i in distances[1:6]:
        recommended_songs.append(songs.iloc[i[0]]['SongName'])
        recommended_posters.append(fetch_poster(songs.iloc[i[0]]['SongName']))
    return recommended_songs,recommended_posters


songs=pickle.load(open('song_list.pkl','rb'))
songs_list=songs['SongName'].values
similarity=pickle.load(open('similarity.pkl','rb'))

st.title('🎵Song Recommender System')
st.markdown('⭐ Discover songs similar to your favorites!')

selected_song_name=st.selectbox('Choose your Favourite Song to get some more crispy ones here',songs_list)

if st.button('Show Recommendations 🚀'):
    names,posters=recommend(selected_song_name)
    if names:
        cols=st.columns(len(names))
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f"""
                     <div class="song-card">
                          <img src="{posters[idx]}" width="150" style="border-radius:10px;">
                          <div class="SongName">{names[idx]}</div?
                        </div>
""",unsafe_allow_html=True)
st.markdown("""
    <style>
        /* Dark background image with overlay */
        .stApp {
            background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                              url("https://plus.unsplash.com/premium_photo-1661963052800-6e6b2aeea937?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8bXVzaWMlMjBiYWNrZ3JvdW5kfGVufDB8fDB8fHww");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }

        .song-card {
            text-align: center;
            padding: 10px;
            margin: 3px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            color: white;  /* fixed spelling */
            font-weight: bold;
        }

        .song-card:hover {
            transform: scale(1.50);
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        }

        /* Button hover effect */
        div.stButton > button:first-child {
            background-color: #ff4b4b;
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            transition: all 0.3s ease;
        }

        div.stButton > button:first-child:hover {
            background-color: #ff1a1a;
            transform: scale(1.05);
            box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        }
    </style>
""", unsafe_allow_html=True)


