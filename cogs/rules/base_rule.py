from datetime import datetime, timedelta

class BaseRule:
    """Base class for all rule implementations"""
    
    def __init__(self, channel, duration):
        """Initialize the rule
        
        Args:
            channel: The Discord channel where the rule is active
            duration: The duration in minutes for how long the rule will be active
        """
        self.channel = channel
        self.duration = duration
        self.end_time = datetime.now() + timedelta(minutes=duration)
        
    @property
    def name(self):
        """Return the name of the rule"""
        return "Base Rule"
    
    @property
    def description(self):
        """Return the description of the rule with duration"""
        return f"For the next {self.duration} minutes, this is a base rule."
    
    async def check_message(self, message):
        """Check if a message complies with the rule
        
        Args:
            message: The Discord message to check
            
        Returns:
            None if the message complies with the rule, or a string with the violation explanation
        """
        # Base implementation always passes
        return None
    
    def is_expired(self):
        """Check if the rule has expired
        
        Returns:
            True if the rule has expired, False otherwise
        """
        return datetime.now() > self.end_time