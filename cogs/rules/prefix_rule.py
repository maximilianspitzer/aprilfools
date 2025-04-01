from cogs.rules.base_rule import BaseRule

class PrefixRule(BaseRule):
    """Rule requiring messages to start with a specific prefix"""
    
    @property
    def name(self):
        return "Prefix Rule"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, all messages must start with 'In my humble opinion'."
    
    async def check_message(self, message):
        # Check if message starts with the required prefix
        if not message.content.lower().startswith("in my humble opinion"):
            return "Your message must start with 'In my humble opinion,'! Be humble!"
        return None