from telegram import Update
from telegram.ext import ContextTypes


from config import BOT_USERNAME
from handlers.responses import handle_response



# ----- Message type handling  -----
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Receive message send by user, 
    Check if the message is private with the bot or from a group chat.
    The bot only process a response If the message is private or
    if bot is mentioned in the group chat.
    Message destinated to the bot are then send to response handler to be processed
    '''
    message_type = update.message.chat.type
    text = update.message.text

    # for debugging purposes
    print(f"{message_type} chat. -- User({update.message.chat.id}), message: '{text}'")

    # check if the message is sent from a group chat or private.
    if message_type in ["group", "supergroup"]:
        # bot mentionned, bot respond (in group chat)
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip().lower()
            response = await handle_response(new_text)
        else:
            # bot not mentionned in group chat. no further action
            return
    else:
        response = await handle_response(text) # removed update and context, seemed unnecessary for this operation

    # allow more than a single response to a message.
    if isinstance(response, tuple):
        for message in response:
            print("Bot:", message)
            await update.message.reply_text(message)
            
    else:
        print("Bot:", response)
        await update.message.reply_text(response)