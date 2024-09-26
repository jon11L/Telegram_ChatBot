import os
from dotenv import load_dotenv

from typing import Final

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from googleapiclient.discovery import build
import random
load_dotenv()

# ---------- ----------
# ---------- settings of Tokens ----------
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")
YOUTUBE_TOKEN : Final = os.getenv("YOUTUBE_TOKEN") 

BOT_USERNAME = os.getenv("BOT_USERNAME")

youtube = build("youtube", "v3", developerKey=YOUTUBE_TOKEN)


# ---------- commands for the bot ----------
async def start_command(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am Slim_Bot. I can help you find the latest videos from YouTube.")


async def help_command(update: Update, Context: ContextTypes.DEFAULT_TYPE, ):
    with open("command_list.md", "r") as command_file:
        markdown_content = command_file.read()
    await update.message.reply_text(markdown_content, parse_mode=telegram.constants.ParseMode.MARKDOWN )


async def custom_command(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Custom command to be implemented")

# ---------- Youtube API uses ----------
# ---------- retrieving the videos ----------
def get_random_video_youtube():
    """
    Retrieves a random trending video from YouTube using the YouTube Data API.
    """
    try:
        video_response = youtube.videos().list(
            part='snippet,statistics',
            chart='mostPopular',
            maxResults=25
        ).execute()

        if not video_response['items']:
            return None, "No trending videos found."

        # Choose a random video from the results
        video = random.choice(video_response['items'])
        video_id = video['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        return video_url
    
    except Exception as e:
        return None, f"An error occurred: {str(e)}"


async def youtube_video(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    video = get_random_video_youtube()
    await update.message.reply_text(f"Getting random video from YouTube...\n{video}")




    



# ---  Messages and responses handling -------------------------------- 
async def handle_message(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f"User ({update.message.chat.id}) // {message_type} chat: '{text}'")

    if message_type in ["group", "supergroup"]:
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print("Bot:", response)
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
        return "sorry, you're own your own... "
    elif "video" in processed_text:
        video_url, error_message = get_random_video_youtube()  # Unpack return values
        if video_url:
            return video_url
        else:
            return error_message
    else:
        return "I don't understand what you wrote."
    

async def error(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused an error... \ncontext:{Context.error}")
    await update.message.reply_text("an error occurred, please try again.")




if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    print("Starting bot...")

    # commands and description for setting in the botFather if needed
    app.add_handler(CommandHandler('start', start_command)) # start - to start the bot
    app.add_handler(CommandHandler('help', help_command)) # help - to get the list of available commands
    app.add_handler(CommandHandler('custom', custom_command)) # custom command
    app.add_handler(CommandHandler('video', get_random_video_youtube)) # video - get a random trending youtube video

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)