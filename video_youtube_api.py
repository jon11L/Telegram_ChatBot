import os
from typing import Final
from dotenv import load_dotenv
import random
from googleapiclient.discovery import build

load_dotenv()

YOUTUBE_TOKEN : Final = os.getenv("YOUTUBE_TOKEN") 

def get_random_video_youtube():
    """
    Retrieves a random trending video from YouTube using the YouTube Data API.
    """
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_TOKEN)
        video_response = youtube.videos().list(
            part='snippet,statistics',
            chart='mostPopular',
            maxResults=25
        ).execute()

        if not video_response['items']:
            return None, "No trending videos found."

        # Choose a random video from the results
        video = random.choice(video_response['items'])
        video_id = video['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    
    except Exception as e:
        return None, f"An error occurred: {str(e)}"
    

if __name__ == '__main__':
    get_random_video_youtube()