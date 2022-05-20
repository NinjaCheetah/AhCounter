# Ah Counter
Discord bot that counts "Ah", among other words.

[NCX Programming Website](https://ncxprogramming.com/programs/ahcounter)

## Running
To run this bot, you'll first need to set up a `config.json` file in the bot's root directory. Instructions on how to do this can be found on [the wiki](https://github.com/NinjaCheetah/AhCounter/wiki), and an example config file is provided.

## First Run
The first time the bot is run, or if the database is deleted, the bot will automatically create `counters.db`. This is the database that the word counts are stored in. When the bot starts, it will automatically add "Ah" as a word to count for every server the bot is in.

## The Config File
Ah Counter requires a couple values in its config file to start, which are detailed in the wiki. On top of that, you are able to specify users that you want on the "sleep users" list. This is a feature designed for fun that replies with "🧢" when these people say "sleep". Details on how this feature works are coming soon. You can safely omit these values in the meantime without causing issues.


## Docker
This section is outdated and will require updates to work with newer bot versions!

A Dockerfile is now provided for Ah Counter. You can build the image with:
`docker build -t ahcounter .`
and run it with
`docker run -it --rm --name ahcounter ahcounter`
Note that there are currently some issues with Docker, the biggest being that the counters.json file will not be preserved outside of the Docker image.
