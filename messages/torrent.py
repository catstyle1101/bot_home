from torrent_api.data_formatter import TorrentFormatter


def format_torrent(torrent: TorrentFormatter, short: bool = False) -> str:
    """
    Formats a torrent object into a string representation.

    Args:
    - torrent (TorrentFormatter): The torrent object to format.
    - short (bool, optional): If True, only the torrent title is included
        in the result. Defaults to False.

    Returns:
    - str: The formatted torrent string.
    """
    result = f"• {torrent.title}\n"
    if not short:
        result += (
            f"size: ({torrent.size}); "
            f"S/L({torrent.seeders}/{torrent.leechers}); "
            f"downloads: {torrent.downloads}"
            f"\n/link_{torrent.magnet_key}\n\n"
        )
    return result
