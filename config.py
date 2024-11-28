import os
from dotenv import load_dotenv
from typing import Final

load_dotenv()

# setting the Tokens here.
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME : Final = os.getenv("BOT_USERNAME")

YOUTUBE_TOKEN : Final = os.getenv("YOUTUBE_TOKEN")
RANDOM_FACT_TOKEN : Final = os.getenv("RANDOM_FACT_TOKEN") 

WEB_HOOK_URL : Final = os.getenv("WEB_HOOK_URL")

# set to True when application is deployed or in production environment to switch communication . 
PRODUCTION : bool = False # False: polling, True: webhook.