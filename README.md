# April Fools AI Mod Bot

A Discord bot that enforces silly rules on April Fools' Day using OpenAI's API.

## Features

- Enforce random silly rules in Discord channels for a specified duration
- Create custom rules with the `/custom_rule` command
- Uses OpenAI to check if messages follow the rules
- Automatically ends rules after the specified time has passed
- Supports per-channel rules (different channels can have different active rules)

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on the `.env.example` template and add:
   - Your Discord bot token
   - Your OpenAI API key
4. Invite the bot to your server with the necessary permissions (Send Messages, Read Message History, Use Slash Commands)
5. Run the bot:
   ```
   python main.py
   ```

## Commands

- `/ai_mod [duration]` - Activate a random funny rule for the specified duration (in minutes, default 15)
- `/custom_rule [rule] [duration]` - Create and enforce a custom rule for the specified duration
- `/end_rule` - End the active rule in the current channel

## How It Works

1. When a rule is activated, the bot announces the rule in the channel
2. For every message sent in that channel, the bot uses OpenAI to check if the message follows the rule
3. If the message violates the rule, the bot will reply with a humorous explanation
4. After the specified duration, the rule automatically ends

## Notes

- This bot is designed for fun on April Fools' Day
- Keep rule durations reasonable (1-60 minutes)
- Remember to use your OpenAI API credits responsibly
