from cogs.rules.emoji_rule import EmojiRule
from cogs.rules.prefix_rule import PrefixRule
from cogs.rules.pirate_rule import PirateRule
from cogs.rules.punctuation_rule import PunctuationRule
from cogs.rules.rhyme_rule import RhymeRule
from cogs.rules.all_caps_rule import AllCapsRule
from cogs.rules.your_excellence_rule import YourExcellenceRule
from cogs.rules.five_words_rule import FiveWordsRule
from cogs.rules.shakespeare_rule import ShakespeareRule
from cogs.rules.corporate_jargon_rule import CorporateJargonRule
from cogs.rules.overly_formal_rule import OverlyFormalRule
from config import OPENAI_API_KEY
import logging

class RuleFactory:
    """Factory class for creating rule instances"""
    
    @staticmethod
    def create_rule(rule_type, channel, duration, rule_text=None):
        """Create a rule instance based on rule type
        
        Args:
            rule_type: The type of rule to create
            channel: The Discord channel where the rule is active
            duration: The duration in minutes for how long the rule will be active
            rule_text: Optional custom rule text for AI-based rules
            
        Returns:
            A rule instance
        """
        if rule_type == "emoji":
            return EmojiRule(channel, duration)
        elif rule_type == "prefix":
            return PrefixRule(channel, duration)
        elif rule_type == "pirate":
            return PirateRule(channel, duration)
        elif rule_type == "punctuation":
            return PunctuationRule(channel, duration)
        elif rule_type == "rhyme":
            return RhymeRule(channel, duration)
        elif rule_type == "all_caps":
            return AllCapsRule(channel, duration)
        elif rule_type == "your_excellence":
            return YourExcellenceRule(channel, duration)
        elif rule_type == "five_words":
            return FiveWordsRule(channel, duration)
        elif rule_type == "shakespeare":
            return ShakespeareRule(channel, duration)
        elif rule_type == "corporate_jargon":
            return CorporateJargonRule(channel, duration)
        elif rule_type == "overly_formal":
            return OverlyFormalRule(channel, duration)
        elif rule_type == "ai":
            return AIRule(channel, duration, rule_text)
        elif rule_type == "custom":
            return CustomRule(channel, duration, rule_text)
        else:
            # Default to a custom rule if the type is not recognized
            return CustomRule(channel, duration, rule_text)


class AIRule:
    """Rule that uses OpenAI to check message compliance"""
    
    def __init__(self, channel, duration, rule_text):
        self.channel = channel
        self.duration = duration
        self.rule_text = rule_text
        self.openai_handler = None
        self._init_openai_handler()
        from datetime import datetime, timedelta
        self.end_time = datetime.now() + timedelta(minutes=duration)
    
    def _init_openai_handler(self):
        """Initialize OpenAI handler if needed"""
        if not self.openai_handler and OPENAI_API_KEY:
            from cogs.openai_handler import OpenAIHandler
            self.openai_handler = OpenAIHandler(OPENAI_API_KEY)
    
    @property
    def name(self):
        return "AI-Enforced Rule"
    
    @property
    def description(self):
        return self.rule_text
    
    async def check_message(self, message):
        self._init_openai_handler()
        
        if not self.openai_handler:
            return None  # Skip checking if OpenAI is not available
            
        # Check result directly
        complies, reason = await self.openai_handler.check_rule_compliance(self.rule_text, message.content)
        if not complies:
            return reason
            
        return None
    
    def is_expired(self):
        from datetime import datetime
        return datetime.now() > self.end_time


class CustomRule:
    """Rule that uses basic keyword matching for common patterns"""
    
    def __init__(self, channel, duration, rule_text):
        self.channel = channel
        self.duration = duration
        self.rule_text = rule_text
        from datetime import datetime, timedelta
        self.end_time = datetime.now() + timedelta(minutes=duration)
    
    @property
    def name(self):
        return "Custom Rule"
    
    @property
    def description(self):
        return self.rule_text
    
    async def check_message(self, message):
        # For custom rules without AI, use a simple keyword check
        # This is a very basic check that looks for keywords in the rule
        rule_lower = self.rule_text.lower()
        
        if "emoji" in rule_lower:
            import emoji
            if not any(c in emoji.EMOJI_DATA for c in message.content):
                return "Your message needs to include an emoji!"
        elif ("uppercase" in rule_lower or "all caps" in rule_lower) and not message.content.isupper():
            return "Your message needs to be in ALL CAPS!"
        elif "lowercase" in rule_lower and not message.content.islower():
            return "Your message needs to be in lowercase!"
        elif "question" in rule_lower and "?" not in message.content:
            return "Your message needs to be a question!"
        elif "exclamation" in rule_lower and "!" not in message.content:
            return "Your message needs more excitement! Add an exclamation mark!"
            
        return None
    
    def is_expired(self):
        from datetime import datetime
        return datetime.now() > self.end_time