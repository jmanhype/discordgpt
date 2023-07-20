import asyncio
from bot import DiscordBot
from config import Config
import openai

def main():
    """
    The main entry point of the program. It initializes the bot and starts it.
    """

    # Load the configuration from environment variables
    Config.load_from_env()

    # Check if the Discord token and OpenAI API key are set
    if Config.discord_token is None or Config.openai_key is None:
        print("Error: DISCORD_TOKEN and OPENAI_KEY must be set.")
        return

    # Set up your OpenAI API credentials
    openai.api_key = Config.openai_key

    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt="Write a tagline for an ice cream shop."
    )

    # Extract the generated text from the API response
    generated_text = response['choices'][0]['text']

    # Print the generated text
    print("Generated Text:", generated_text)

    # Initialize the bot
    bot = DiscordBot(Config.discord_token)

    # Start the bot
    bot.run()

if __name__ == "__main__":
    main()