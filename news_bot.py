import asyncio
import discord
import os
import requests

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Load the API key for the Google News API from the environment file
API_KEY = os.environ["GOOGLE_NEWS_API_KEY"]
CHANNEL_ID = os.environ["DISCORD_CHANNEL_ID"]

@client.event
async def on_ready():
    # Start a timer to retrieve news articles every minute
    while True:
        await asyncio.sleep(60)
        # Build the query string for the Google News API
        query = "site:ft.com OR site:politico.com OR site:bloomberg.com OR site:wsj.com OR site:apnews.com OR site:reuters.com OR site:nytimes.com OR site:foxnews.com OR site:aljazeera.com when:1h"
        params = {
            "q": query,
            "sortBy": "publishedAt",
            "apiKey": API_KEY
        }
        # Make the API request
        response = requests.get("https://newsapi.org/v2/everything", params=params)
        # Parse the response and retrieve the articles
        articles = response.json()["articles"]
        # Send a message with the articles to the "news" channel
        news_channel = discord.utils.get(client.get_all_channels(), id=int(CHANNEL_ID))
        for article in articles:
            await news_channel.send(f"{article['title']}\n{article['url']}")

# Load the Discord bot token from the environment file
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
client.run(BOT_TOKEN)
