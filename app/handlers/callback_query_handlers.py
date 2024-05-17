import logging
from datetime import datetime

from aiogram import Router, F, types
from transmission_rpc import Torrent

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
from transmission_client import TransmissionClient
from utils import render_message

router = Router(name=__name__)

logger = logging.getLogger(__name__)

MINUTES = 60


class Cache:
    _torrents: list | None = []
    _expires_at: int | float | None = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def get_torrents(self) -> list[Torrent] | None:
        now = datetime.now().timestamp()
        if self._expires_at is None or now > self._expires_at:
            return None
        return self._torrents

    def set_torrents(self, torrents: list[Torrent]) -> None:
        self._expires_at = datetime.now().timestamp() + 10 * MINUTES
        self._torrents = torrents


@router.callback_query(
    StartMenuCallbackData.filter(F.action == Action.downloaded_torrents)
)
async def downloaded_torrents(callback_query: types.CallbackQuery):
    await callback_query.answer()
    cache = Cache()
    torrents = cache.get_torrents()
    if torrents is None:
        transmission = TransmissionClient()
        torrents = transmission.get_downloaded_torrents()
        cache.set_torrents(torrents)
    await callback_query.message.edit_text(
        text="Список скачанных торрентов:" if torrents else "Ничего не скачано еще.",
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
):
    await callback_query.answer()
    cache = Cache()
    torrents = cache.get_torrents()
    if torrents is None:
        transmission = TransmissionClient()
        torrents = transmission.get_downloaded_torrents()
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
):
    transmission = TransmissionClient()
    torrent_name = transmission.get_torrent_name(callback_data.torrent_id)
    message = render_message(
        template_name=MessageType.delete_torrent,
        torrent_name=torrent_name,
    )
    await callback_query.answer()
    await callback_query.message.edit_text(
        text=message,
        reply_markup=generate_del_torrent_kb(callback_data.torrent_id)
    )


@router.callback_query(
    TorrentDelConfirmCallbackData.filter(F.action == DeleteActionEnum.delete)
)
async def delete_torrent(
    callback_query: types.CallbackQuery,
    callback_data: TorrentDelConfirmCallbackData,
):
    transmission = TransmissionClient()
    torrent_name = transmission.get_torrent_name(callback_data.torrent_id)
    transmission = TransmissionClient()
    is_deleted = transmission.del_torrent(index=callback_data.torrent_id)
    message = render_message(
        MessageType.confirm_delete_message,
        torrent_name=torrent_name,
        is_deleted=is_deleted,
    )
    await callback_query.answer(text=message, show_alert=True)
    torrents = transmission.get_downloaded_torrents()
    cache = Cache()
    cache.set_torrents(torrents)
    await callback_query.message.edit_text(
        text=message,
        reply_markup=generate_torrent_keyboard(torrents=torrents)
    )


@router.callback_query(
    TorrentDelConfirmCallbackData.filter(F.action == DeleteActionEnum.no_delete)
)
async def no_delete_torrent(
    callback_query: types.CallbackQuery,
    callback_data: TorrentDelConfirmCallbackData,
):
    await callback_query.answer()
    transmission = TransmissionClient()
    torrent_name = transmission.get_torrent_name(callback_data.torrent_id)
    message = render_message(
        MessageType.confirm_delete_message,
        torrent_name=torrent_name,
        is_deleted=False,
    )
    cache = Cache()
    torrents = cache.get_torrents()
    if torrents is None:
        transmission = TransmissionClient()
        torrents = transmission.get_downloaded_torrents()
        cache.set_torrents(torrents)
    await callback_query.message.edit_text(
        text=message,
        reply_markup=generate_torrent_keyboard(torrents=torrents),
    )
