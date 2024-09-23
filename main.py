import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()


# --- Telegram token from botfather.
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
youtube_api_token = os.getenv('youtube_api_token') # not yet made 


# - commands for the bot  - initial, need logic.
async def start_command(update: Update):
    await update.message.reply_text("Hi! I am Slim0_1 Bot. I can help you find the latest videos from YouTube.")


async def help_command(update: Update):
    await update.message.reply_text("Here is a list of the commands available.")


async def custom_command(update: Update):
    await update.message.reply_text("Custom commands that needs to be configured.")
    await update.message.reply_text("Hi! I am Slim0_1 Bot. I can help you find the latest videos from YouTube.")

# response
def handle_response(text: str):
    processed_text = text.lower()

    if "hello" in processed_text:
        return "Hello!"
    elif "how are you" in processed_text:
        return "I am doing well. How about you?"
    elif "what is your name" in processed_text:
        return "My name is Slim0_1 Bot."
    else:
        return "I don't understand."
