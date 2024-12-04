import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# from spotipy.oauth2 import SpotifyOAuth

import random
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET # SPOTIFY_REDIRECT_URL

from templates.music_genre_list import music_genre

# ----------Authentication for retrieving user specfic level data. 
# Oauth flow authentication/require further authentication(url redirect) ----------- 
#  Not in use.

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
    """Search for tracks on Spotify. 
    with a randomized query to return varied song.
    (- query based on a random music genre 
    -a randomized offset to not only reach the top titles)
    -- Return only one song per request.
    """
    spotify = get_spotify_client()

    # ---- preselect a music genre for the query  /in process---------

    # # choose between famous or not famous tracks
    # tag = random.choice(["new", "hipster"])
    # print(tag)

    
    # # add a random year range to the query, optionally add a year range
    # start_year = random.randint(1970, 2024)
    # end_year = start_year + random.randint(5, 10)
    # year_range = f"{start_year}-{end_year}"

    # build the query
    # query = f'genre:"{genre}" tag:{tag} year:"{year_range}"' # +year:{year_range}


    result = False
    tries = 0

    while result == False:
        tries += 1
        genre = random.choice(music_genre)
        print("-"*10, "fetching for a song...", "-"*10)
        print(f"Try N:{tries} with genre:{genre}")

        try:
            query = f'genre:"{genre}"' # +year:{year_range}
            request = spotify.search(q=query, limit=1, offset=random.randint(0, 99), type='track')
            # print(request) # debugging purpose

            print(f"total result is:  '{request['tracks']['total']}'\n")
            # check if the request returned any song, if not it ask again until when  result is True
            if request['tracks']['total'] != 0:
                result = True
            
        except Exception as e:
            print(f"something happened could not get a track. \n error: {e}")
            return "Unable to get some music at the moment."

    if request:
        
        tracks = request['tracks']['items']
        track = random.choice(tracks)
        # print(track) debugging to check what's inside

        track_url : str = track['external_urls']['spotify']
        track_name : str  = track['name']
        artist_name : str  = track['artists'][0]['name']
        release_date : str  = track['album']['release_date'][0:4]

        track_info : str  = f"Genre:  '{genre}'\n\nTrack:  {track_name}\nReleased in:  {release_date}\nArtist:  {artist_name}"
        print(track_info, track_url, "\n\n")

        return track_info, track_url
    else:
        print(f"No tracks found for query: {query}")

