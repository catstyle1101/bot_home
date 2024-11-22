from dataclasses import dataclass


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


def format_data(data: dict[str, str | int]) -> TorrentFormatter:
    """
    Format the given data into a TorrentFormatter object.

    Parameters:
    - data (json): The data to be formatted.

    Returns:
    - TorrentFormatter: The formatted data as a TorrentFormatter object.
    """
    return TorrentFormatter(
        title=str(data["title"]),
        magnet_key=str(data["magnet_key"]),
        size=str(data["size"]),
        downloads=int(data["downloads"]),
        seeders=int(data["seeders"]),
        leechers=int(data["leechers"]),
        rank=int(data["rank"]),
        tracker=str(data["tracker"]),
    )
