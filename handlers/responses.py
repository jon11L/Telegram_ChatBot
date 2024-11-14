from api_functions.video_youtube_api import get_random_video_youtube
from api_functions.random_fact import get_random_fact
from command_list import get_list_command

import random


async def handle_response(text: str, update, context):
    '''function handle a bot response depending on the  message sent by user.'''
    processed_text = text.lower()

    if any(word in processed_text for word in["hello","hey", "what's up", "hi","salut", "hallo"]):
        return  random.choice(["Hello!", "Hey there!", "Hi! How can I assist you?", "Good to see you!"])
    
    elif "how are you" in processed_text:
        return "I am doing well. How about you?"
    
    elif any(word in processed_text for word in["thanks","thank you"]):
        return random.choice(["you are welcome.", "my pleasure", "sure thing", "if i can do anything else?"])
    
    elif "what is your name" in processed_text:
        return random.choice(["My name is Slim Bot.","Slim", "slim bot",
                            "slim bot and you?", "My name is Slim Bot. what is yours?",
                            "i am Slim bot and yourself?"]
                            )
    elif any(word in processed_text for word in["command","commands", "help"]):
        list_of_commands = get_list_command()
        return list_of_commands
    
    elif any(word in processed_text for word in["video","videos","to watch", "youtube"]):
        video_url = get_random_video_youtube()
        return ("here's a video for you:", video_url)
    
    elif any(word in processed_text for word in["fact","facts", "something interesting", "share something"]):
        fact =  get_random_fact() 
        return (random.choice(["Did you know:", "hmm..", "let me think.","oh, there is:"]), fact)
    
    elif "weather" in processed_text:
        return "Sorry, I can't provide weather updates yet, but it's probably nice out!"

    else:
        return random.choice(["Sorry, i did not quite catch that, could you repeat?",
                            "i did not understood", "oh, could you please repeat?", 
                            "i'm sorry, I don't have the answer to that question, but I can help you find something else.",
                            "i'm afraid I can't help you with that"]
                            )
