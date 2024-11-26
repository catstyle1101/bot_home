from aiogram.client.default import DefaultBotProperties
from aiohttp import web
import ssl

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers import router, on_shutdown, make_on_startup
from config import settings
from logger_config import configure_logger
from provider.qbittorrent import QBittorrent
from provider.memcache import MemCache


def main() -> None:
    configure_logger()

    bot = Bot(
        settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_router(router)

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

    on_startup = make_on_startup(dp, bot)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

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
    main()
