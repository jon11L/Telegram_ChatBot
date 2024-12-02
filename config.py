import os
from dotenv import load_dotenv
from typing import Final

load_dotenv()

# setting the Tokens here.
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME : Final = os.getenv("BOT_USERNAME")

YOUTUBE_TOKEN : Final = os.getenv("YOUTUBE_TOKEN")
RANDOM_FACT_TOKEN : Final = os.getenv("RANDOM_FACT_TOKEN") 

SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
# SPOTIFY_REDIRECT_URL = os.getenv('SPOTIFY_REDIRECT_URL') # Not in use finally

WEB_HOOK_URL : Final = os.getenv("WEB_HOOK_URL") # for the telegram communication/updates 

# set to True when application is deployed or in production environment to switch communication . 
PRODUCTION : bool = False # False: polling, True: webhook.



# -------------------------------------------
# Optional but recommended settings file (settings.py)
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     app_name: str = "Your App Name"
#     debug: bool = False
#     database_url: str
    
#     class Config:
#         env_file = ".env"

# settings = Settings()