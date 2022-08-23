# Ah Counter "dbinit.py"
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
import logging


async def prepare_guild_settings(bot):
    async with bot.db.cursor() as cursor:
        sql = '''
            CREATE TABLE IF NOT EXISTS guild_settings
                (GUILD_ID BIGINT PRIMARY KEY,
                MILESTONE_CHANNEL BIGINT);
        '''
        await cursor.execute(sql)
        sql = 'SELECT GUILD_ID FROM guild_settings'
        await cursor.execute(sql)
        guild_id_list = [item for t in await cursor.fetchall() for item in t]
        for guild in bot.guilds:
            if guild.id not in guild_id_list:
                sql = '''
                    INSERT INTO guild_settings 
                    (GUILD_ID,MILESTONE_CHANNEL)
                    VALUES ($1, 0)
                '''
                await cursor.execute(sql, guild.id)
                logging.info("Adding new guild to settings: %s", guild.name)
                await bot.db.commit()


async def prepare_tables(bot):
    async with bot.db.cursor() as cursor:
        for guild in bot.guilds:
            guild_id = '{}'.format(guild.id)
            sql = '''
                CREATE TABLE IF NOT EXISTS guild_counters
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    GUILD_ID BIGINT,
                    WORD TEXT,
                    REGEX TEXT,
                    COUNT INT,
                    WORDBOUND BOOL)
            '''
            await cursor.execute(sql.format("\"" + guild_id + "\""))
            check_row_template = 'SELECT count(*) as tot FROM GUILD_COUNTERS WHERE guild_id=$1;'
            await cursor.execute(check_row_template, guild_id)
            if not min(await cursor.fetchone()) > 0:
                sql = '''
                    INSERT INTO GUILD_COUNTERS 
                    (GUILD_ID,WORD,REGEX,COUNT,WORDBOUND) 
                    VALUES 
                    ($1,'Ah', 'ah+', 0 , TRUE)
                '''
                await cursor.execute(sql, guild_id)
                logging.info("Adding new guild to counters: %s", guild.name)
                await bot.db.commit()
