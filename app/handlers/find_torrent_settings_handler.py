from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import Command

from config import settings
from enums import MessageType
from keyboards import torrent_settings_kb, TrackerCb, TrackerListAction
from middlewares import IsAdminMiddleware
from torrent_api.fetch import list_of_trackers
from utils import render_message

router = Router(name=__name__)
router.message.middleware(IsAdminMiddleware())


HOURS = 60 * 60


class TrackersCache:
    _trackers: list[str] | None = []
    _expires_at: int | float | None = None
    _instance = None

    def __new__(cls) -> "TrackersCache":
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def get(self) -> list[str] | None:
        now = datetime.now().timestamp()
        if self._expires_at is None or now > self._expires_at:
            return None
        return self._trackers

    def set(self, trackers: list[str]) -> None:
        self._expires_at = datetime.now().timestamp() + 24 * HOURS
        self._trackers = trackers


@router.message(Command("torrent_settings"))
async def torrent_settings_handler(message: types.Message) -> None:
    answer = render_message(MessageType.torrent_settings)
    trackers_cache = TrackersCache()
    trackers = trackers_cache.get()
    if trackers is None:
        trackers = await list_of_trackers()
        trackers_cache.set(trackers)
    await message.reply(answer, reply_markup=torrent_settings_kb(trackers=trackers))


@router.callback_query(TrackerCb.filter(F.action == TrackerListAction.add))
async def add_tracker(
    callback_query: types.CallbackQuery, callback_data: TrackerCb
) -> None:
    settings.FIND_TORRENTS_TRACKERS.append(callback_data.tracker)
    trackers_cache = TrackersCache()
    trackers = trackers_cache.get()
    if trackers is None:
        trackers = await list_of_trackers()
        trackers_cache.set(trackers)
    if not isinstance(callback_query, types.Message):
        return None
    await callback_query.message.edit_reply_markup(
        reply_markup=torrent_settings_kb(trackers=trackers)
    )


@router.callback_query(TrackerCb.filter(F.action == TrackerListAction.delete))
async def del_tracker(
    callback_query: types.CallbackQuery, callback_data: TrackerCb
) -> None:
    settings.FIND_TORRENTS_TRACKERS = [
        i for i in settings.FIND_TORRENTS_TRACKERS if i != callback_data.tracker
    ]
    trackers_cache = TrackersCache()
    trackers = trackers_cache.get()
    if trackers is None:
        trackers = await list_of_trackers()
        trackers_cache.set(trackers)
    if not isinstance(callback_query, types.Message):
        return None
    await callback_query.message.edit_reply_markup(
        reply_markup=torrent_settings_kb(trackers=trackers)
    )
