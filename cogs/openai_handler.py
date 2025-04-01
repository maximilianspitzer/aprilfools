import openai
import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any

class OpenAIHandler:
    """Handler for OpenAI API calls with cost-saving optimizations"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """Initialize the OpenAI handler
        
        Args:
            api_key: The OpenAI API key
            model: The model to use for completions (default: gpt-3.5-turbo)
        """
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
        self.message_buffer = {}  # {channel_id: [message1, message2, ...]}
        self.buffer_timers = {}   # {channel_id: asyncio.Task}
        self.last_api_call = {}   # {channel_id: datetime}
        self.rate_limit_delay = 1.0  # Seconds between API calls to same channel
        self.max_buffer_size = 5  # Max number of messages to buffer before processing
        self.buffer_timeout = 2.0  # Seconds to wait before processing buffered messages
        self.max_tokens = 4000    # Max tokens allowed in a single API call
        self.token_safety_margin = 400  # Tokens to reserve for the response
        
        # Rough token estimation (character count / 4)
        self.token_estimator = lambda text: len(text) // 4
    
    async def check_rule_compliance(self, rule_text: str, message_content: str) -> Tuple[bool, Optional[str]]:
        """Check if a message complies with a rule
        
        Args:
            rule_text: The rule to check against
            message_content: The message content to check
            
        Returns:
            Tuple of (complies, violation_reason)
            complies: True if the message complies with the rule, False otherwise
            violation_reason: Explanation of the violation if not compliant, None otherwise
        """
        # Check if message is too large for the API (reserve tokens for the rule and response)
        estimated_tokens = self.token_estimator(message_content) + self.token_estimator(rule_text) + self.token_safety_margin
        if estimated_tokens > self.max_tokens:
            logging.warning(f"Message too large for API check: ~{estimated_tokens} tokens")
            return True, None  # Skip checking very large messages
        
        try:
            # Create the prompt for OpenAI
            prompt = f"""
            You are April Fools AI Mod, a bot that enforces fun rules on a Discord server.
            
            RULE: {rule_text}
            
            USER MESSAGE: "{message_content}"
            
            Does this message follow the rule? Respond with:
            - "YES" if the message follows the rule
            - "NO: [brief explanation of violation]" if the message violates the rule
            
            Keep your explanation very brief and humorous.
            """
            
            # Call OpenAI API using the new client
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are April Fools AI Mod, a strict but humorous enforcer of rules."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            
            result = response.choices[0].message.content.strip()
            
            # If the message doesn't follow the rule
            if result.startswith("NO:"):
                return False, result[3:].strip()
            else:
                return True, None
                
        except Exception as e:
            logging.error(f"Error checking message against rule: {e}")
            return True, None  # In case of API errors, let messages through
    
    async def add_to_buffer(self, channel_id: int, rule_text: str, message_content: str, callback) -> None:
        """Add a message to the buffer for batch processing
        
        Args:
            channel_id: The channel ID where the message was sent
            rule_text: The rule to check against
            message_content: The message content to check
            callback: Function to call with the result (message_content, complies, violation_reason)
        """
        # Initialize buffer for this channel if it doesn't exist
        if channel_id not in self.message_buffer:
            self.message_buffer[channel_id] = []
        
        # Add message to buffer
        self.message_buffer[channel_id].append((message_content, rule_text, callback))
        
        # If buffer is full, process it immediately
        if len(self.message_buffer[channel_id]) >= self.max_buffer_size:
            await self.process_buffer(channel_id)
        else:
            # Otherwise, set/reset a timer to process the buffer after a delay
            if channel_id in self.buffer_timers and not self.buffer_timers[channel_id].done():
                self.buffer_timers[channel_id].cancel()
            
            self.buffer_timers[channel_id] = asyncio.create_task(self.buffer_timeout_task(channel_id))
    
    async def buffer_timeout_task(self, channel_id: int) -> None:
        """Task to process buffer after timeout
        
        Args:
            channel_id: The channel ID whose buffer to process
        """
        await asyncio.sleep(self.buffer_timeout)
        await self.process_buffer(channel_id)
    
    async def process_buffer(self, channel_id: int) -> None:
        """Process all messages in the buffer for a channel
        
        Args:
            channel_id: The channel ID whose buffer to process
        """
        # Check if buffer is empty
        if channel_id not in self.message_buffer or not self.message_buffer[channel_id]:
            return
        
        # Apply rate limiting if needed
        if channel_id in self.last_api_call:
            time_since_last_call = (datetime.now() - self.last_api_call[channel_id]).total_seconds()
            if time_since_last_call < self.rate_limit_delay:
                await asyncio.sleep(self.rate_limit_delay - time_since_last_call)
        
        # Get messages from buffer
        messages = self.message_buffer[channel_id].copy()
        self.message_buffer[channel_id] = []
        
        # If we have multiple messages with the same rule, we can batch them together
        rule_groups = {}
        for content, rule, callback in messages:
            if rule not in rule_groups:
                rule_groups[rule] = []
            rule_groups[rule].append((content, callback))
        
        # Process each rule group
        for rule, message_group in rule_groups.items():
            if len(message_group) == 1:
                # If only one message, process it directly
                content, callback = message_group[0]
                complies, reason = await self.check_rule_compliance(rule, content)
                await callback(content, complies, reason)
            else:
                # For multiple messages, create a batch request
                await self.process_batch(rule, message_group)
        
        # Update last API call timestamp
        self.last_api_call[channel_id] = datetime.now()
    
    async def process_batch(self, rule: str, message_group: List[Tuple[str, Any]]) -> None:
        """Process a batch of messages with the same rule
        
        Args:
            rule: The rule to check against
            message_group: List of (content, callback) tuples
        """
        # Format messages for batch processing
        messages_text = "\n".join([f"MESSAGE {i+1}: \"{content}\"" for i, (content, _) in enumerate(message_group)])
        
        # Check if batch is too large for the API
        estimated_tokens = self.token_estimator(messages_text) + self.token_estimator(rule) + self.token_safety_margin
        if estimated_tokens > self.max_tokens:
            # If too large, process individually
            for content, callback in message_group:
                complies, reason = await self.check_rule_compliance(rule, content)
                await callback(content, complies, reason)
            return
        
        try:
            # Create the prompt for batch processing
            prompt = f"""
            You are April Fools AI Mod, a bot that enforces fun rules on a Discord server.
            
            RULE: {rule}
            
            {messages_text}
            
            For each message, indicate if it follows the rule by responding with a list in this format:
            MESSAGE 1: [YES/NO: reason if no]
            MESSAGE 2: [YES/NO: reason if no]
            ...and so on.
            
            Keep your explanations very brief and humorous.
            """
            
            # Call OpenAI API using the new client
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are April Fools AI Mod, a strict but humorous enforcer of rules."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse the results
            lines = result.split("\n")
            for i, (content, callback) in enumerate(message_group):
                message_prefix = f"MESSAGE {i+1}: "
                
                # Find the corresponding line in the response
                for line in lines:
                    if line.startswith(message_prefix):
                        response_part = line[len(message_prefix):].strip()
                        
                        if response_part.startswith("YES"):
                            await callback(content, True, None)
                        elif response_part.startswith("NO:"):
                            reason = response_part[3:].strip()
                            await callback(content, False, reason)
                        else:
                            # If format is unexpected, assume the message is compliant
                            await callback(content, True, None)
                        
                        break
                else:
                    # If we didn't find a line for this message, assume it's compliant
                    await callback(content, True, None)
                    
        except Exception as e:
            logging.error(f"Error in batch processing: {e}")
            
            # In case of API errors, process messages individually if there aren't too many
            if len(message_group) <= 3:
                for content, callback in message_group:
                    complies, reason = await self.check_rule_compliance(rule, content)
                    await callback(content, complies, reason)
            else:
                # Otherwise, just let all messages through
                for content, callback in message_group:
                    await callback(content, True, None)