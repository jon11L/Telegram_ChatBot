from video_youtube_api import get_random_video_youtube
from random_fact import get_random_fact

import random


def handle_response(text: str):
    processed_text = text.lower()

    if "hello" in processed_text:
        return  random.choice(["Hello!", "Hey there!", "Hi! How can I assist you?", "Good to see you!"])
    
    elif "how are you" in processed_text:
        return "I am doing well. How about you?"
    
    elif "what is your name" in processed_text:
        return "My name is Slim Bot."
    
    elif "help" in processed_text:
        return random.choice(["How can I assist?", "I'm here to help. What do you need?", "Ask me anything!", "would you like to see the command list?"])
    
    elif "video" in processed_text:
        video_url = get_random_video_youtube()  # Unpack return values
        return f"here's a video for you:\n\n{video_url}"
    
    elif "fact" in processed_text:
        fact =  get_random_fact() 
        return f"Did you know:\n\n{fact}"
    
    elif "weather" in processed_text:
        return "Sorry, I can't provide weather updates yet, but it's probably nice out!"
    
    else:
        return "Sorry, i did not quite catch that, could you repeat?"