import random
import requests, json
import re
from config import TOKEN_CINELIB #, USER_CINELIB, PW_CINELIB

# set up api, get user or Token from movie_lib project.
# call and get a response to check


# def get_token():
#     pass


def extract_text(text):
    '''Extract search query: genre from text using regular expressions'''
    if not text:
        return None

    # print(f"preprocessed text: {text}\n")
    text_patterns = {
        r'movie ([\w-]+(?:[\s|-|,]\w+)?)',
        # r'movie (\w{3,})',
        r'([\w-]+(?:[|-|,]\w+)?) movie',
        # r'(\w{3,}) movie',
        r'movies ([\w-]+(?:[\s|-|,]\w+)?)',
        # r'movies (\w{3,})',
        r'to watch ([\w-]+(?:[\s|-|,]\w+)?)',
        r'to watch some ([\w-]+(?:[\s|-|,]\w+)?)',
        # r'to watch (\w{3,})',
        r'film ([\w-]+(?:[\s|-|,]\w+)?)',
        # r'film (\w{3,})',
        r'([\w-]+(?:[|-|,]\w+)?) film',
        # r'(\w{3,}) film',
    }
    

    for pattern in text_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"match: {match}")
            print(f"match-group: {match.group}")
            print(f"match-group1: {match.group(1)}")
            # replace any ", or -"  with re.sub() ?

            return match.group(1)
    
    return None


def get_list_movie(text):

    max_page = 500
    # page = random.randint(1, max_page)
    headers = {"Authorization": f"Token {TOKEN_CINELIB}"}

    print(f"text: {text}")
    if text:
        max_page = 7
        page = random.randint(1, max_page)
        url = f'http://127.0.0.1:8000/api/v1/movie/list/?page{page}&search={text}'
    else:
        page = random.randint(1, max_page)
        url = f'http://127.0.0.1:8000/api/v1/movie/list/?page={page}'
    print(url)
    # user = USER_CINELIB
    # password = PW_CINELIB
    # credential = f"{user}: {password}"
    # auth=("username", "password")

    # sending Token auth in the header.

    try:
        response = requests.get(url, headers=headers)
        # print(response.json)
    # response = requests.get(api_url, auth=auth)
    except Exception as e:
        print(f"something happened. Could not retrieve a movie.\nerror: {e}")
        return "Unable to get random movie at the moment."

    # if response.status_code == requests.codes.ok or 200:
    if response.status_code == 200:
        data = json.loads(response.text)
        results = data["results"]
        if len(results) == 0:
            print("call ok, but no result found")
            # to wrap later in a Retry while loop.
            url = f'http://127.0.0.1:8000/api/v1/movie/list/?page={page}'
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            results = data["results"]

        return results
    elif response.status_code == 429:
        print (f"Error response:{response.status_code}, throttling", response, response.text)
        return "Looks like something happened. Please try again in a few seconds."
    else:
        print(f"Error: {response.status_code}", response.text, "\n")
        return "Sorry, i could not get any movies right now, ask again later."


def get_movie_detail(movie_id: int):

    url = f'http://127.0.0.1:8000/api/v1/movie/detail/{movie_id}/'
    # sending Token auth in the header.
    headers = {"Authorization": f"Token {TOKEN_CINELIB}"}
    # print(headers)

    try:
        response = requests.get(url, headers=headers)
        print(response.json, "\n\n",  json.loads(response.text))
    # response = requests.get(api_url, auth=auth)
    except Exception as e:
        print(f"something happened. Could not retrieve a movie.\nerror: {e}")
        return "Unable to get random movie at the moment."
    
    if response.status_code == 200:
        data = json.loads(response.text)
        return data

    elif response.status_code == 429:
        print (f"Error response:{response.status_code}, throttling", response)
        return "Looks like something happened. Please try again in a few seconds."
    else:
        print(f"Error: {response.status_code}", response.text, "\n")
        # return "Sorry, i could not get any movies right now, ask again later."
        return "Sorry, i could not get any movies right now, ask again later."


def get_random_movie(**kwargs):
    '''function to get a random movie from the api'''
    # check if extra input data for query
    text = extract_text(kwargs.get('processed_text'))
    # 1 call the get list.
    list_movies = get_list_movie(text)
    # 2 retrieve one movie by selecting a random one
    count = len(list_movies)
    print(f"total movies in the list: {count}")

    r_index = random.randint(1, count -1) # getting a random index

    sel_movie = list_movies[r_index] # extract one random movie element
    print(sel_movie)

    # get the movie id
    if sel_movie and isinstance(sel_movie, dict):
        movie_id = sel_movie.get('id')
    print(f"fetched movie id: {movie_id}")
    # 3 Get the movie detail by calling the movie detail endpoint with the movie id.
    try:
        movie = get_movie_detail(movie_id)
    except Exception as e:
        print("Something happen when fetching movie detail")

    if movie and isinstance(movie, dict):
        # block to construct nice response
        title = movie['title']
        description = movie.get('description', "N/a")
        genre = ' - '.join(movie.get('genre', ''))
        r_date =  movie['release_date'] or "N/a"
        country = ' - '.join(movie['origin_country'])
        language = movie['original_language']
        rating = round(movie['vote_average'], 2)
        casting = movie.get('casting')[0:2]
        main_cast = '\n- '.join([f"{cast['name']} as {cast['role']}" for cast in casting])

        image = movie.get('poster_images', '')
        if image:
            image = image[0]

    movie_info: str = (
        f"\n    **{title}**\n\n "
        f" Genre:  {genre}\nRelease date:  {r_date}\n"
        f" Country:  {country}    //    Language:  {language}\n"
        f" ({rating}/10)\n"
        f"\n Main cast:\n {main_cast}\n"
        f"\n\n                  Description:\n {description}\n\n"

        f"https://image.tmdb.org/t/p/w500{image}"
    )

    # 4 return the movie detail. in a nice format
    return movie_info
