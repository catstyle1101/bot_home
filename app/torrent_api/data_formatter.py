from dataclasses import dataclass
import datetime
import json


@dataclass
class TorrentFormatter:
    title: str
    magnet_key: str
    size: str
    rank: int
    tracker: str
    downloads: int
    seeders: int
    leechers: int
    magnet_link: str = ""


def format_data(data: json) -> TorrentFormatter:
    """
    Format the given data into a TorrentFormatter object.

    Parameters:
    - data (json): The data to be formatted.

    Returns:
    - TorrentFormatter: The formatted data as a TorrentFormatter object.
    """
    return TorrentFormatter(
        title=data["title"],
        magnet_key=data["magnet_key"],
        size=data["size"],
        downloads=data["downloads"],
        seeders=int(data["seeders"]),
        leechers=int(data["leechers"]),
        rank=int(data["rank"]),
        tracker=data["tracker"],
    )
