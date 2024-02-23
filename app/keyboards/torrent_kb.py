import itertools
from enum import StrEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from transmission_rpc import Torrent

from config import settings


class DeleteActionEnum(StrEnum):
    delete = auto()
    no_delete = auto()


class TorrentsListKeyboardCallbackData(CallbackData, prefix="del_list_torrents"):
    torrent_id: int


class TorrentDelConfirmCallbackData(CallbackData, prefix="delete_torrent_confirm"):
    torrent_id: int
    action: DeleteActionEnum


class NavigateTorrentsListCallbackData(CallbackData, prefix="navigate_torrents"):
    page: int


def generate_torrent_keyboard(
    torrents: list[Torrent],
    page: int = 0,
    page_size: int = settings.SHOW_TORRENTS_PAGE_SIZE,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    count_pages = len(torrents) // page_size + 1
    torrents = list(itertools.batched(torrents, n=page_size))
    for torrent in torrents[page]:
        builder.button(
            text=f"{torrent[1]} {torrent[2]}",
            callback_data=TorrentsListKeyboardCallbackData(
                torrent_id=torrent[0]
            ).pack(),
        )
    builder.adjust(1)

    next_page = page + 1 if page < count_pages - 1 else 0
    prev_page = page - 1 if page > 0 else count_pages - 1

    builder.row(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=NavigateTorrentsListCallbackData(
                page=prev_page,
            ).pack(),
        ),
        InlineKeyboardButton(
            text=f"Страница {page + 1}/{count_pages}",
            callback_data=f"Страница {page + 1}",
        ),
        InlineKeyboardButton(
            text="➡️",
            callback_data=NavigateTorrentsListCallbackData(
                page=next_page,
            ).pack(),
        ),
        width=3,
    )
    return builder.as_markup()


def generate_del_torrent_kb(torrent_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="Да",
            callback_data=TorrentDelConfirmCallbackData(
                action=DeleteActionEnum.delete,
                torrent_id=torrent_id,
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=TorrentDelConfirmCallbackData(
                action=DeleteActionEnum.no_delete,
                torrent_id=torrent_id,
            ).pack(),
        ),
    )
    builder.adjust(2)
    return builder.as_markup()
