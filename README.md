# Ah Counter
Discord bot that counts "Ah", among other words.
## Running
To run this bot, you'll first need to set up a `config.json` file in the bot's root directory (the one with `bot.py` in it!) with your token and the channel you'd like milestone messages to be sent to. An example file is provided below:

```json
# config.json
{
  "DISCORD_TOKEN": "<bot token>",
  "MILESTONE_CHANNEL": <Discord channel ID>
}
```
Note that the bot must be in the server that the channel is in.

## First Run
The first time the bot is run, or if the JSON files are deleted, the bot will automatically create `counters.json` and `devcounters.json`. These are the files that the word counts are stored in. `counters.json` is used for normal operation and `devcounters.json` is used if the bot is in development mode, mostly just for testing new features. This auto-generated file will only count "Ah" by default. Documentation regarding adding new words is coming soon.

## Extensions
All maintained extensions are loaded automatically on bot startup. Legacy extensions are still present within the bot's source `(root)/cogs/legacy/`, however most of them are either broken because they aren't maintained or they're redundant because their functionallity was merged with other extensions. If you absolutely need one, you can load it by appending `legacy.` before the extension name when using the built-in load command. Ex: `$load legacy.secrethelp`
## The Config File
Ah Counter requires a couple values in its config file to start, which are detailed above. On top of that, you are able to specify users that you want on the "sleep users" list. This is a feature designed for fun that replies with "🧢" when these people say "sleep". Details on how this works are coming soon. You can safely omit these values in the meantime and it will not cause issues.
