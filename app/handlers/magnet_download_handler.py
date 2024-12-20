import logging

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from enums import MessageType, ErrorMessage
from keyboards import (
    torrent_group_kb,
    TorrentsGroup,
    TorrentsGroupCallbackData,
    start_menu_kb,
)
from middlewares import IsAdminMiddleware
from provider.protocols import Downloader

from utils import render_message

router = Router(name=__name__)
router.message.middleware(IsAdminMiddleware())

logger = logging.getLogger(__name__)


class FSMDownloadMagnet(StatesGroup):
    magnet_link = State()


@router.message(F.text.startswith("magnet:"))
async def magnet_download(
    message: types.Message,
    state: FSMContext,
    is_admin: bool,
    downloader: Downloader,
) -> None:
    if not message.text:
        await state.clear()
        return None
    await state.set_state(FSMDownloadMagnet.magnet_link)
    await state.update_data(magnet_link=message.text)
    reply_message = render_message(
        MessageType.select_group,
    )
    await message.reply(
        text=reply_message,
        reply_markup=torrent_group_kb(),
    )


@router.callback_query(
    TorrentsGroupCallbackData.filter(),
)
async def magnet_download_group(
    callback_query: types.CallbackQuery,
    callback_data: TorrentsGroupCallbackData,
    state: FSMContext,
    downloader: Downloader,
) -> None:
    if callback_data.group is TorrentsGroup.cancel:
        await callback_query.answer()
        await state.clear()
        if callback_query.message and isinstance(callback_query.message, types.Message):
            await callback_query.message.edit_text(
                text=ErrorMessage.magnet_not_added_to_download,
                reply_markup=start_menu_kb(),
            )
        return
    data = await state.get_data()
    magnet_link = data.get("magnet_link")
    if magnet_link == TorrentsGroup.cancel:
        magnet_link = ""
    result = downloader.add_torrent(
        magnet_link=str(magnet_link),
        category=callback_data.group,
    )
    logger.debug("%r", result)
    reply_message = render_message(
        MessageType.download_magnet,
        result=result,
    )
    await callback_query.answer(text=reply_message)
    await state.clear()
    start_message = render_message(
        MessageType.download_magnet,
        name=callback_query.from_user.full_name,
        is_admin=True,
    )
    if callback_query.message and isinstance(callback_query.message, types.Message):
        await callback_query.message.edit_text(
            text=start_message,
            reply_markup=start_menu_kb(),
        )
