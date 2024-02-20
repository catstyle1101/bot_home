import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from config import settings


async def on_startup(bot: Bot) -> None:
    logger = logging.getLogger(__name__)
    res = await bot.set_webhook(
        f"https://{settings.DOMAIN}{settings.WEBHOOK_PATH}",
        secret_token=settings.WEBHOOK_SECRET,
        drop_pending_updates=True,
        allowed_updates=["message", "sticker", "callback_query", "edited_message"]

    )
    if res:
        logger.info("Webhook installed successfully")
        for admin_id in settings.ADMINS:
            try:
                await bot.send_message(chat_id=admin_id, text="Bot is online!")
                logger.info(f"Message to admin {admin_id} was sent.")
            except Exception as e:
                logger.warning(f"'{e}' was occurred, chat id is {admin_id}.")
    else:
        logger.error("Webhook was not installed")

    await bot.set_my_commands(
        [
            BotCommand(
                command="start",
                description="Начало работы с ботом."
            ),
            BotCommand(
                command="help",
                description="Бот домашний помощник."
            )
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )


async def on_shutdown(bot: Bot) -> None:
    logger = logging.getLogger(__name__)
    res = await bot.delete_webhook()
    if res:
        logger.info("Webhook deleted successfully")
