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
#API_KEY = os.environ["GOOGLE_NEWS_API_KEY"]
CHANNEL_IDS = os.environ["DISCORD_CHANNEL_ID"].split(",")

# Set up a list of domains to search for articles
domains = ['techcrunch.com', 'nbcnews.com', 'npr.org', 'thehill.com', 'abcnews.com', 'cnn.com', 'finance.yahoo.com', 'nypost.com', 'cnbc.com', 'wapo.com', 'ft.com', 'politico.com', 'bloomberg.com', 'wsj.com', 'apnews.com', 'reuters.com', 'nyt.com', 'bbc.com', 'abcnews.com', 'washingtontimes.com', 'foxnews.com', 'aljazeera.com']

# Store the most recent timestamps of articles posted to the Discord channel(s) by publisher
most_recent_timestamps = {}

@client.event
async def on_ready():
    # Set up a list of API keys to use
    api_keys = [os.environ["GOOGLE_NEWS_API_KEY_1"], os.environ["GOOGLE_NEWS_API_KEY_2"]]
    # Set up a counter to keep track of which API key is being used
    api_key_index = 0
    # Send a starting message to the "news" channels
    for channel_id in CHANNEL_IDS:
        news_channel = discord.utils.get(client.get_all_channels(), id=int(channel_id))
        await news_channel.send("News bot starting up! I'll be posting news articles.")
    # Start a timer to retrieve news articles every hour
    printed = False  # Flag to track whether the response has been printed
    while True:
        await asyncio.sleep(480)
        # Build the query string for the Google News API
#        query = "when:1h"
        async for message in news_channel.history(limit=1):
            last_message_timestamp = message.created_at
        params = {
 #           "q": query,
            "domains": ",".join(domains),  # Specify the domains to search
 #           "sortBy": "publishedAt",
            "apiKey": api_keys[api_key_index]
        }
        # Make the API request
        try:
            response = requests.get("https://newsapi.org/v2/everything", params=params)
            # Reset the API key index to 0 if the request was successful
            api_key_index = 0
        except Exception as e:
            logger.error("Error making API request: %s", e)
            continue
        # Check if the API returned a 429 error (Too Many Requests)
        if response.status_code == 429:
            # Switch to the alternate API key
            api_key_index = 1 - api_key_index
            continue
        # Parse the response and retrieve the articles
        try:
            articles = response.json()["articles"]
        except Exception as e:
            logger.error("Error parsing API response: %s", e)
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

# Load the Discord bot token from the environment file
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
client.run(BOT_TOKEN)
