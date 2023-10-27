#!/home/ubuntu/bot/env/ python
import logging
import sys

from aiogram.utils import executor

from config import settings
from create_bot import bot, dp
import handlers # noqa

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
    for user in settings.ALLOWED_USERS:
        await bot.send_message(user, 'Bot is online!')
    logging.info('Bot is online')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
