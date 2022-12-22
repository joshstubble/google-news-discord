• git clone repo
• get api tokens for Discord Bot and Google News (NewsAPI). I made two accounts and got two api keys.  
• get channel id from discord channel you want bot to post in. Put channel ID in .ENV. You can add multiple channels in the .env file by separating them with a ','.
• add discord bot to server
• `docker-compose up -d --build`. 

I made two NewsAPI accounts in case a rate limit is hit the code tries the next key. The code as written should not get you rate limited if you do not turn the bot on and off. As I was testing the bot, bringing it up and down, I was hitting rate limits easily. This bot will not get rate limited if you run it and leave it alone with one key. It is not my intention to get around googles api limits on a consistent basis. 

This bot searches a set of domains listed in the code. It is written to track the most recent timestamp of articles by domain and only posts articles if the stored timestamp is later than the new article. 



