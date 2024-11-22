from enum import auto, IntEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Action(IntEnum):
    find = auto()
    downloaded_torrents = auto()


class StartMenuCallbackData(CallbackData, prefix="start_menu"):
    action: Action


def start_menu_kb(*, is_admin: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔎  Найти",
        callback_data=StartMenuCallbackData(action=Action.find).pack(),
    )
    if is_admin:
        builder.button(
            text="📂 Скачанные торренты",
            callback_data=StartMenuCallbackData(
                action=Action.downloaded_torrents
            ).pack(),
        )
    builder.adjust(1)
    return builder.as_markup()
