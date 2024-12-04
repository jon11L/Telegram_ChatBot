from fastapi import FastAPI, Request
# from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import uvicorn

from telegram import Update

from config import WEB_HOOK_URL, PRODUCTION
from bot import TelegramBot
# from api_clients.music_api import create_spotify_oauth


# Main function that triggers Bot start and shutdown when Fastapi is ran.
@asynccontextmanager
async def lifespan(app: FastAPI):
    """This function is called when the FastAPI server is started,
        to handles startup and shutdown events.
    """
    global telegram_bot

    try:
        # Initialize bot with all configurations
        print("Call the bot initialization...")
        telegram_bot = await TelegramBot.initialize_bot()
        # Setup webhook or polling
        await telegram_bot.setup_webhook_or_polling()
        
        yield
        
    finally:
        # Cleanup on shutdown
        if telegram_bot:
            print("Shutting down Bot...")
            # await telegram_bot.cleanup_bot(telegram_bot)
            await telegram_bot.bot_shutdown()


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="TeleBot",
    description="A Telegram bot to learn and consolidate programming concepts.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def home():
    return {"message": "Hello World"}

# url needed to receive webhook incoming requests from telegram.
@app.post("/webhook")
async def webhook(request: Request):
    ''' Handle incoming updates message/request from telegram. '''
    if PRODUCTION:
        json_data = await request.json()
        update = Update.de_json(json_data, telegram_bot.bot)
        await telegram_bot.process_update(update)
        return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1",
                port=8000, lifespan="on",
                reload=True
                )


# ----------------------------------------------------------------
# in development mode: spotify functions will be cleaned and sorted.
# Those functions below serve for Oauthflow authentication with spotify:
# Are not needed in the end due to the api logic..

# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# implement callback for spotify authentication and token exchange
# @app.get("/spotify/callback")
# async def redirect(): # code: str
#     # sp_oauth = create_spotify_oauth()
#     # token_info = sp_oauth.get_access_token(code)

#     return "return: ok"


# check for user credential and redirect to Spotify specified URL for authentication.
# @app.get("/spotify-login")
# def spotify_login():
#     sp_oauth = create_spotify_oauth()
#     auth_url = sp_oauth.get_authorize_url()
#     print(f"Spotify Redirecting to url: {auth_url}")
#     return  RedirectResponse(url=auth_url)
