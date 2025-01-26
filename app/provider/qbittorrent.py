import logging

from qbittorrent import Client  # type: ignore

from provider.schemas import Torrent
from config import settings

logger = logging.getLogger(__name__)


class QBittorrent:
    def __init__(self) -> None:
        try:
            self.client = Client(settings.QBITTORRENT.HOST)
            self.client.login(settings.QBITTORRENT.LOGIN, settings.QBITTORRENT.PASSWORD)
        except Exception as e:
            raise e

    def login(self) -> None:
        try:
            self.client.login(settings.QBITTORRENT.LOGIN, settings.QBITTORRENT.PASSWORD)
        except Exception as e:
            raise e

    def get_downloaded_torrents(self) -> list[Torrent]:
        self.login()
        torrents = self.client.torrents()
        logger.debug(torrents)
        torrents = [
            Torrent(
                id=(i["infohash_v1"] or i["infohash_v2"]),
                name=i["name"],
                size=i["total_size"],
                category=i["category"],
                comment=i["comment"],
                magnet_uri=i["magnet_uri"],
            )
            for i in torrents
        ]
        logger.info("List of parsed downloaded torrents: %s", torrents)
        return sorted(torrents, key=lambda t: t.name)

    def get_torrent_by_id(self, torrent_id: str) -> Torrent | None:
        self.login()
        torrents = self.get_downloaded_torrents()
        for torrent in torrents:
            if torrent.id == torrent_id:
                return torrent
        return None

    def add_torrent(
        self,
        magnet_link: str,
        **kwargs: dict[str, str],
    ) -> bool:
        self.login()
        magnet_link = magnet_link.strip()
        if "," in magnet_link:
            magnet_links = magnet_link.split(",")
        elif "\n" in magnet_link:
            magnet_links = magnet_link.split("\n")
        else:
            magnet_links = [magnet_link]
        return str(self.client.download_from_link(magnet_links, **kwargs)) == "Ok."

    def delete_torrent_by_id(self, torrent_id: str) -> None:
        self.login()
        self.client.delete_permanently(torrent_id)
