import random
import requests, json
from config import USER_CINELIB, PW_CINELIB, TOKEN_CINELIB

# set up api, get user or Token from movie_lib project.
# call and get a response to check


# def get_token():
#     pass

def get_movie():
    pass


def get_list_movie():

    MAX_PAGE = 500
    page = random.randint(1, MAX_PAGE)
    url = f'http://127.0.0.1:8000/api/v1/movie/list/?page={page}'
    user = USER_CINELIB
    password = PW_CINELIB
    credential = f"{user}: {password}"

    # auth=("username", "password")

    # sending Token auth in the header.
    headers = {"Authorization": f"Token {TOKEN_CINELIB}"}
    print(headers)

    try:
        response = requests.get(url, headers=headers)
        print(response.json)
    # response = requests.get(api_url, auth=auth)

    except Exception as e:
        print(f"something happened. Could not retrieve a movie.\nerror: {e}")
        return "Unable to get random movie at the moment."

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        results = data["results"]

        select = random.sample(results, 2)
        count = len(data["results"])
        r_index = random.randint(1, count -1)

        fetched_movie = data["results"][r_index] # extract one random movie element
        print(fetched_movie)

        # block to construct nice response
        title = fetched_movie['title']
        # genre = [genre for genre in fetched_movie['genre']]
        genre = ' - '.join(fetched_movie['genre'])
        r_date =  fetched_movie['release_date'] or "N/a"
        # country = fetched_movie['origin_country']
        country = ' - '.join(fetched_movie['origin_country'])
        language = fetched_movie['original_language']
        rating = round(fetched_movie['vote_average'], 2)

        movie_info : str  = f"- Title: {title}\n- Genre:  {genre}\n- Release_date:  {r_date}\n- Origin_country:  {country}\n- language:  {language}\n- vote_average: {rating}"

        return movie_info
    else:
        print("Error:", response.status_code, response.text, "\n")
        return "Sorry, i could not get any movies right now, ask again later."



    # print(f"response: {r}")
    # return response