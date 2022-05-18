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
    except KeyError:
        bot_managers = [0]
    return bot_managers


BOT_MANAGERS = get_bot_managers()


def get_sleepusers():
    sleepusers = []
    try:
        for key in CONFIG["SLEEPUSERS"]:
            i = CONFIG["SLEEPUSERS"][key]
            sleepusers.append(int(i["ID"]))
        return sleepusers
    except KeyError:
        return [0]


SLEEPUSERS = get_sleepusers()
