import atexit
import logging.config

from aiohttp import web
import ssl
import yaml

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers import router
from config import settings
from utils import on_startup, on_shutdown


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    bot = Bot(settings.BOT_TOKEN, parse_mode=ParseMode.HTML)


    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=settings.WEB_SERVER_HOST, port=settings.WEB_SERVER_PORT)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(settings.WEBHOOK_SSL_CERT, settings.WEBHOOK_SSL_PRIV)

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
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
    logger = logging.getLogger(__name__)
    logger.info("Starting...")
    main()
