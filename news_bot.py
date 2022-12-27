import asyncio
import discord
import os
import requests
import logging
import datetime
import dateutil.parser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Load the API key for the Google News API from the environment file
api_keys = [os.environ["GOOGLE_NEWS_API_KEY_1"], os.environ["GOOGLE_NEWS_API_KEY_2"], os.environ["GOOGLE_NEWS_API_KEY_3"]]
CHANNEL_IDS = os.environ["DISCORD_CHANNEL_ID"].split(",")

# Set up a counter to keep track of which API key is being used
#api_key_index = 0

# Set up a list of domains to search for articles
domains = ['axios.com', 'techmeme.com', 'nbcnews.com', 'npr.org', 'thehill.com', 'abcnews.com', 'cnn.com', 'yahoo.com', 'nypost.com', 'cnbc.com', 'washingtonpost.com', 'ft.com', 'politico.com', 'bloomberg.com', 'wsj.com', 'apnews.com', 'reuters.com', 'nytimes.com', 'bbc.com', 'abcnews.com', 'washingtontimes.com', 'foxnews.com', 'aljazeera.com']

# Store the most recent timestamps of articles posted to the Discord channel(s) by publisher
most_recent_timestamps = {}

@client.event
async def on_ready():
    # Send a starting message to the "news" channels
    for channel_id in CHANNEL_IDS:
        news_channel = discord.utils.get(client.get_all_channels(), id=int(channel_id))
        await news_channel.send("News bot starting up! I'll be posting news articles.")
    # Start a timer to retrieve news articles every hour
    printed = False  # Flag to track whether the response has been printed
    while True:
        await asyncio.sleep(150)
        # Build the query string for the Google News API
#        query = "when:1h"
        async for message in news_channel.history(limit=1):
            last_message_timestamp = message.created_at
        api_key_index = 0 if "api_key_index" not in locals() else api_key_index 
        params = {
 #           "q": query,
            "domains": ",".join(domains),  # Specify the domains to search
 #           "sortBy": "publishedAt",
            "language": "en",
            "apiKey": api_keys[api_key_index]
        }
        # Make the API request
        try:
            response = requests.get("https://newsapi.org/v2/everything", params=params)
        except Exception as e:
            logger.error("Error making API request: %s", e)
        continue

  	    # Make the API request
        try:
            response = requests.get("https://newsapi.org/v2/everything", params=params)
        except Exception as e:
            logger.error("Error making API request: %s", e)
            continue

        # Check if the API returned a 429 error (Too Many Requests)
        if response.status_code == 429:
            # Switch to the alternate API key
            api_key_index = (api_key_index + 1) % 3  # This will switch between 0, 1, and 2
            continue
        # Send a message with the articles to the "news" channel if they were published after the most recent message in the channel
        for article in articles:
            # Parse the publishedAt string into a datetime object
            published_at = dateutil.parser.parse(article["publishedAt"])
            # Get the publisher of the article
            publisher = article["source"]["name"]
            # Check if the published_at timestamp is newer than the most recent timestamp for this publisher
            if publisher not in most_recent_timestamps or published_at > most_recent_timestamps[publisher]:
                # Update the most recent timestamp for this publisher
                most_recent_timestamps[publisher] = published_at
                # Send the article to the Discord channel(s)
                for channel_id in CHANNEL_IDS:
                    news_channel = discord.utils.get(client.get_all_channels(), id=int(channel_id))
                    await news_channel.send(f"{article['title']}\n{article['url']}")
        else:
            # Switch to the alternate API key
            api_key_index = 1 - api_key_index
# Load the Discord bot token from the environment file
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
client.run(BOT_TOKEN)
