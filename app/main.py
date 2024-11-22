import atexit
import logging.config

from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from aiohttp import web
import ssl
import yaml

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers import router
from config import settings
from provider.qbittorrent import QBittorrent
from provider.memcache import Cache as MemCache


def main() -> None:
    dp = Dispatcher()

    async def on_startup(bot: Bot) -> None:
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

    async def on_shutdown(bot: Bot) -> None:
        logger = logging.getLogger(__name__)
        res = await bot.delete_webhook()
        if res:
            logger.info("Webhook deleted successfully")

    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    bot = Bot(
        settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK.SECRET,
        downloader=QBittorrent(),
        cache=MemCache(),
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK.PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=settings.WEB_SERVER_HOST, port=settings.WEB_SERVER_PORT)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(settings.WEBHOOK.SSL_CERT, settings.WEBHOOK.SSL_PRIV)

    web.run_app(
        app,
        host=settings.WEB_SERVER_HOST,
        port=settings.WEB_SERVER_PORT,
        ssl_context=context,
    )


if __name__ == "__main__":
    with open("logging_config.yml", "r", encoding="utf-8") as file:
        logging_config = yaml.safe_load(file)
    logging.config.dictConfig(logging_config)
    if settings.DEBUG:
        logger = logging.getLogger(__name__)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler and hasattr(queue_handler, "listener"):
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
    logger = logging.getLogger(__name__)
    logger.info("Starting...")
    main()
