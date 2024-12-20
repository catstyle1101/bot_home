from datetime import datetime
from typing import Final

from .schemas import Torrent

SECONDS_IN_MINUTE: Final[int] = 60


class MemCache:
    _torrents: list[Torrent] = []
    _expires_at: int | float | None = None
    _instance: "MemCache | None" = None

    def __new__(cls) -> "MemCache":
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, expire_minutes: int = 10):
        self.expire_minutes = expire_minutes

    def get_torrents(self) -> list[Torrent] | None:
        now = datetime.now().timestamp()
        if self._expires_at is None or now > self._expires_at:
            self._torrents = []
        return self._torrents

    def set_torrents(self, torrents: list[Torrent]) -> None:
        self._expires_at = int(
            datetime.now().timestamp() + self.expire_minutes * SECONDS_IN_MINUTE
        )
        self._torrents = torrents
