A simple bot that forwards Discord messages from a specific channel to [Ntfy](https://ntfy.sh) notifications.

## Setup

1. Create a Discord bot and get its token
2. Configure environment variables in .env file or directly in docker-compose.yml:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   CHANNEL_ID=discord_channel_id_to_monitor
   NTFY_TOPIC=your_ntfy_topic
   NTFY_PRIORITY=3  # 1-5: min, low, default, high, urgent
   ```

## Running

### Using Docker Compose (recommended)
```sh
docker-compose up -d
```

### Running locally
```sh
pip install -r requirements.txt
python main.py
```

## How it works

The bot monitors a specified Discord channel and forwards any messages to your Ntfy topic, including the sender's name, message content, attachments, and timestamp.