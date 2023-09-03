import aiohttp
import json

from torrent_api.data_formatter import format_data, TorrentFormatter


def session_maker():
    session = aiohttp.ClientSession(
        base_url='https://api.freedomist.ru')
    return session


async def fetch_url(
        url: str,
        query: str,
        trackers: list[str] = ["nnmclub"],
        order_by: str = 's',
        filter_by_size: str = '',
        limit: int = 20,
        offset: int = 0,
        full_match: bool = True,
        token: str = ''
) -> json:
    data = {
        "query": query,
        "trackers": trackers,
        "order_by": order_by,
        "filter_by_size": filter_by_size,
        "limit": limit,
        "offset": offset,
        "full_match": full_match,
        "token": token,
    }
    async with session_maker() as session:
        async with session.post(url, json=data, ssl=False) as response:
            return json.loads(await response.text())


async def scrap_torrents(query: str) -> dict[str, TorrentFormatter]:
    raw_data = await fetch_url('/search', query=query)
    data = {i['magnet_key']: format_data(i) for i in raw_data['data']}
    return data


async def make_magnet_link(torrent: TorrentFormatter):
    async with session_maker() as session:
        async with session.get(
            f'/magnet/{torrent.magnet_key}', ssl=False
        ) as response:
            res = await response.text()
            res = json.loads(res)
            if res['status_code'] == 200:
                torrent.magnet_link = res['data']['magnet_link']
    return torrent
