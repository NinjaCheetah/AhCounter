# AhCounter
Discord bot that counts "Ah", among other words
## Running
To run this bot, you'll first need to set up a .env file with your token and the channel you'd like milestone messages to be sent to. An example file is provided below:

```
# .env
DISCORD_TOKEN=<bot token>
MILESTONE_CHANNEL=<Discord channel ID>
```
Note that the bot must be in the server that the channel is in.

## Extensions
All maintained extensions are loaded automatically on bot startup. Legacy extensions are still present within the bot's source `(root)/cogs/legacy/`, however most of them are either broken because they aren't maintained or they're redundant because their functionallity was merged with other extensions. If you absolutely need one, you can load it by appending `legacy.` before the extension name when using the built-in load command. Ex: `$load legacy.secrethelp`
