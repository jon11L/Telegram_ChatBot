# Telegram Chatbot.

### Project in construction....

## Description
Slim_Bot is a Telegram bot that provides users with random trending YouTube videos and interesting facts. It's designed to entertain and inform users through simple commands

## Bot Features
- Fetch random trending YouTube videos
- Generate random facts
- Handle both private and group chat interactions
- Respond to basic conversational inputs

## Commands
- `/start`: Initiates the bot and provides a welcome message
- `/help`: Displays a list of available commands (from a markdown file)
- `/video`: Retrieves and sends a random trending YouTube video
- `/fact`: Generates and sends a random fact

## Technologies Used
- language:
   > Python
- Framework : 
   > Fastapi framework

- libraries:
   > python-telegram-bot library

- API : 
   > Telegram Bot API -- YouTube Data API -- API Ninjas (for random facts)

- requests library for API interactions

## Setup and Installation
1. create a new bot with BotFather on telegram ( type in the search bar )
2. Clone the repository 
3. Install required dependencies:

   ```
   pip install -r requirements.txt.
   ```
   
4. Set up environment variables for your API tokens:
   - `TELEGRAM_BOT_TOKEN`
   - `YOUTUBE_TOKEN`
   - `RANDOM_FACT_TOKEN`

7. Run the bot:
   ```
   python3 main.py
   ```

## Code Structure

- Main bot logic and command handlers
- Message handling and response generation
- YouTube video fetching function
- Random fact generation function

## Future Improvements

- Refactoring the project into separate files V
- deployment 
- Spotify API to fetch for random music.
- improve exisiting feature with optional keyword query (for youtube)
- Improve error handling and logging
- Testing
- Possibly add more interactive features over time.

## Contributing

Feel free to check, clone the project; Contributions, issues, and feature requests are welcome.

## License

This project is [MIT] licensed.