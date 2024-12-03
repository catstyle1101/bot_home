from enum import StrEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class TorrentsGroup(StrEnum):
    films = auto()
    series = auto()
    children = auto()
    cancel = auto()
    empty = "Без группы"


class TorrentsGroupCallbackData(CallbackData, prefix="TorrentsGroup"):
    group: TorrentsGroup


def torrent_group_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for group in TorrentsGroup:
        builder.row(
            InlineKeyboardButton(
                text=group,
                callback_data=TorrentsGroupCallbackData(
                    group=group,
                ).pack(),
            )
        )
    # builder.row(
    #     InlineKeyboardButton(
    #         text=TorrentsGroup.series,
    #         callback_data=TorrentsGroupCallbackData(
    #             group=TorrentsGroup.series,
    #         ).pack(),
    #     )
    # )
    # builder.row(
    #     InlineKeyboardButton(
    #         text=TorrentsGroup.children,
    #         callback_data=TorrentsGroupCallbackData(
    #             group=TorrentsGroup.children,
    #         ).pack(),
    #     )
    # )
    # builder.row(
    #     InlineKeyboardButton(
    #         text=TorrentsGroup.cancel,
    #         callback_data=TorrentsGroupCallbackData(
    #             group=TorrentsGroup.cancel,
    #         ).pack(),
    #     )
    # )
    return builder.as_markup()
