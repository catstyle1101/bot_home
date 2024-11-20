import logging
from datetime import datetime

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from config import settings
from enums import MessageType, ErrorMessage
from keyboards import (
    StartMenuCallbackData,
    Action,
    torrent_find_kb,
    NavigateFindTorrentsCb,
    start_menu_kb,
)
from torrent_api.fetch import make_magnet_link, scrap_torrents

# from transmission_client import TransmissionClient
from utils import render_message, prepare_message

router = Router(name=__name__)


class TorrentsCache:
    torrents = None
    timestamp = 0


class FSMFindTorrents(StatesGroup):
    title = State()


@router.callback_query(
    StartMenuCallbackData.filter(F.action == Action.find),
)
async def find_title(callback: types.CallbackQuery, state: FSMContext):
    """
    A callback query handler that handles the 'menu_find' text.
    It sets the FSMFindTorrents.title state and sends a message
    to the callback's message with the text 'Скинь название торрента'.

    Parameters:
    - callback: A types.CallbackQuery object representing the callback query.

    Returns:
    - None
    """
    await callback.answer()
    await state.set_state(FSMFindTorrents.title)
    await callback.message.answer("Скинь название торрента")


@router.message(FSMFindTorrents.title)
async def show_torrents(message: types.Message, state: FSMContext):
    """
    This function is a message handler for the FSMFindTorrents state.
    It takes in a message and a state context as parameters.
    The function retrieves the 'title' from the state context and uses
    it to scrape torrents. It then formats the torrents and sends them as
    a reply to the original message. Finally, it finishes the state context.

    Parameters:
    - message: A types.Message object representing the message received.
    - state: A FSMContext object representing the state context.

    Returns:
    - None
    """
    await state.update_data(title=message.text)

    torrents = await scrap_torrents(query=message.text)
    if torrents:
        TorrentsCache.torrents = torrents
        TorrentsCache.timestamp = datetime.now().timestamp() + 60 * 10
        answer = render_message(
            MessageType.format_find_torrent,
            torrents=[i for i in torrents.values()],
            is_short=False,
        )
        answer_messages = prepare_message(message=answer, delimiter=" ..")
        for idx, reply_message in enumerate(answer_messages, 1):
            if idx == len(answer_messages):
                try:
                    await message.reply(
                        reply_message,
                        reply_markup=torrent_find_kb(
                            query=message.text,
                        ),
                    )
                except ValueError as e:
                    logging.error(e)
                    await message.reply(reply_message)
            else:
                await message.reply(reply_message)
    else:
        answer = render_message(MessageType.nothing_found)
        await message.reply(text=answer)
    await state.clear()


@router.callback_query(NavigateFindTorrentsCb.filter())
async def navigate_find_torrents(
    callback_query: CallbackQuery,
    callback_data: NavigateFindTorrentsCb,
) -> None:
    await callback_query.answer()
    try:
        torrents = await scrap_torrents(
            query=callback_data.query, offset=callback_data.offset
        )
        TorrentsCache.torrents = torrents
        TorrentsCache.timestamp = datetime.now().timestamp() * 60 * 10
        if torrents:
            answer = render_message(
                MessageType.format_find_torrent,
                torrents=[i for i in torrents.values()],
                is_short=False,
            )
            answer_messages = prepare_message(message=answer, delimiter=" ..")
            await callback_query.message.edit_text(
                text=answer_messages[0],
                reply_markup=torrent_find_kb(
                    query=callback_data.query,
                    current_offset=callback_data.offset,
                ),
            )
    except Exception:
        await callback_query.message.edit_text(
            text=ErrorMessage.api_not_found,
            reply_markup=start_menu_kb(),
        )


# @router.message(F.text.startswith("/link_"))
# async def download_torrent(message: types.Message):
#     """
#     Handles the download of a torrent based on a message.
#
#     Args:
#     - message (types.Message): The message object containing the command.
#
#     Returns:
#     - None
#     """
#     if (
#         TorrentsCache.torrents is None
#         or datetime.now().timestamp() > TorrentsCache.timestamp
#     ):
#         TorrentsCache.timestamp = datetime.now().timestamp()
#         await message.answer("Сделай поиск заново, ссылки устарели")
#         return
#
#     magnet_key = message.text.split("_")[1]
#     torrent = await make_magnet_link(TorrentsCache.torrents.get(magnet_key))
#     if torrent is None:
#         await message.answer("Сделай поиск заново, ссылки устарели")
#
#     if torrent.magnet_link.startswith("magnet"):
#         if message.from_user.id in settings.ADMINS:
#             client = TransmissionClient()
#             client.add_torrent(torrent.magnet_link)
#             await message.answer("Закачка добавлена")
#
#         answer = render_message(
#             MessageType.format_find_torrent,
#             torrents=[torrent],
#             is_short=True,
#         )
#         await message.answer(text=answer)
#         await message.answer(torrent.magnet_link)
