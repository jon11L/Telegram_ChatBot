import os
from dotenv import load_dotenv
import http.client
import random, requests, json

from typing import Final

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from googleapiclient.discovery import build
load_dotenv()

# ---------- ----------
# ---------- settings of Tokens ----------
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME : Final = os.getenv("BOT_USERNAME")
RANDOM_FACT_TOKEN : Final = os.getenv("RANDOM_FACT_TOKEN")
YOUTUBE_TOKEN : Final = os.getenv("YOUTUBE_TOKEN") 


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
        youtube = build("youtube", "v3", developerKey=YOUTUBE_TOKEN)
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
    await update.message.reply_text(f"{video}")

# ---------- random fact generator part ----------
def get_random_fact():
    # -- randomfact api endpoint and connection
    api_url = 'https://api.api-ninjas.com/v1/facts?'
    response = requests.get(api_url, headers={'X-Api-Key': RANDOM_FACT_TOKEN})
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        fact = data[0]["fact"]
        return fact
    else:
        print("Error:", response.status_code, response.text)

async def random_fact(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    fact = get_random_fact()
    await update.message.reply_text(fact)


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


#  response communication of user
def handle_response(text: str):
    processed_text = text.lower()

    if "hello" in processed_text:
        return "Hello!"
    elif "how are you" in processed_text:
        return "I am doing well. How about you?"
    elif "what is your name" in processed_text:
        return "My name is Slim0_1 Bot."
    elif "help" in processed_text:
        return ""
    elif "video" in processed_text:
        video_url = get_random_video_youtube()  # Unpack return values
        return video_url
    elif "fact" in processed_text:
        new_fact =  get_random_fact() 
        return new_fact 
    else:
        return "I don't understand what you wrote."
    

async def error(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    '''log all errors'''
    print(f"Update error:\n' {update} '\ncontext:\n'  {Context.error} '. ")
    await update.message.reply_text("an error occurred, please try again.")


if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    print("Starting bot...")

    # commands and description for setting in the botFather if needed
    app.add_handler(CommandHandler('start', start_command)) # start - to start the bot
    app.add_handler(CommandHandler('help', help_command)) # help - to get the list of available commands
    app.add_handler(CommandHandler('custom', custom_command)) # custom command
    app.add_handler(CommandHandler('video', youtube_video)) # video - get a random trending youtube video
    app.add_handler(CommandHandler('fact', random_fact)) # fact - display a random fact.

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)