import os
from dotenv import load_dotenv

from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# from googleapiclient.discovery import build
# import random
load_dotenv()


# --- Telegram token from botfather.
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")
# YOUTUBE_API_TOKEN : Final = os.getenv("youtube_api_token") # not yet made 

BOT_USERNAME = os.getenv("BOT_USERNAME")

# youtube = build("youtube", "v3", developerKey=YOUTUBE_API_TOKEN)


# - commands for the bot  - initial, need logic.
async def start_command(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am Slim_Bot. I can help you find the latest videos from YouTube.")


async def help_command(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    help_message = "Here is a list of the commands available. \ntype /start to start the bot  \ntype /help to get help  \ntype /custom to provide a custom command  \ntype /video to search for a video"
    await update.message.reply_text(help_message)


async def custom_command(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am Slim0_1 Bot. I can help you find the latest videos from YouTube.")


# ---  Messages and responses handling -------------------------------- 
async def handle_message(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type in ["group", "supergroup"]:
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print("Bot", response)
    await update.message.reply_text(response)


# response
def handle_response(text: str):
    processed_text = text.lower()

    if "hello" in processed_text:
        return "Hello!"
    elif "how are you" in processed_text:
        return "I am doing well. How about you?"
    elif "what is your name" in processed_text:
        return "My name is Slim0_1 Bot."
    elif "help" in processed_text:
        print("Here is a list of the commands available.")
    else:
        return "I don't understand what you wrote."
    

async def error(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused an error... \ncontext:{Context.error}")



def get_random_video_youtube():

    # TODO: implement logic to fetch random video from YouTube using the YouTube API.
    # TODO: implement logic to handle incoming messages.
    pass



if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    print("Starting bot...")

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)