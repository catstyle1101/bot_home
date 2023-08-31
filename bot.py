#!/home/ubuntu/bot/env/ python
import asyncio
import logging
import sys

from aiogram.utils import executor
import aioschedule as schedule

from config import ADMINS
from create_bot import bot, dp
from handlers import scrapping, magnet_download
from homework_checker import scrap_homework

logging.basicConfig(
    level=logging.INFO,
    filename="bot_log.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
    encoding='utf-8'
)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)


async def scheduler():
    schedule.every(10).minutes.do(scrap_homework)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(0.1)


async def on_startup(dp):
    for user in ADMINS:
        await bot.send_message(user, 'Bot is online!')
    logging.info('Bot is online')
    asyncio.create_task(scheduler())


scrapping.register_handlers_scrapping(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
