import logging
from typing import Callable, Any, Coroutine

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from config import settings


def make_on_startup(
    dp: Dispatcher, bot: Bot
) -> Callable[[Bot], Coroutine[Any, Any, None]]:
    async def inner(bot: Bot) -> None:
        logger = logging.getLogger(__name__)
        res = await bot.set_webhook(
            f"https://{settings.DOMAIN}{settings.WEBHOOK.PATH}",
            secret_token=settings.WEBHOOK.SECRET,
            drop_pending_updates=True,
            allowed_updates=dp.resolve_used_update_types(),
        )
        if res:
            logger.info("Webhook installed successfully")
            for admin_id in settings.ADMIN_LIST:
                try:
                    await bot.send_message(chat_id=admin_id, text="Bot is online!")
                    logger.info(f"Message to admin {admin_id} was sent.")
                except Exception as e:
                    logger.warning(f"'{e}' was occurred, chat id is {admin_id}.")
        else:
            logger.error("Webhook was not installed")

        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Начало работы с ботом."),
                BotCommand(command="help", description="Бот домашний помощник."),
            ],
            scope=BotCommandScopeAllPrivateChats(),
        )

    return inner
