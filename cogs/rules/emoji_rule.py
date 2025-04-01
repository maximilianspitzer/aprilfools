import emoji
import re
from cogs.rules.base_rule import BaseRule

class EmojiRule(BaseRule):
    """Rule requiring messages to contain at least one emoji"""
    
    @property
    def name(self):
        return "Emoji Rule"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, all messages must contain at least one emoji."
    
    async def check_message(self, message):
        # Check for standard Unicode emojis
        has_unicode_emoji = any(c in emoji.EMOJI_DATA for c in message.content)
        
        # Check for custom Discord emojis (format: <:name:id> or <a:name:id> for animated)
        discord_emoji_pattern = re.compile(r'<a?:[a-zA-Z0-9_]+:[0-9]+>')
        has_discord_emoji = bool(discord_emoji_pattern.search(message.content))
        
        # Message passes if it has either type of emoji
        if not (has_unicode_emoji or has_discord_emoji):
            print(f"Message without emoji: {message.content}")
            return "you forgor to add some emojis gang! 🥺👉👈"
        
        print(f"Message with emoji: {message.content}")
        return None