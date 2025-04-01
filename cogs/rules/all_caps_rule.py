from cogs.rules.base_rule import BaseRule

class AllCapsRule(BaseRule):
    """Rule requiring messages to be written in ALL CAPS"""
    
    @property
    def name(self):
        return "All Caps Rule"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, all messages must be written in ALL CAPS."
    
    async def check_message(self, message):
        # Check if message is all uppercase
        if not message.content.isupper():
            return "YOUR MESSAGE MUST BE IN ALL CAPS! LOUDER!!"
        return None