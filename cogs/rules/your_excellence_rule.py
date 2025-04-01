from cogs.rules.base_rule import BaseRule

class YourExcellenceRule(BaseRule):
    """Rule requiring messages to address others as 'Your Excellence'"""
    
    @property
    def name(self):
        return "Your Excellence Rule"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, everyone must address each other as 'Your Excellence'."
    
    async def check_message(self, message):
        # Check if message contains "Your Excellence"
        if "your excellence" not in message.content.lower():
            return "You must address others as 'Your Excellence'! Show some respect!"
        return None