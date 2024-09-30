import os
from dotenv import load_dotenv
from typing import Final

from handlers.responses import handle_response
from video_youtube_api import get_random_video_youtube
from random_fact import get_random_fact
from command_list import get_list_command

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()

# ---------- settings of Tokens ----------
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME : Final = os.getenv("BOT_USERNAME")


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

# ----- Message type handling  -----
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''check if the message is private with the bot or from a group chat.
    The bot only process a response If the message is private or if bot is mentioned in group chat.
    '''
    message_type = update.message.chat.type
    text = update.message.text

    # for debugging purposes
    print(f"User ({update.message.chat.id}) // {message_type} chat: '{text}'")

    if message_type in ["group", "supergroup"]:
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = await handle_response(new_text, update, context)
        else:
            return
    else:
        response = await handle_response(text, update, context)

    if isinstance(response, tuple):
        for message in response:
            print("Bot:", message)
            await update.message.reply_text(message)
    else:
        print("Bot:", response)
        await update.message.reply_text(response)


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
