import asyncio
import os
from typing import Final

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

import uvicorn

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ---------- importing handlers and API functions ----------
from handlers.messages import handle_message
from api_functions.video_youtube_api import get_random_video_youtube
from api_functions.random_fact import get_random_fact
from command_list import get_list_command

# from config import Config

load_dotenv()



# ---------- settings of Tokens ----------
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")
WEB_HOOK : Final = os.getenv("WEB_HOOK_URL")

# Set PRODUCTION TO TRUE in production environment 
PRODUCTION = False

# global bot instance
bot_app = None



async def initialize_bot():
    """This function initializes the bot."""

    # preset of commands for the bot that the user will see in the chat with '/'
    commands = [
    ("start", "Start the bot"),
    ("help", "Get the list of available commands"),
    ("video", "Get a random trending video from Youtube"),
    ("fact", "Get a random fact")
]
    
    bot = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    await bot.bot.set_my_commands(commands)

    # list of bot commands and their description for setting in the botFather.
    bot.add_handler(CommandHandler('start', start)) # start - to start the bot
    bot.add_handler(CommandHandler('help', show_list_command)) # help - to get the list of available commands
    bot.add_handler(CommandHandler('video', youtube_video)) # video - get a random trending video from youtube
    bot.add_handler(CommandHandler('fact', random_fact)) # fact - get a random fact.
    
    # messages
    bot.add_handler(MessageHandler(filters.TEXT, handle_message))
    #handle Errors
    bot.add_error_handler(error)

    # Initialize the bot
    await bot.initialize()
    print("initializing bot...")

    return bot


async def setup_webhook_or_polling(bot: Application):
    """Set polling or webhook depending on the environment."""

    # Webhook/polling handler to receive updates from telegram server
    if PRODUCTION:
        webhook_url = f"{WEB_HOOK}/webhook"
        await bot.bot.set_webhook(url = webhook_url)# Webhook in production.
        print(f"Webhook set to {webhook_url}")
    else:
        # start the bot with Polling
        await bot.start()
        await bot.updater.start_polling(poll_interval=3) # Polling for local testing/environment
        print("Polling...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """This function is called when the FastAPI server is started,
        to handles startup and shutdown events.
    """
    global bot_app

    try:
        # Initialize bot with all configurations
        print("Call the bot initialisation...")
        bot_app = await initialize_bot()
        
        # Setup webhook or polling
        await setup_webhook_or_polling(bot_app)
        
        yield
        
    finally:
        # Cleanup on shutdown
        if bot_app:
            await cleanup_bot(bot_app)


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Slim_Bot",
    description="A Telegram bot for learning programming concepts",
    version="1.0.0",
    lifespan=lifespan
)


async def cleanup_bot(bot: Application):
    """Cleanup bot resources"""
    try:
        if PRODUCTION:
            await bot.bot.delete_webhook()
        await bot.stop()
        await bot.shutdown()
        print("Bot shutdown complete")
    except Exception as e:
        print(f"Error during cleanup: {e}")


@app.post("/webhook")
async def webhook(request: Request):
    ''' Handle incoming updates message/request from telegram. '''
    if PRODUCTION:
        json_data = await request.json()
        update = Update.de_json(json_data, bot_app.bot)
        await bot_app.process_update(update)
        return {"status": "ok"}


# ----------preset commands for the bot ----------
async def start(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I am Slim_Bot. \nI can help you find some trendy youtube videos."
        "Share some fun facts and more...\ntype command to see the commands available."
        )

async def youtube_video(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    video = get_random_video_youtube()
    await update.message.reply_text(f"{video}")


async def random_fact(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    fact = get_random_fact()
    await update.message.reply_text(fact)


async def show_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = get_list_command()
    await update.message.reply_text(commands, parse_mode=telegram.constants.ParseMode.MARKDOWN)


# ---------- logs error on server side and display one in the chat ----------- 
async def error(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    '''Handle errors occuring on bot updates'''
    print(f"Update error on:\n' {update} '\n\ncontext:\n'  {Context.error} '. ")
    await update.message.reply_text("Oups something happened, please try again.")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0",
                port=8000, lifespan="on",
                reload=True
                )