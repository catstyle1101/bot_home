#!/home/ubuntu/bot/env/ python
import asyncio
import logging
import sys

from aiogram.utils import executor
import aioschedule as schedule

from config import ADMINS
from create_bot import bot, dp
import handlers

logging.basicConfig(
    level=logging.INFO,
    filename="bot_log.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
    encoding='utf-8'
)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)


async def on_startup(dp):
    for user in ADMINS:
        await bot.send_message(user, 'Bot is online!')
    logging.info('Bot is online')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
