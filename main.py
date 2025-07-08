import os
import discord
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # The Discord channel ID to monitor
NTFY_URL = os.getenv('NTFY_URL', 'https://ntfy.sh')  # Ntfy server URL
NTFY_TOPIC = os.getenv('NTFY_TOPIC')  # The ntfy topic to send notifications to
NTFY_USERNAME = os.getenv('NTFY_USERNAME', None)  # Optional: Basic auth username
NTFY_PASSWORD = os.getenv('NTFY_PASSWORD', None)  # Optional: Basic auth password
NTFY_PRIORITY = os.getenv('NTFY_PRIORITY', 3)  # Default: normal priority

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Called when the bot has successfully connected to Discord"""
    print(f'{client.user} has connected to Discord!')
    print(f'Monitoring channel ID: {CHANNEL_ID}')
    print(f'Bot is in the following servers:')
    for guild in client.guilds:
        print(f' - {guild.name} (id: {guild.id})')
        for channel in guild.text_channels:
            print(f'   - #{channel.name} (id: {channel.id})')

@client.event
async def on_message(message):
    """Called when a message is received in any channel the bot can see"""
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    
    # Only process messages from the configured channel
    if message.channel.id != CHANNEL_ID:
        return

    print(f"Received message from {message.author.display_name} in {message.channel.name}: {message.content}")
    # Format the message for Ntfy
    timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
    title = f"Message from {message.author.display_name}"
    
    # Include attachments if present
    attachment_urls = ""
    if message.attachments:
        attachment_urls = "\n\nAttachments:\n" + "\n".join([a.url for a in message.attachments])
        
    body = f"{message.content}{attachment_urls}\n\nSent at: {timestamp}"
    
    # Send to Ntfy
    send_to_ntfy(title, body)

def send_to_ntfy(title, message):
    """Sends a notification to Ntfy"""
    ntfy_endpoint = f"{NTFY_URL}/{NTFY_TOPIC}"
    
    headers = {
        "Title": title,
        "Priority": str(NTFY_PRIORITY),
        "Tags": "speech_balloon,discord"
    }
    
    auth = None
    if NTFY_USERNAME and NTFY_PASSWORD:
        auth = (NTFY_USERNAME, NTFY_PASSWORD)
    
    try:
        response = requests.post(
            ntfy_endpoint,
            data=message.encode('utf-8'),
            headers=headers,
            auth=auth
        )
        
        if response.status_code >= 200 and response.status_code < 300:
            print(f"Message forwarded successfully to Ntfy at {datetime.now()}")
        else:
            print(f"Failed to send to Ntfy. Status code: {response.status_code}, Response: {response.text}")
    
    except Exception as e:
        print(f"Error sending to Ntfy: {e}")

if __name__ == "__main__":
    # Check if required environment variables are set
    if not TOKEN:
        print("Error: DISCORD_TOKEN environment variable is not set")
        exit(1)
    
    if not CHANNEL_ID:
        print("Error: CHANNEL_ID environment variable is not set")
        exit(1)
        
    if not NTFY_TOPIC:
        print("Error: NTFY_TOPIC environment variable is not set")
        exit(1)
    
    # Start the Discord bot
    client.run(TOKEN)