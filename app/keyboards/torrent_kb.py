import itertools
from enum import StrEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from provider.schemas import Torrent

from config import settings


class DeleteActionEnum(StrEnum):
    delete = auto()
    no_delete = auto()


class TorrentsListKeyboardCallbackData(CallbackData, prefix="del_list_torrents"):
    torrent_id: int | str | None


class TorrentDelConfirmCallbackData(CallbackData, prefix="del_t_conf"):
    torrent_id: int | str
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
    torrents_list = list(itertools.batched(torrents, n=page_size))
    for torrent in torrents_list[page]:
        builder.button(
            text=f"{torrent.name} {torrent.str_size}",
            callback_data=TorrentsListKeyboardCallbackData(
                torrent_id=torrent.id
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


def generate_del_torrent_kb(torrent_id: int | str) -> InlineKeyboardMarkup:
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
