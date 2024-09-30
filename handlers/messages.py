import os
from dotenv import load_dotenv
from typing import Final

from telegram import Update
from telegram.ext import ContextTypes
from handlers.responses import handle_response

load_dotenv()

BOT_USERNAME : Final = os.getenv("BOT_USERNAME")


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