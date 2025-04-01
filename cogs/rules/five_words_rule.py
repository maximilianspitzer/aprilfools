from cogs.rules.base_rule import BaseRule

class FiveWordsRule(BaseRule):
    """Rule requiring messages to contain exactly five words"""
    
    @property
    def name(self):
        return "Five Words Rule"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, messages can only contain exactly 5 words."
    
    async def check_message(self, message):
        # Count words in the message
        words = message.content.strip().split()
        word_count = len(words)
        
        # Check if the message contains exactly 5 words
        if word_count != 5:
            return f"Your message must contain exactly 5 words! You used {word_count}."
        return None