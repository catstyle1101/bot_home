import logging

from aiogram import Bot


async def on_shutdown(bot: Bot) -> None:
    logger = logging.getLogger(__name__)
    res = await bot.delete_webhook()
    if res:
        logger.info("Webhook deleted successfully")
