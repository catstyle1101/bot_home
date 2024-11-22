import logging

from aiogram import Router, F, types

from enums import MessageType, ErrorMessage
from keyboards import start_menu_kb
from middlewares import IsAdminMiddleware
from provider.protocols import Downloader

from utils import render_message

router = Router(name=__name__)
router.message.middleware(IsAdminMiddleware())

logger = logging.getLogger(__name__)


@router.message(F.text.startswith("magnet:"))
async def magnet_download(
    message: types.Message,
    is_admin: bool,
    downloader: Downloader,
) -> None:
    if not message.text:
        return None
    result = downloader.add_torrent(message.text)
    logger.debug(repr(result))
    if result:
        reply_message = render_message(
            MessageType.download_magnet,
            result=result,
            is_admin=is_admin,
        )
        await message.reply(text=reply_message, reply_markup=start_menu_kb())
    else:
        await message.reply(text=ErrorMessage.magnet_not_added_to_download)
