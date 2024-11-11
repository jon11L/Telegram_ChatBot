from flask import Flask, request, Response

import os
from dotenv import load_dotenv
from typing import Final

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ---------- importing handlers and API functions ----------
from handlers.messages import handle_message
from api_functions.video_youtube_api import get_random_video_youtube
from api_functions.random_fact import get_random_fact
from command_list import get_list_command


load_dotenv()

# initialize Flask app
app = Flask(__name__)

# ---------- settings of Tokens ----------
TELEGRAM_BOT_TOKEN : Final = os.getenv("TELEGRAM_BOT_TOKEN")
# WEB_HOOK : Final = os.getenv("WEB_HOOK_URL")


@app.route("/")
def index():
    return "Hello, this is Slim_Bot!"


async def initialize_bot():
    """This function initializes the bot."""

    bot = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    print("Starting bot...")

    # list of bot commands, handlers and their description for setting in the botFather if needed
    bot.add_handler(CommandHandler('start', start)) # start - to start the bot
    bot.add_handler(CommandHandler('help', show_list_command)) # help - to get the list of available commands
    bot.add_handler(CommandHandler('video', youtube_video)) # video - get a random trending video from youtube
    bot.add_handler(CommandHandler('fact', random_fact)) # fact - get a random fact.
    # messages
    bot.add_handler(MessageHandler(filters.TEXT, handle_message))
    #handle Errors
    bot.add_error_handler(error)

    # await bot.bot.set_webhook(url=f"{WEB_HOOK}")

    return bot



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
    '''log all errors'''
    print(f"Update error on:\n' {update} '\n\ncontext:\n'  {Context.error} '. ")
    await update.message.reply_text("Oups something happened, please try again.")

@app.route("/webhook", methods=["POST"])
async def webhook():
    ''' Handle incoming updates message|request from telegram./ '''
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
                                
        bot_app.process_update(update)



if __name__ == '__main__':
    import asyncio
    app.run(debug=True)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot_app = loop.run_until_complete(initialize_bot())

    # start the polling thread
    loop.create_task(bot_app.run_polling(poll_interval=3))
    print("Polling...")
