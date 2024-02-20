from aiogram import Router, F, types

from enums import MessageType
from keyboards import start_menu_kb
from middlewares import IsAdminMiddleware
from transmission_client import TransmissionClient
from utils import render_message

router = Router(name=__name__)
router.message.middleware(IsAdminMiddleware())


@router.message(F.text.startswith("magnet:"))
async def magnet_download(message: types.Message, is_admin: bool):
    transmission = TransmissionClient()
    result = transmission.add_torrent(link=message.text)
    reply_message = render_message(
        MessageType.download_magnet,
        result=result,
        is_admin=is_admin,
    )
    await message.reply(text=reply_message, reply_markup=start_menu_kb())
