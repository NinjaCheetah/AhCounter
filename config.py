# Ah Counter "config.py"
# Copyright (C) 2022  NinjaCheetah

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import json
import logging

logging.basicConfig(filename="bot.log",
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d:%(name)s:%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


def get_config():
    with open('config.json', 'r') as f:
        try:
            config = json.load(f)
            return config
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Error loading config.json: {}'.format(exc))


CONFIG = get_config()


def get_bot_managers():
    bot_managers = []
    try:
        for key in CONFIG["BOT_MANAGERS"]:
            i = CONFIG["BOT_MANAGERS"][key]
            bot_managers.append(int(i["ID"]))
    except KeyError as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        logging.warning(exc + ". No bot managers are configured.")
        bot_managers = [0]
    return bot_managers


BOT_MANAGERS = get_bot_managers()


def get_banned_words():
    banned_words = []
    try:
        for key in CONFIG["BANNED_WORDS"]:
            banned_words.append(key)
    except KeyError as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        logging.warning(exc + ". No banned words are configured.")
    banned_words.append("\"")
    banned_words.append("\"")
    return banned_words


BANNED_WORDS = get_banned_words()
