from cogs.rules.base_rule import BaseRule
import re
import random
import logging
from collections import defaultdict

# We'll use pronouncing library for better rhyme detection
try:
    import pronouncing
    PRONOUNCING_AVAILABLE = True
except ImportError:
    PRONOUNCING_AVAILABLE = False
    logging.warning("Pronouncing library not available. Using fallback rhyme detection.")

class RhymeRule(BaseRule):
    """Rule requiring messages to rhyme with the previous message"""
    
    # Class-level dictionary to store last words per channel
    # This ensures each channel has its own separate state
    channel_last_words = defaultdict(lambda: None)
    
    def __init__(self, channel, duration):
        super().__init__(channel, duration)
        # Initialize this channel's last word to None
        RhymeRule.channel_last_words[channel.id] = None
    
    @property
    def name(self):
        return "Rhyme Rule"
    
    @property
    def description(self):
        return f"For the next {self.duration} minutes, all messages must rhyme with the previous message."
    
    def get_last_word(self, text):
        """Extract the last word from a text, removing punctuation"""
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        
        # Split and get the last word
        words = text.strip().split()
        if not words:
            return None
            
        # Get last word and remove punctuation
        last_word = re.sub(r'[^\w\']+$', '', words[-1].lower())
        
        # Skip very short words or words with no letters
        if len(last_word) < 2 or not re.search(r'[a-z]', last_word):
            return None
            
        return last_word
    
    def words_rhyme(self, word1, word2):
        """Check if two words rhyme"""
        # Words must be different to rhyme
        if word1.lower() == word2.lower():
            return False
        
        # Use the pronouncing library for phonetic rhyming
        if PRONOUNCING_AVAILABLE:
            # Check if word2 is in the rhymes list for word1
            rhymes = pronouncing.rhymes(word1.lower())
            if word2.lower() in rhymes:
                return True
                
            # If not found in pronouncing, fall back to character-based check
            return self._character_based_rhyme(word1, word2)
        else:
            # Fall back to character-based method
            return self._character_based_rhyme(word1, word2)
    
    def _character_based_rhyme(self, word1, word2):
        """Simple character-based rhyme detection"""
        # Check if words end with the same 2+ characters
        min_length = min(len(word1), len(word2))
        if min_length >= 3:
            # For longer words, check more ending characters
            chars_to_check = min(3, min_length // 2)
            return word1[-chars_to_check:].lower() == word2[-chars_to_check:].lower()
        else:
            # For very short words, just check if they end the same
            return word1[-1].lower() == word2[-1].lower()
    
    def get_rhyme_examples(self, word):
        """Get example words that rhyme with the given word"""
        if not PRONOUNCING_AVAILABLE:
            return None
        
        try:
            rhymes = pronouncing.rhymes(word.lower())
            # Filter out the word itself and get only simple words
            rhymes = [r for r in rhymes if r.lower() != word.lower() and len(r) < 8]
            
            if not rhymes:
                return None
                
            # Return a few random examples
            sample_size = min(3, len(rhymes))
            return random.sample(rhymes, sample_size)
        except:
            return None
    
    async def check_message(self, message):
        """Check if the message rhymes with the previous message in this channel"""
        channel_id = message.channel.id
        
        # Get the last word of the current message
        current_word = self.get_last_word(message.content)
        
        # Skip checking if we can't extract a meaningful word
        if not current_word:
            return None
        
        # Get the last word for this channel
        last_word = RhymeRule.channel_last_words[channel_id]
        
        # If this is the first message with this rule in this channel
        if last_word is None:
            # Store the current word as the last word for this channel
            RhymeRule.channel_last_words[channel_id] = current_word
            return None
        
        # Check if the words rhyme
        if not self.words_rhyme(last_word, current_word):
            # Get rhyme examples
            examples = self.get_rhyme_examples(last_word)
            
            # Create the violation message
            violation = f"Your message should end with a word that rhymes with '{last_word}'!"
            
            # Add examples if available
            if examples:
                violation += f" Examples: {', '.join(examples)}"
                
            return violation
        
        # Update the last word for this channel
        RhymeRule.channel_last_words[channel_id] = current_word
        
        return None