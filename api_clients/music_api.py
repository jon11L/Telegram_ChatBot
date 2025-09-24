import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# from spotipy.oauth2 import SpotifyOAuth
import re
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
#  ---------------------------------------------------------------

def get_spotify_client():
    """Initialize Spotify client using client credentials (no user token required)."""
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(auth_manager=auth_manager)



def extract_genre(text):
    '''Extract music genre from text using regular expressions'''

    # print(f"preprocessed text: {text}\n")
    text_patterns = {
        r'song ([\w-]+(?:[\s|-]\w+)?)', # song + word-word
        r'song (\w{3,})',
        r'music ([\w-]+(?:[\s|-]\w+)?)',
        r'music (\w{3,})',
        r'audio ([\w-]+(?:[\s|-]\w+)?)',
        r'audio (\w{3,})',
        r'track ([\w-]+(?:[\s|-]\w+)?)',
        r'track (\w{3,})',
    }
    
    for pattern in text_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"match: {match}")
            print(f"match-group: {match.group}")
            print(f"match-group1: {match.group(1)}")
            return match.group(1)
    
    return None


def search_track(**kwargs):
    """Search for tracks on Spotify. 
    with a randomized query to return varied song.
    (- query based on a random music genre 
    -a randomized offset to not only reach the top titles)
    -- Return only one song per request.
    """
    # gather the autorization credentials with the spotify clientcredentials
    spotify = get_spotify_client()

    if kwargs.get("genre") != None:
        genre = kwargs.get("genre") # genre given by user in 
        # print(f" given: {genre}")
    else:
        genre = random.choice(music_genre)

    result = False
    tries = 0
    while result == False and tries < 5:
        tries += 1
        
        if tries > 1:
            genre = random.choice(music_genre)

        print("-"*10, "fetching for a song...", "-"*10)
        print(f"Try N:{tries} with genre:{genre}")

        query = f'genre:"{genre}"'
        try:

            # ----- request to Spotify API -----
            request = spotify.search(q=query, limit=5, offset=random.randint(0, 99), type='track')
            # print("\n", request, "\n") # debugging purpose
            
        except Exception as e:
            print(f"something happened could not get a track. \n error: {e}")
            return "Unable to get some music at the moment."
        
        if request:
            if request['tracks']['total'] == 0:
                print(f"total result: '{request['tracks']['total']}, NO RESULT'\n")
            else:
                print(f"total result: '{request['tracks']['total']}, OK'\n")
            # check if the request returned any song, if not it ask again until when  result is True
            if request['tracks']['total'] != 0:
                result = True
        else:
            continue

    if request:
        
        tracks = request['tracks']['items']
        track = random.choice(tracks)
        # print(track) debugging to check what's inside

        track_url : str = track['external_urls']['spotify']
        track_name : str  = track['name']
        artist_name : str  = track['artists'][0]['name']
        release_date : str  = track['album']['release_date'][0:4]

        track_info : str  = f"Genre: '{genre}'\n\nArtist:  {artist_name}\nTrack:  {track_name}\nReleased in {release_date}"

        return track_info, track_url
    else:
        print(f"No tracks found for query: {query}")



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

    # -------- end of trying to improve query --------------------