import logging

from aiogram import Router, F, types

from enums import MessageType
from keyboards import (
    Action,
    StartMenuCallbackData,
    generate_torrent_keyboard,
    generate_del_torrent_kb,
    NavigateTorrentsListCallbackData,
    TorrentDelConfirmCallbackData,
    TorrentsListKeyboardCallbackData,
    DeleteActionEnum,
)
from provider.protocols import Downloader, TorrentsCache
from utils import render_message

router = Router(name=__name__)

logger = logging.getLogger(__name__)


@router.callback_query(
    StartMenuCallbackData.filter(F.action == Action.downloaded_torrents)
)
async def downloaded_torrents(
    callback_query: types.CallbackQuery,
    downloader: Downloader,
    cache: TorrentsCache,
) -> None:
    await callback_query.answer()
    torrents = cache.get_torrents()
    if not torrents:
        torrents = downloader.get_downloaded_torrents()
        cache.set_torrents(torrents)
    if getattr(callback_query, "message", None) and isinstance(
        callback_query.message, types.Message
    ):
        await callback_query.message.edit_text(
            text=(
                "Список скачанных торрентов:" if torrents else "Ничего не скачано еще."
            ),
            reply_markup=(
                generate_torrent_keyboard(
                    torrents=torrents,
                )
                if torrents
                else None
            ),
        )


@router.callback_query(NavigateTorrentsListCallbackData.filter())
async def navigate_torrents(
    callback_query: types.CallbackQuery,
    callback_data: NavigateTorrentsListCallbackData,
    downloader: Downloader,
    cache: TorrentsCache,
) -> None:
    await callback_query.answer()
    torrents = cache.get_torrents()
    if not torrents:
        torrents = downloader.get_downloaded_torrents()
    if getattr(callback_query, "message", None) and isinstance(
        callback_query.message, types.Message
    ):
        await callback_query.message.edit_reply_markup(
            reply_markup=generate_torrent_keyboard(
                torrents=torrents,
                page=callback_data.page,
            ),
        )


@router.callback_query(TorrentsListKeyboardCallbackData.filter())
async def delete_torrent_page(
    callback_query: types.CallbackQuery,
    callback_data: TorrentDelConfirmCallbackData,
    downloader: Downloader,
) -> None:
    torrent = downloader.get_torrent_by_id(callback_data.torrent_id)
    message = render_message(
        template_name=MessageType.delete_torrent,
        torrent=torrent,
    )
    await callback_query.answer()
    if getattr(callback_query, "message", None) and isinstance(
        callback_query.message, types.Message
    ):
        await callback_query.message.edit_text(
            text=message, reply_markup=generate_del_torrent_kb(callback_data.torrent_id)
        )


@router.callback_query(
    TorrentDelConfirmCallbackData.filter(F.action == DeleteActionEnum.delete)
)
async def delete_torrent(
    callback_query: types.CallbackQuery,
    callback_data: TorrentDelConfirmCallbackData,
    downloader: Downloader,
    cache: TorrentsCache,
) -> None:
    torrent = downloader.get_torrent_by_id(callback_data.torrent_id)
    is_deleted = downloader.delete_torrent_by_id(callback_data.torrent_id)
    message = render_message(
        MessageType.confirm_delete_message,
        torrent_name=torrent.name,
        is_deleted=is_deleted,
    )
    await callback_query.answer(text=message, show_alert=True)
    torrents = downloader.get_downloaded_torrents()
    cache.set_torrents(torrents)
    if getattr(callback_query, "message", None) and isinstance(
        callback_query.message, types.Message
    ):
        await callback_query.message.edit_text(
            text=message, reply_markup=generate_torrent_keyboard(torrents=torrents)
        )


@router.callback_query(
    TorrentDelConfirmCallbackData.filter(F.action == DeleteActionEnum.no_delete)
)
async def no_delete_torrent(
    callback_query: types.CallbackQuery,
    callback_data: TorrentDelConfirmCallbackData,
    downloader: Downloader,
    cache: TorrentsCache,
) -> None:
    await callback_query.answer()
    torrent = downloader.get_torrent_by_id(callback_data.torrent_id)
    message = render_message(
        MessageType.confirm_delete_message,
        torrent=torrent,
        is_deleted=False,
    )
    torrents = cache.get_torrents()
    if not torrents:
        torrents = downloader.get_downloaded_torrents()
        cache.set_torrents(torrents)
    if not isinstance(callback_query.message, types.Message):
        return None
    await callback_query.message.edit_text(
        text=message,
        reply_markup=generate_torrent_keyboard(torrents=torrents),
    )
