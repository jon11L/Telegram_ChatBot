import random

import googleapiclient.discovery
from config import YOUTUBE_TOKEN

api_service_name = "youtube"
api_version = "v3"

video_type = ["sport", "fun", "nature", "news","events", "animals", "discovery",
            "diy", "travel", "documentary", "music", "science", "technology", "planting",
            "food", "meme", "history", "travel documentary", "popular", "cooking"]

# possible order parameter ['searchSortUnspecified', 'date', 'rating', 'viewCount', 'relevance', 'title', 'videoCount']"


def get_random_video_youtube():
    """
    Retrieves a random trending video from YouTube using the YouTube Data API.
    """
    query = random.choice(video_type)
    print("\n","-"*10, "start querying for videos...", "-"*10)
    print(f" video style: {query}")
    
    try:
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=YOUTUBE_TOKEN)

        request = youtube.search().list(
            part="snippet",
            q=query,
            order='relevance',
            type = "video",
            maxResults=3,
            ).execute()

        if not request['items']:
            return None, "No trending videos found."

        print("-"*10, f"videos found: {len(request['items'])}", "-"*10)
        # print(f"{request['items']}") # debug and read request purposes
        
        # Choose a random video from the results
        video = random.choice(request['items'])
        print(f"selected video items:\n {video} \n")
        video_id = video['id']['videoId']

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return f"Genre:  '{query}'", video_url

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "sorry, it seem like the link did not work"

