#!/home/ubuntu/bot/env/ python
import logging
import sys

from aiogram.utils import executor

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
    """
    Asynchronous function that is called when the bot starts up.

    Args:
        dp (Dispatcher): The dispatcher object used to handle updates.

    Returns:
        None
    """
    for user in ADMINS:
        await bot.send_message(user, 'Bot is online!')
    logging.info('Bot is online')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
