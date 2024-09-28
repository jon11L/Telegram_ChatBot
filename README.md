# Telegram Chatbot.

### Project in construction....
implementing the logic in python.


building a telegram chatbot where several similar commands will be available to get random medias, such as: a randomized music, youtube video (perhaps documentary if triggered specific), a news of the day, a fun fact ...


## Description
Slim_Bot is a Telegram bot that provides users with random trending YouTube videos and interesting facts. It's designed to entertain and inform users through simple commands and natural language interactions.

## Features
- Fetch random trending YouTube videos
- Generate random facts
- Respond to basic conversational inputs
- Handle both private and group chat interactions

## Commands
- `/start`: Initiates the bot and provides a welcome message
- `/help`: Displays a list of available commands (from a markdown file)
- `/custom`: Placeholder for future custom commands
- `/video`: Retrieves and sends a random trending YouTube video
- `/fact`: Generates and sends a random fact

## Technologies Used
- Python
- python-telegram-bot library
- YouTube Data API
- API Ninjas (for random facts)
- requests library for API interactions

## Setup and Installation
1. create a new bot with BotFather on telegram ( type in the search bar )
2. 
3. Clone the repository
4. Install required dependencies:
   ```
   pip install python-telegram-bot google-api-python-client requests
   ```
5. Set up environment variables for your API tokens:
   - `TELEGRAM_BOT_TOKEN`
   - `YOUTUBE_TOKEN`
   - `RANDOM_FACT_TOKEN`
6. Run the bot:
   ```
   python your_bot_file.py
   ```

## Code Structure
- Main bot logic and command handlers
- YouTube video fetching function
- Random fact generation function
- Message handling and response generation

## Future Improvements
- Implement the custom command functionality
- Add more interactive features
- Improve error handling and logging
- Implement user preferences and personalization

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check [issues page] if you want to contribute.



## License
This project is [MIT] licensed.