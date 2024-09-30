import os
from typing import Final
from dotenv import load_dotenv

import requests, json

load_dotenv()

RANDOM_FACT_TOKEN : Final = os.getenv("RANDOM_FACT_TOKEN") 


def get_random_fact():
    ''' retrieve a random fact using ninjaApi '''
    api_url = 'https://api.api-ninjas.com/v1/facts?'
    response = requests.get(api_url, headers={'X-Api-Key': RANDOM_FACT_TOKEN})
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        fact = data[0]["fact"]
        return fact
    else:
        print("Error:", response.status_code, response.text)
        return "Sorry, i could not think of any fact right now, ask again later."
