from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import settings


class NavigateFindTorrentsCb(CallbackData, prefix="NavFT"):
    offset: int
    query: str


def torrent_find_kb(query: str, current_offset: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    prev_offset = max(0, current_offset - settings.FIND_TORRENTS_LIMIT)
    next_offset = current_offset + settings.FIND_TORRENTS_LIMIT
    builder.add(
        InlineKeyboardButton(
            text="◀️",
            callback_data=NavigateFindTorrentsCb(
                offset=prev_offset, query=query
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text=f"{current_offset}-{next_offset}",
            callback_data=f"{current_offset}-{next_offset}",
        ),
    )
    builder.add(
        InlineKeyboardButton(
            text="▶️",
            callback_data=NavigateFindTorrentsCb(
                offset=next_offset, query=query
            ).pack(),
        )
    )
    builder.adjust(3)
    return builder.as_markup()
