import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update

import time

# ---------- get the access token  ---------- 
from config import TELEGRAM_BOT_TOKEN
from config import WEB_HOOK_URL
from config import PRODUCTION

# ---------- importing handlers and API functions ----------
from handlers.messages import handle_message
from command_list import get_list_command
from api_clients.video_youtube_api import get_random_video_youtube
from api_clients.music_api import search_track
from api_clients.random_fact import get_random_fact
from api_clients.weather_api import get_weather_data




class TelegramBot:
    def __init__(self):
        self.bot_app = None


    @classmethod
    async def initialize_bot(cls):
        self = cls()
        self.bot_app = await self.bot_setup()
        return self


    async def bot_setup(self):
        """This function initializes the bot. Building it, giving the command set up"""

        # global bot_app
        # preset of commands for the bot that the user will see in the chat with '/'
        bot_commands = [
        ("start", "Start the bot"),
        ("help", "Get the list of available commands"),
        ("music", "Get a random music track"),
        ("video", "Get a random trending video from Youtube"),
        ("weather", "Get the current weather of the city requested you must specify your city after weather"),
        ("fact", "Get a random fact")
    ]
        try:
            self.bot_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
            await self.bot_app.bot.set_my_commands(bot_commands)

            # list of bot commands and their description for setting in the botFather.
            self.bot_app.add_handler(CommandHandler('start', self.start)) # start - to start the bot
            self.bot_app.add_handler(CommandHandler('help', self.show_list_command)) # help - to get the list of available commands
            self.bot_app.add_handler(CommandHandler('music', self.get_track)) # provide a random track from spotify
            self.bot_app.add_handler(CommandHandler('video', self.youtube_video)) # video - get a random trending video from youtube
            self.bot_app.add_handler(CommandHandler('weather', self.get_weather)) # video - get the weather of the city requested
            self.bot_app.add_handler(CommandHandler('fact', self.random_fact)) # fact - get a random fact.
            # messages
            self.bot_app.add_handler(MessageHandler(filters.TEXT, handle_message))
            #handle Errors
            self.bot_app.add_error_handler(self.error)

            # Initialize the bot
            print("initializing bot...")
            await self.bot_app.initialize()
        except Exception as e:
            print(f"An error occurred: \n\n{str(e)}")
            # await self.bot_shutdown()

        return self.bot_app
    

    async def setup_webhook_or_polling(self):
        """Set polling or webhook depending on the environment."""

        # Webhook/polling handler to receive updates from telegram server
        if PRODUCTION:
            await self.setup_webhook()
        else: 
            await self.setup_polling()


    async def setup_webhook(self):
        webhook_url = f"{WEB_HOOK_URL}/webhook"
        await self.bot_app.run_webhook(url = webhook_url) # Webhook in production.
        print(f"Webhook set to {webhook_url}")


    async def setup_polling(self):
        # start the bot with Polling 
        await self.bot_app.start()
        await self.bot_app.updater.start_polling(poll_interval=3) # Polling for local testing/environment
        print("Bot's Polling...")


    async def bot_shutdown(self):
        """Cleanup resources, stop updates and shutdown the bot."""
        try:
            if PRODUCTION:
                await self.bot_app.bot.delete_webhook()
            
            if self.bot_app.updater:
                await self.bot_app.updater.stop()
                await self.bot_app.updater.shutdown()
            await self.bot_app.stop()
            await self.bot_app.shutdown()
            print("Bot shutdown complete.")
        except Exception as e:
            print(f"Error during cleanup: {e}")


    # ----------preset commands for the bot ----------
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("User typed the command: Start")
        await update.message.reply_text(
            "Hi! I am Slim_Bot. \nI can help you find some trendy youtube videos."
            "Share some fun facts and more...\ntype command to see the commands available."
            )
        

    async def show_list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        commands = get_list_command()
        print("User typed the command: List Command")
        await update.message.reply_text(commands, parse_mode=telegram.constants.ParseMode.MARKDOWN)


    async def youtube_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("User typed the command: Video Youtube")
        video_content = get_random_video_youtube()
        if video_content:
            for content in video_content:
                await update.message.reply_text(f"{content}")
                time.sleep(1)
        else:
            await update.message.reply_text("No video found. Please try again")


    async def random_fact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        fact = get_random_fact()
        print("User typed the command: Fact.")
        await update.message.reply_text(fact)


    async def get_track(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("User typed the command: 'music'\n")
        track_content = search_track()
        print(track_content)

        if track_content:
            for content in track_content:
                await update.message.reply_text(content)
                time.sleep(1)
        else:
            await update.message.reply_text("No tracks found.")



    async def get_weather(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        args = context.args

        if not args:
        # No city specified, prompt the user
            await update.message.reply_text(
            "Please specify a city. For example: /weather Paris\n"
            "Type the city name after the /weather command."
            )
            return
        
        city = args[0].strip()

        try:
            # user must write is city somehow
            weather_data = get_weather_data(city)
            print("User typed the command: weather")
            # print(weather_data)
            await update.message.reply_text(weather_data)
        
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {str(e)}")


    # ---------- logs error on server side and display one in the chat ----------- problem: catches all errror, harder to debug
    async def error(self, update: Update, Context: ContextTypes.DEFAULT_TYPE):
        '''Handle errors occuring on bot updates'''
        print("Update error on:", "\n", {update}, "\n", "context:", f"'{Context.error}'. " )
        await update.message.reply_text("Oups something happened, please try again.")
