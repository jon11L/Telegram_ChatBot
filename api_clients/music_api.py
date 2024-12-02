import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

import random
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET # SPOTIFY_REDIRECT_URL

from templates.query_spoti import music_genre

# ---------- for user specfic level data. 
# Oauth flow authentication/require further authentication(url redirect) ----------- 

# # Create a Spotify client with OAuth
# def create_spotify_oauth():
#     return SpotifyOAuth(
#         client_id=SPOTIFY_CLIENT_ID,
#         client_secret=SPOTIFY_CLIENT_SECRET,
#         redirect_uri=SPOTIFY_REDIRECT_URL,
#         scope="user-library-read" # user-read-playback-state,user-read-currently-playing,
#     )

def get_spotify_client():
    """Initialize Spotify client using client credentials (no user token required)."""
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def search_track(): # query: str
    """Search for tracks on Spotify."""
    spotify = get_spotify_client()

    # query_list = ["Rock", "Raegge", "Rap", "Elevator", "2-Step", "8bit", "Ambient Ambient Dub", "pop", "trip-hop", "NY Blues", "Piano Blues", "Piedmont Blues", "Punk Blues", "Ragtime Blues"]
    query = random.choice(music_genre)
    print(f"genre choosen: {query}")
    try:
        results = spotify.search(q=query, type='track', limit=5, offset=random.randint(0, 99))
        tracks = results['tracks']['items']
        track = random.choice(tracks)
        print(track['external_urls']['spotify'])
    except Exception as e:
        print(f"something happened could not get a track. \n error: {e}")
# genre choosen: {query}, 
# # "artist": track["artist"][0]["name"]
#     send = f"genre choosen: {query} \nartist: {track['artist'][0]['name']}"
#     print(send)

    return f"{track['external_urls']['spotify']}"

