# Ah Counter
Discord bot that counts "Ah", among other words.
## Running
To run this bot, you'll first need to set up a `config.json` file in the bot's root directory. Instructions on how to do this can be found on [the wiki](https://github.com/NinjaCheetah/AhCounter/wiki).

## First Run
The first time the bot is run, or if the JSON files are deleted, the bot will automatically create `counters.json`. This is the file that the word counts are stored in. This auto-generated file will only count "Ah" by default.

## Extensions
All maintained extensions are loaded automatically on bot startup. Legacy extensions are still present within the bot's source `(root)/cogs/legacy/`, however most of them are either broken because they aren't maintained or they're redundant because their functionallity was merged with other extensions. If you absolutely need one, you can load it by appending `legacy.` before the extension name when using the built-in load command. Ex: `$load legacy.secrethelp` Support will not be provided for legacy extensions.

## The Config File
Ah Counter requires a couple values in its config file to start, which are detailed above. On top of that, you are able to specify users that you want on the "sleep users" list. This is a feature designed for fun that replies with "🧢" when these people say "sleep". Details on how this works are coming soon. You can safely omit these values in the meantime and it will not cause issues.


## Docker
A Dockerfile is now provided for Ah Counter. You can build the image with:
`docker build -t ahcounter .`
and run it with
`docker run -it --rm --name ahcounter ahcounter`
Note that there are currently some issues with Docker, the biggest being that the counters.json file will not be preserved outside of the Docker image.
