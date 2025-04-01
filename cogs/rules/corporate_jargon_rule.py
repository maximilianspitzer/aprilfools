from cogs.rules.base_rule import BaseRule
from config import OPENAI_API_KEY

class CorporateJargonRule(BaseRule):
    """Rule requiring messages to include corporate buzzwords or business jargon"""
    
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
        return "Corporate Jargon"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, all messages must include at least two pieces of corporate buzzwords or business jargon."
    
    async def check_message(self, message):
        """Check if message includes corporate jargon"""
        self._init_openai_handler()
        
        if not self.openai_handler:
            return None  # Skip checking if OpenAI is not available
        
        rule_text = """Messages must include at least two different corporate buzzwords or business jargon terms. 
Examples include: synergy, leverage, actionable, bandwidth, circle back, deep dive, paradigm shift, value-add, 
low-hanging fruit, touch base, moving forward, drill down, thought leadership, best practices, holistic approach, etc. Don't be too strict and be sarcastic."""
        
        # Check result directly
        complies, reason = await self.openai_handler.check_rule_compliance(rule_text, message.content)
        if not complies:
            return reason
        
        return None