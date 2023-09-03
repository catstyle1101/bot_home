from dataclasses import dataclass
import datetime
import json


@dataclass
class TorrentFormatter:
    title: str
    magnet_key: str
    size: str
    post_datetime: datetime
    rank: int
    tracker: str
    downloads: int
    seeders: int
    leechers: int
    magnet_link: str = ''


def format_data(data: json) -> TorrentFormatter:
    return TorrentFormatter(
        title=data['title'],
        magnet_key=data['magnet_key'],
        size=data['size'],
        downloads=data['downloads'],
        post_datetime=datetime.datetime.strptime(
            data['post_datetime'], '%Y-%m-%d %H:%M:%S'),
        seeders=int(data['seeders']),
        leechers=int(data['leechers']),
        rank=int(data['rank']),
        tracker=data['tracker'],
    )
