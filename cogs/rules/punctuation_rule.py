import re
from cogs.rules.base_rule import BaseRule

class PunctuationRule(BaseRule):
    """Rule requiring messages to have perfect punctuation and grammar"""
    
    @property
    def name(self):
        return "Punctuation Rule"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, all messages must have perfect punctuation and grammar."
    
    async def check_message(self, message):
        # Simple check for proper capitalization and ending punctuation
        if not re.search(r'[.!?]$', message.content) or message.content != message.content.capitalize():
            return "Your message lacks proper punctuation! Capital letter at the start and period at the end, please."
        return None