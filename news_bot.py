import asyncio
import discord
import os
import requests
import logging
import datetime
import dateutil.parser

api_key_index = 0

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

api_keys = [os.environ["GOOGLE_NEWS_API_KEY_1"], os.environ["GOOGLE_NEWS_API_KEY_2"], os.environ["GOOGLE_NEWS_API_KEY_3"]]
CHANNEL_IDS = os.environ["DISCORD_CHANNEL_ID"].split(",")

domains = ['axios.com', 'techmeme.com', 'nbcnews.com', 'npr.org', 'thehill.com', 'abcnews.com', 'cnn.com', 'yahoo.com', 'nypost.com', 'cnbc.com', 'washingtonpost.com', 'ft.com', 'politico.com', 'bloomberg.com', 'wsj.com', 'apnews.com', 'reuters.com', 'nytimes.com', 'bbc.com', 'abcnews.com', 'washingtontimes.com', 'foxnews.com', 'aljazeera.com']

most_recent_timestamps = {}

@client.event
async def on_ready():
    for channel_id in CHANNEL_IDS:
        news_channel = discord.utils.get(client.get_all_channels(), id=int(channel_id))
        await news_channel.send("News bot starting up! I'll be posting news articles.")
    client.loop.create_task(fetch_and_post_news())

async def fetch_and_post_news():
    while True:
        global api_key_index
        max_retries = 3
        retries = 0
        await asyncio.sleep(200)
        for channel_id in CHANNEL_IDS:
            news_channel = discord.utils.get(client.get_all_channels(), id=int(channel_id))
            async for message in news_channel.history(limit=1):
                last_message_timestamp = message.created_at
        params = {
            "domains": ",".join(domains),
            "language": "en",
            "apiKey": api_keys[api_key_index]
        }
        try:
            response = requests.get("https://newsapi.org/v2/everything", params=params)
        except Exception as e:
            logger.error("Error making API request: %s", e)
            continue

        while response.status_code == 429:
            api_key_index = (api_key_index + 1) % len(api_keys)
            if retries >= max_retries:
                break
            params["apiKey"] = api_keys[api_key_index]
            response = requests.get("https://newsapi.org/v2/everything", params=params)
            retries += 1

        try:
            articles = response.json()["articles"]
        except Exception as e:
            logger.error("Error parsing response: %s", e)
            continue

        for article in articles:
            published_at = dateutil.parser.parse(article["publishedAt"])
            publisher = article["source"]["name"]
            if publisher not in most_recent_timestamps or published_at > most_recent_timestamps[publisher]:
                most_recent_timestamps[publisher] = published_at
                for channel_id in CHANNEL_IDS:
                    news_channel = discord.utils.get(client.get_all_channels(), id=int(channel_id))
                    await news_channel.send(f"{article['title']}\n{article['url']}")

BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
client.run(BOT_TOKEN)
