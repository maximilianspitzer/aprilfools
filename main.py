import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import logging
import os
from config import DISCORD_TOKEN, GUILD_ID

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot
class AprilFoolsBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.active_rules = {}  # Store active rules for each channel

    async def setup_hook(self):
        # Load all cogs
        for filename in os.listdir('./cogs'):
            # Skip files that are not cogs (like the openai_handler utility)
            if filename.endswith('.py') and filename != 'openai_handler.py':
                await self.load_extension(f'cogs.{filename[:-3]}')
                logging.info(f'Loaded extension: {filename[:-3]}')
        
        # Sync commands to a specific guild if GUILD_ID is available
        if GUILD_ID:
            try:
                guild_id = int(GUILD_ID)
                guild = discord.Object(id=guild_id)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                logging.info(f"Slash commands synced to guild ID: {guild_id}")
            except (ValueError, TypeError) as e:
                logging.error(f"Invalid GUILD_ID: {e}. Please set a valid guild ID in .env file.")
        else:
            logging.warning("No GUILD_ID set. Skipping command sync to avoid rate limits.")

    async def on_ready(self):
        logging.info(f'{self.user} has connected to Discord!')
        await self.change_presence(activity=discord.Game(name="April Fools AI Mod"))

# Create bot instance
bot = AprilFoolsBot()

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)