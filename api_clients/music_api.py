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
    try:
        results = spotify.search(q=query, type='track', limit=5, offset=random.randint(0, 99))
        tracks = results['tracks']['items']
        track = random.choice(tracks)
        # print(track) debugging to check what's inside

        track_url = track['external_urls']['spotify']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        print(track_url)
        release_date = track['album']['release_date'][0:4]
        track_info = f"Genre: {query}\n\nTrack: {track_name}\nReleased in: {release_date}\nArtist: {artist_name}"
        print(track_info)

        # return track_url 
        return track_info, track_url 

    except Exception as e:
        print(f"something happened could not get a track. \n error: {e}")
        return "Unable to get some music at the moment."

