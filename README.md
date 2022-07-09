# Ah Counter
Discord bot that counts "Ah", among other words.

[Website](https://ninjacheetah.github.io/projects/maintained/ahcounter)

## Running
To run this bot, you'll first need to set up a `config.json` file in the bot's root directory. Instructions on how to do this can be found on [the wiki](https://github.com/NinjaCheetah/AhCounter/wiki), and an example config file is provided.

## First Run
The first time the bot is run, or if the database is deleted, the bot will automatically create `counters.db`. This is the database that the word counts are stored in. When the bot starts, it will automatically add "Ah" as a word to count for every server the bot is in.

## The Config File
Ah Counter requires a couple values in its config file to start, which are detailed in the wiki. These include the bot's token, the bot's invite link (if you want your instance to be public), and bot managers. On top of that, you are able to specify users that you want on the "sleep users" list. This is a feature designed for fun that replies with "🧢" when these people say "sleep". You can learn how to set up the config file [here](https://github.com/NinjaCheetah/AhCounter/wiki/Configuring-the-Bot-(With-the-config-file)).
