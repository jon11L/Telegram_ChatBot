from video_youtube_api import get_random_video_youtube
from random_fact import get_random_fact
from command_list import get_list_command

import random


async def handle_response(text: str, update, context):
    processed_text = text.lower()

    if any(word in processed_text for word in["hello","hey", "what's up", "hi","salut", "hallo"]):
        return  random.choice(["Hello!", "Hey there!", "Hi! How can I assist you?", "Good to see you!"])
    
    elif "how are you" in processed_text:
        return "I am doing well. How about you?"
    
    elif any(word in processed_text for word in["thanks","thank you"]):
        return random.choice(["you are welcome.", "my pleasure"])
    
    elif "what is your name" in processed_text:
        return "My name is Slim Bot."
    
    elif any(word in processed_text for word in["command","commands", "help"]):
        list_of_commands = get_list_command()
        return list_of_commands
    
    elif any(word in processed_text for word in["video","videos","to watch", "youtube"]):
        video_url = get_random_video_youtube()
        return ("here's a video for you:\n\n", video_url)
    
    elif any(word in processed_text for word in["fact","facts", "something interesting", "share something"]):
        fact =  get_random_fact() 
        return ("Did you know:", fact)
    
    elif "weather" in processed_text:
        return "Sorry, I can't provide weather updates yet, but it's probably nice out!"
    
    else:
        return "Sorry, i did not quite catch that, could you repeat?"
