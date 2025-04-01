from cogs.rules.base_rule import BaseRule
from config import OPENAI_API_KEY

class OverlyFormalRule(BaseRule):
    """Rule requiring messages to be excessively formal and polite"""
    
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
        return "Overly Formal"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, all messages must be excessively formal and polite, as if addressing royalty."
    
    async def check_message(self, message):
        """Check if message is excessively formal and polite"""
        self._init_openai_handler()
        
        if not self.openai_handler:
            return None  # Skip checking if OpenAI is not available
        
        rule_text = """Messages must be somewhat formal and polite, as if speaking to someone of high status.
Be quite lenient - accept any message that has even a small touch of formality or politeness.
Accept messages with Victorian/British-style speech patterns, old-fashioned language, or any polite expressions.
Acceptable examples include:
- "oh golly oh gosh what a splendid day it is today kind sir"
- "I dare say this is rather fascinating"
- "How delightful to see you"
- "Good day to you"
- "Might I suggest..."
- Any message with words like "sir", "madam", "please", "thank you", "kind", "splendid", etc.
Only reject messages that are clearly rude, use slang, or have absolutely no formal elements at all."""
        
        # Check result directly
        complies, reason = await self.openai_handler.check_rule_compliance(rule_text, message.content)
        if not complies:
            return reason
        
        return None