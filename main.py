import os
from dotenv import load_dotenv
from typing import Final

from handlers.messages import handle_message
from api_functions.video_youtube_api import get_random_video_youtube
from api_functions.random_fact import get_random_fact
from command_list import get_list_command

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
load_dotenv()

# ---------- settings of Tokens ----------
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")

# ----------preset commands for the bot ----------
async def start(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am Slim_Bot. \nI can help you find some trendy youtube videos. Share some fun facts and more...\ntype command to see the commands available.")


async def youtube_video(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    video = get_random_video_youtube()
    await update.message.reply_text(f"{video}")


async def random_fact(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    fact = get_random_fact()
    await update.message.reply_text(fact)


async def show_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fact = get_list_command()
    await update.message.reply_text(fact, parse_mode=telegram.constants.ParseMode.MARKDOWN)


# ---------- logs error on server side and display one in the chat ----------- 
async def error(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    '''log all errors'''
    print(f"Update error on:\n' {update} '\n\ncontext:\n'  {Context.error} '. ")
    await update.message.reply_text("Oups something happened, please try again.")


if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    print("Starting bot...")

    # commands and description for setting in the botFather if needed
    app.add_handler(CommandHandler('start', start)) # start - to start the bot
    app.add_handler(CommandHandler('help', show_list_command)) # help - to get the list of available commands
    app.add_handler(CommandHandler('video', youtube_video)) # video - get a random trending youtube video
    app.add_handler(CommandHandler('fact', random_fact)) # fact - display a random fact.

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)
