import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord API token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# OpenAI API configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Discord Guild ID (for command syncing)
GUILD_ID = os.getenv('GUILD_ID')  # Add to .env file with your guild ID

# Bot configuration
BOT_NAME = "April Fools AI Mod"
COMMAND_PREFIX = "!"
BOT_MESSAGE_DELETE_DELAY = 5  # Seconds to wait before deleting violation messages

# Funny rules ideas (examples)
FUNNY_RULES = [
    "For the next {duration} minutes, all messages must contain at least one emoji.",
    "For the next {duration} minutes, all messages must start with 'In my humble opinion,'.",
    "For the next {duration} minutes, everyone must speak like a pirate.",
    "For the next {duration} minutes, all messages must have perfect punctuation and grammar.",
    "For the next {duration} minutes, all messages must rhyme with the previous message.",
    "For the next {duration} minutes, all messages must be written in ALL CAPS.",
    "For the next {duration} minutes, everyone must address each other as 'Your Excellence'.",
    "For the next {duration} minutes, messages can only contain exactly 5 words.",
    "For the next {duration} minutes, all messages must be written in Shakespearean English.",
    "For the next {duration} minutes, all messages must include at least two pieces of corporate buzzwords or business jargon.",
    "For the next {duration} minutes, all messages must be excessively formal and polite, as if addressing royalty."
]

# Rule types for built-in checkers (matching the order of FUNNY_RULES)
# These determine which built-in rule checker to use for each rule
RULE_TYPES = [
    "emoji",              # Messages must contain emoji
    "prefix",             # Messages must start with "In my humble opinion,"
    "pirate",             # Messages must contain pirate-like terms
    "punctuation",        # Messages must have proper punctuation
    "rhyme",              # Messages must rhyme with previous message
    "all_caps",           # Messages must be in ALL CAPS
    "your_excellence",    # Messages must include "Your Excellence"
    "five_words",         # Messages must contain exactly 5 words
    "shakespeare",        # Messages must be in Shakespearean English
    "corporate_jargon",   # Messages must include corporate jargon
    "overly_formal"       # Messages must be overly formal and polite
]