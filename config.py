import os
from dotenv import load_dotenv
from typing import Final

load_dotenv()

# setting the Tokens here.
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")

YOUTUBE_TOKEN : Final = os.getenv("YOUTUBE_TOKEN")
RANDOM_FACT_TOKEN : Final = os.getenv("RANDOM_FACT_TOKEN") 

WEB_HOOK_URL : Final = os.getenv("WEB_HOOK_URL")
