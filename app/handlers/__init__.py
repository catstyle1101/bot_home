__all__ = ("router", "on_shutdown", "make_on_startup")
from aiogram import Router

from .callback_query_handlers import router as callback_router
from .commands_handlers import router as commands_router
from .common_handlers import router as common_router
from .magnet_download_handler import router as magnet_download_router
from .find_torrent_handler import router as find_torrent_router
from .find_torrent_settings_handler import router as find_torrent_settings_router
from .on_shutdown import on_shutdown
from .on_startup import make_on_startup

router = Router(name=__name__)

router.include_routers(
    commands_router,
    find_torrent_router,
    callback_router,
    find_torrent_settings_router,
    magnet_download_router,
)
# This must be the last one!
router.include_router(common_router)
