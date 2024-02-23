from enum import StrEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import settings


class TrackerListAction(StrEnum):
    delete = auto()
    add = auto()


class TrackerCb(CallbackData, prefix="list_of_trackers"):
    tracker: str
    action: TrackerListAction


def torrent_settings_kb(trackers):
    builder = InlineKeyboardBuilder()
    for tracker in trackers:
        if tracker in settings.FIND_TORRENTS_TRACKERS:
            text = f"{tracker.capitalize()} ✅"
            callback = TrackerCb(tracker=tracker, action=TrackerListAction.delete)
        else:
            text = f"{tracker.capitalize()} ❌"
            callback = TrackerCb(tracker=tracker, action=TrackerListAction.add)
        builder.add(InlineKeyboardButton(text=text, callback_data=callback.pack()))
    builder.adjust(1)
    return builder.as_markup()
