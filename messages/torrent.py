from torrent_api.data_formatter import TorrentFormatter


def format_torrent(torrent: TorrentFormatter, short: bool = False) -> str:
    result = f"• {torrent.title}\n"
    if not short:
        result += (
            f"size: ({torrent.size}); "
            f"S/L({torrent.seeders}/{torrent.leechers}); "
            f"downloads: {torrent.downloads}"
            f"\n/link_{torrent.magnet_key}\n\n"
        )
    return result
