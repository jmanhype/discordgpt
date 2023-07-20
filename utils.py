import re
from typing import Tuple

def format_message(content: str) -> str:
    """
    Formats a message before sending it to the Discord server.

    Parameters:
    content (str): The content of the message.

    Returns:
    str: The formatted message.
    """
    # Replace multiple spaces with a single space
    content = re.sub(r'\s+', ' ', content)
    # Trim leading and trailing spaces
    content = content.strip()
    return content

def parse_command(message: str) -> Tuple[str, str]:
    """
    Parses a command from a message.

    A command is a message that starts with '!'. The command name is the first word after '!', and the command argument is the rest of the message.

    Parameters:
    message (str): The message to parse.

    Returns:
    Tuple[str, str]: The command name and argument. If the message is not a command, both are empty strings.
    """
    if not message.startswith('!'):
        return '', ''

    parts = message[1:].split(' ', 1)
    command = parts[0]
    argument = parts[1] if len(parts) > 1 else ''
    return command, argument