import os
from typing import Optional

class Config:
    """
    A class used to represent the configuration for the bot.

    ...

    Attributes
    ----------
    discord_token : str
        a string representing the Discord bot token
    openai_key : str
        a string representing the OpenAI API key

    Methods
    -------
    load_from_env():
        Loads the configuration from environment variables.
    """

    discord_token: Optional[str] = None
    openai_key: Optional[str] = None

    @classmethod
    def load_from_env(cls):
        """
        Loads the configuration from environment variables.

        The following environment variables are used:
        - DISCORD_TOKEN: the Discord bot token
        - OPENAI_KEY: the OpenAI API key

        If an environment variable is not set, the corresponding attribute is set to None.
        """

        cls.discord_token = os.getenv('DISCORD_TOKEN')
        cls.openai_key = os.getenv('OPENAI_KEY')

# Load the configuration from environment variables when the module is imported
Config.load_from_env()