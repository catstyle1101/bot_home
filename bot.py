#!/home/ubuntu/bot/env/ python
import logging
import sys

from aiogram.utils import executor
from config import ADMINS
from create_bot import bot, dp
from handlers import client, admin, scrapping, magnet_download

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

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
scrapping.register_handlers_scrapping(dp)
magnet_download.register_handlers_magnet_download(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
