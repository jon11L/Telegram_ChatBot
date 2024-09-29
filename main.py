import os
from dotenv import load_dotenv
# import http.client
import random, requests, json
from typing import Final

from video_youtube_api import get_random_video_youtube
from random_fact import get_random_fact
from responses import handle_response


import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


load_dotenv()

# ---------- ----------
# ---------- settings of Tokens ----------
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME : Final = os.getenv("BOT_USERNAME")
RANDOM_FACT_TOKEN : Final = os.getenv("RANDOM_FACT_TOKEN") 


# ---------- commands for the bot ----------
async def start_command(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am Slim_Bot. I can help you find the latest videos from YouTube.")


async def list_command(update: Update, Context: ContextTypes.DEFAULT_TYPE, ):
    with open("command_list.md", "r") as command_file:
        markdown_content = command_file.read()
    await update.message.reply_text(markdown_content, parse_mode=telegram.constants.ParseMode.MARKDOWN )


# async def custom_command(update: Update, Context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Hi! Custom command to be implemented")


async def youtube_video(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    video = get_random_video_youtube()
    await update.message.reply_text(f"{video}")


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


async def error(update: Update, Context: ContextTypes.DEFAULT_TYPE):
    '''log all errors'''
    print(f"Update error:\n' {update} '\ncontext:\n'  {Context.error} '. ")
    await update.message.reply_text("Oups something happened, please try again.")


if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    print("Starting bot...")

    # commands and description for setting in the botFather if needed
    app.add_handler(CommandHandler('start', start_command)) # start - to start the bot
    app.add_handler(CommandHandler('command', list_command)) # help - to get the list of available commands
    # app.add_handler(CommandHandler('custom', custom_command)) # custom command
    app.add_handler(CommandHandler('video', youtube_video)) # video - get a random trending youtube video
    app.add_handler(CommandHandler('fact', random_fact)) # fact - display a random fact.

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)