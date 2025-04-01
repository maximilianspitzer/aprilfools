import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
import logging
from datetime import datetime, timedelta
from config import OPENAI_API_KEY, FUNNY_RULES, RULE_TYPES, BOT_MESSAGE_DELETE_DELAY
from cogs.rules import RuleFactory
import openai

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

class AIMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_rules = {}  # {channel_id: rule_instance}
        self.rule_timers = {}   # {channel_id: asyncio.Task}

    @app_commands.command(name="ai_mod", description="Activate the AI Mod for April Fools")
    @app_commands.describe(duration="Duration in minutes for the rule to be active (1-60)")
    async def ai_mod(self, interaction: discord.Interaction, duration: int = 15):
        """Enable AI Mod to enforce a funny rule for a specified duration"""
        if not 1 <= duration <= 60:
            await interaction.response.send_message("Duration must be between 1 and 60 minutes", ephemeral=True)
            return
        
        # Select a random rule and its type from the config
        rule_idx = random.randint(0, len(FUNNY_RULES) - 1)
        rule_text = FUNNY_RULES[rule_idx].format(duration=duration)
        rule_type = RULE_TYPES[rule_idx]
        
        channel_id = interaction.channel_id
        
        # Create a rule instance using the factory
        rule = RuleFactory.create_rule(rule_type, interaction.channel, duration)
        
        # Store active rule
        self.active_rules[channel_id] = rule
        
        # Cancel existing timer if there is one
        if channel_id in self.rule_timers and not self.rule_timers[channel_id].done():
            self.rule_timers[channel_id].cancel()
        
        # Create a new timer
        self.rule_timers[channel_id] = asyncio.create_task(self.end_rule_timer(channel_id, duration))
        
        # Announce the rule
        await interaction.response.send_message(f"🤖 **AI MOD ANNOUNCEMENT** 🤖\n\n{rule.description}\n\nThis rule will be enforced for the next {duration} minutes!")

    @app_commands.command(name="trigger_rule", description="Trigger a specific rule by name")
    @app_commands.describe(
        rule_type="The specific rule to enforce",
        duration="Duration in minutes for the rule to be active (1-60)"
    )
    @app_commands.choices(rule_type=[
        app_commands.Choice(name="Emoji Rule", value="emoji"),
        app_commands.Choice(name="Prefix Rule", value="prefix"),
        app_commands.Choice(name="Pirate Rule", value="pirate"),
        app_commands.Choice(name="Punctuation Rule", value="punctuation"),
        app_commands.Choice(name="Rhyme Rule", value="rhyme"),
        app_commands.Choice(name="All Caps Rule", value="all_caps"),
        app_commands.Choice(name="Your Excellence Rule", value="your_excellence"),
        app_commands.Choice(name="Five Words Rule", value="five_words"),
        app_commands.Choice(name="Shakespeare Rule", value="shakespeare"),
        app_commands.Choice(name="Corporate Jargon Rule", value="corporate_jargon"),
        app_commands.Choice(name="Overly Formal Rule", value="overly_formal")
    ])
    async def trigger_rule(self, interaction: discord.Interaction, rule_type: str, duration: int = 15):
        """Trigger a specific rule by name"""
        if not 1 <= duration <= 60:
            await interaction.response.send_message("Duration must be between 1 and 60 minutes", ephemeral=True)
            return
        
        channel_id = interaction.channel_id
        
        # Create a rule instance using the factory
        rule = RuleFactory.create_rule(rule_type, interaction.channel, duration)
        
        # Store active rule
        self.active_rules[channel_id] = rule
        
        # Cancel existing timer if there is one
        if channel_id in self.rule_timers and not self.rule_timers[channel_id].done():
            self.rule_timers[channel_id].cancel()
        
        # Create a new timer
        self.rule_timers[channel_id] = asyncio.create_task(self.end_rule_timer(channel_id, duration))
        
        # Announce the rule
        await interaction.response.send_message(f"🤖 **AI MOD ANNOUNCEMENT** 🤖\n\n{rule.description}\n\nThis rule will be enforced for the next {duration} minutes!")

    @app_commands.command(name="custom_rule", description="Create a custom rule enforced by AI")
    @app_commands.describe(
        rule="The rule to enforce",
        duration="Duration in minutes for the rule to be active (1-60)",
        use_ai="Whether to use AI for checking (more expensive but handles complex rules)"
    )
    async def custom_rule(self, interaction: discord.Interaction, rule: str, duration: int = 15, use_ai: bool = False):
        """Create a custom rule to be enforced by the bot"""
        if not 1 <= duration <= 60:
            await interaction.response.send_message("Duration must be between 1 and 60 minutes", ephemeral=True)
            return
        
        channel_id = interaction.channel_id
        
        # Format the rule
        formatted_rule = f"For the next {duration} minutes, {rule}"
        
        # Create a rule instance using the factory
        rule_instance = RuleFactory.create_rule(
            "ai" if use_ai else "custom", 
            interaction.channel, 
            duration, 
            formatted_rule
        )
        
        # Store active rule
        self.active_rules[channel_id] = rule_instance
        
        # Cancel existing timer if there is one
        if channel_id in self.rule_timers and not self.rule_timers[channel_id].done():
            self.rule_timers[channel_id].cancel()
        
        # Create a new timer
        self.rule_timers[channel_id] = asyncio.create_task(self.end_rule_timer(channel_id, duration))
        
        # Announce the rule
        await interaction.response.send_message(f"🤖 **AI MOD ANNOUNCEMENT** 🤖\n\n{formatted_rule}\n\nThis rule will be enforced for the next {duration} minutes!")

    @app_commands.command(name="end_rule", description="End the currently active rule in this channel")
    async def end_rule_command(self, interaction: discord.Interaction):
        """End the currently active rule in this channel"""
        channel_id = interaction.channel_id
        
        if channel_id not in self.active_rules:
            await interaction.response.send_message("There is no active rule in this channel", ephemeral=True)
            return
        
        # End the rule
        await self.end_rule(channel_id)
        await interaction.response.send_message("The active rule has been ended!")

    async def end_rule_timer(self, channel_id, duration):
        """Timer to automatically end a rule after the specified duration"""
        try:
            await asyncio.sleep(duration * 60)  # Convert minutes to seconds
            if channel_id in self.active_rules:
                await self.end_rule(channel_id)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logging.error(f"Error in rule timer: {e}")

    async def end_rule(self, channel_id):
        """End an active rule in a channel"""
        if channel_id in self.active_rules:
            rule = self.active_rules[channel_id]
            channel = rule.channel
            
            # Remove the rule
            del self.active_rules[channel_id]
            
            # Send end message
            await channel.send(f"🤖 **AI MOD ANNOUNCEMENT** 🤖\n\nThe rule: '{rule.description}' has ended. You are free... for now! 😈")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Check messages against active rules"""
        # Ignore bot messages to prevent feedback loops
        if message.author.bot:
            return
            
        channel_id = message.channel.id
        
        # If there's an active rule for this channel
        if channel_id in self.active_rules:
            rule = self.active_rules[channel_id]
            
            # Check if the rule is still active
            if rule.is_expired():
                await self.end_rule(channel_id)
                return
                
            # Check message against the rule
            violation = await rule.check_message(message)
            
            # If there's a violation, handle it
            if violation:
                await self.handle_rule_violation(message, violation)

    async def handle_rule_violation(self, message, violation):
        """Handle a rule violation by deleting the message and notifying the user"""
        try:
            # Create a notification mentioning the user
            violation_msg = await message.channel.send(
                f"{message.author.mention} 🚨 **RULE VIOLATION** 🚨\n{violation}",
                allowed_mentions=discord.AllowedMentions(users=True)
            )
            
            # Try to delete the violating message
            try:
                await message.delete()
            except discord.errors.Forbidden:
                logging.warning(f"Bot doesn't have permission to delete messages in {message.channel.name}")
            except discord.errors.NotFound:
                # Message already deleted
                pass
            except Exception as e:
                logging.error(f"Error deleting message: {e}")
            
            # Delete our violation message after a delay
            await asyncio.sleep(BOT_MESSAGE_DELETE_DELAY)
            try:
                await violation_msg.delete()
            except:
                pass
                
        except Exception as e:
            logging.error(f"Error handling rule violation: {e}")

async def setup(bot):
    await bot.add_cog(AIMod(bot))