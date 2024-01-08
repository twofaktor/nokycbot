# nokyc bot

A telegram bot to list all current [Bisq](https://bisq.network) and [Robosats](https://learn.robosats.com/) offers

# Instructions

- Change `config.py` with your bot token, tor proxy port, and webhook info (if you're going to use webhooks to connect to your bot)
- For development and testing, set your environment variable `MODE` to `'polling'`. For production, set the variable to `'webhook'`
- Run the bot with `python3 bot.py`
