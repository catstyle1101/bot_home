from typing import Protocol

from .schemas import Torrent


class Downloader(Protocol):
    def get_downloaded_torrents(self) -> list[Torrent]: ...

    def get_torrent_by_id(self, torrent_id: str | int) -> Torrent: ...

    def delete_torrent_by_id(self, torrent_id: str | int) -> bool: ...

    def add_torrent(
        self,
        magnet_link: str,
        name: str = "",
        category: str = "",
        comment: str = "",
    ) -> bool: ...


class Cache(Protocol):
    _torrents: list[Torrent] = []
    _expires_at: int | float | None = None

    def get_torrents(self) -> list[Torrent]: ...

    def set_torrents(self, torrents: list[Torrent]) -> None: ...
