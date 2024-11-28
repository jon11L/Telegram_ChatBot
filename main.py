from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
import uvicorn

import telegram
from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from config import WEB_HOOK_URL, PRODUCTION
from bot import TelegramBot


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
        telegram_bot = await TelegramBot.create_bot()
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


# url needed to receive webhook incoming requests.
@app.post("/webhook")
async def webhook(request: Request):
    ''' Handle incoming updates message/request from telegram. '''
    if PRODUCTION:
        json_data = await request.json()
        update = Update.de_json(json_data, telegram_bot.bot)
        await telegram_bot.process_update(update)
        return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0",
                port=8000, lifespan="on",
                reload=True
                )