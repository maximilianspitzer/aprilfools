from cogs.rules.base_rule import BaseRule
from config import OPENAI_API_KEY
from cogs.openai_handler import OpenAIHandler

class ShakespeareRule(BaseRule):
    """Rule requiring messages to be written in Shakespearean English"""
    
    def __init__(self, channel, duration):
        super().__init__(channel, duration)
        self.openai_handler = None
        self._init_openai_handler()
    
    def _init_openai_handler(self):
        """Initialize OpenAI handler if needed"""
        if not self.openai_handler and OPENAI_API_KEY:
            from cogs.openai_handler import OpenAIHandler
            self.openai_handler = OpenAIHandler(OPENAI_API_KEY)
    
    @property
    def name(self):
        return "Shakespeare Mode"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, all messages must be written in Shakespearean English."
    
    async def check_message(self, message):
        """Check if message is written in Shakespearean English"""
        self._init_openai_handler()
        
        if not self.openai_handler:
            return None  # Skip checking if OpenAI is not available
        
        # Process the message through the handler
        async def handle_result(content, complies, reason):
            return reason  # Just return the reason, the outer method will handle the reply
        
        rule_text = """Messages should attempt to include some Shakespearean or Elizabethan English elements.
Be quite lenient - accept any message that makes even a small effort to sound Shakespearean.
Acceptable elements include:
- Using words like 'thee', 'thou', 'thy', 'thine', 'ye', 'doth', 'hath'
- Adding '-eth' or '-est' endings to verbs (e.g., speaketh, dost)
- Using archaic phrases like 'forsooth', 'prithee', 'verily', 'methinks', 'alas'
- Old-fashioned expressions like 'Good morrow', 'What say you', 'I pray thee'
- Adding 'O' before addressing someone, like 'O friend'
- Using slightly more poetic or flowery language than normal

Only reject messages that make absolutely no attempt to include any Shakespearean elements."""
        
        # Add to buffer and get result
        await self.openai_handler.add_to_buffer(
            message.channel.id,
            rule_text,
            message.content,
            handle_result
        )
        
        # Check result directly for simple messages
        complies, reason = await self.openai_handler.check_rule_compliance(rule_text, message.content)
        if not complies:
            return reason
        
        return None