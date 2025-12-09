<img height=256 width=256 src="https://cdn.ncxprogramming.com/file/icon/ahcounter.png"></img>
# Ah Counter
A customizable Discord bot for counting words (such as "Ah"!) 

Want to use the public instance? You can find that [here](https://discord.com/api/oauth2/authorize?client_id=737755242757881937&permissions=277025508416&scope=applications.commands%20bot)!

As of December 2025, Ah Counter is tested and working on Python 3.14.2 with up-to-date discord.py and aiosqlite.

## Running
To run this bot, you'll first need to set up a `config.json` file in the bot's root directory. Instructions on how to do this can be found on [the wiki](https://github.com/NinjaCheetah/AhCounter/wiki), and an example config file is provided.

## First Run
The first time the bot is run, or if the database is deleted, the bot will automatically create `counters.db`. This is the database that the word counts are stored in. When the bot starts, it will automatically add "Ah" as a word to count for every server the bot is in.

## The Config File
Ah Counter requires a couple values in its config file to start, which are detailed in the wiki. These include the bot's token, the bot's invite link (if you want your instance to be public), and bot managers. You can learn how to set up the config file [here](https://github.com/NinjaCheetah/AhCounter/wiki/Configuring-the-Bot-(With-the-config-file)).
