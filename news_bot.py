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
API_KEY = os.environ["GOOGLE_NEWS_API_KEY"]
CHANNEL_ID = os.environ["DISCORD_CHANNEL_ID"]

# Set up a list of domains to search for articles
domains = ["ft.com", "politico.com", "bloomberg.com", "wsj.com", "apnews.com", "reuters.com", "nytimes.com", "foxnews.com", "aljazeera.com"]

@client.event
async def on_ready():
    # Send a starting message to the "news" channel
    news_channel = discord.utils.get(client.get_all_channels(), id=int(CHANNEL_ID))
    await news_channel.send("News bot starting up! I'll be posting news articles every minute.")
    # Start a timer to retrieve news articles every hour
    printed = False  # Flag to track whether the response has been printed
    while True:
        await asyncio.sleep(60)
        # Build the query string for the Google News API
#        query = "when:1h"

        params = {
 #           "q": query,
            "domains": ",".join(domains),  # Specify the domains to search
            "sortBy": "publishedAt",
            "apiKey": API_KEY
        }
        # Make the API request
        try:
            response = requests.get("https://newsapi.org/v2/everything", params=params)
        except Exception as e:
            logger.error("Error making API request: %s", e)
            continue
        if not printed:  # Print the response object only if it has not been printed yet
            print(response)
            printed = True
        # Parse the response and retrieve the articles
        try:
            articles = response.json()["articles"]
        except Exception as e:
            logger.error("Error parsing API response: %s", e)
            continue
        # Get the timestamp of the most recent message in the "news" channel
        # Get the timestamp of the most recent message in the "news" channel
        news_channel = discord.utils.get(client.get_all_channels(), id=int(CHANNEL_ID))
        async for message in news_channel.history(limit=1):
            last_message_timestamp = message.created_at

        # Send a message with the articles to the "news" channel if they were published after the most recent message in the channel
        for article in articles:
            # Parse the publishedAt string into a datetime object
            published_at = dateutil.parser.parse(article["publishedAt"])
            # Compare the published_at datetime with the last_message_timestamp datetime
            if published_at > last_message_timestamp:
               await news_channel.send(f"{article['title']}\n{article['url']}")


# Load the Discord bot token from the environment file
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
client.run(BOT_TOKEN)
