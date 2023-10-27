import aiohttp
import json

from torrent_api.data_formatter import format_data, TorrentFormatter


def session_maker():
    """
    Create and return a session object for making HTTP requests.

    Returns:
    - aiohttp.ClientSession: A session object for making HTTP requests.
    """
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
    """
    Asynchronously fetches data from a given URL using a POST request
    with a JSON payload.

    Args:
    - url (str): The URL to send the POST request to.
    - query (str): The query string to include in the JSON payload.
    - trackers (list[str], optional): A list of trackers to include in the
        JSON payload. Defaults to ['nnmclub'].
    - order_by (str, optional): The order to sort the results in the
        JSON payload. Defaults to 's'.
    - filter_by_size (str, optional): The size to filter the results in
        the JSON payload. Defaults to ''.
    - limit (int, optional): The maximum number of results to include in the
        JSON payload. Defaults to 20.
    - offset (int, optional): The number of results to skip in the
        JSON payload. Defaults to 0.
    - full_match (bool, optional): Whether to perform a full match search
        in the JSON payload. Defaults to True.
    - token (str, optional): An authentication token to include in
        the JSON payload. Defaults to ''.

    Returns:
    - json: The JSON response from the server.
    """
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
            return await response.json()


async def scrap_torrents(query: str) -> dict[str, TorrentFormatter]:
    """
    An asynchronous function that scrapes torrents based on a given query.

    Parameters:
    - query (str): The query string used to search for torrents.

    Returns:
    - dict[str, TorrentFormatter]: A dictionary containing the magnet
        keys and their corresponding formatted torrent data.
    """
    raw_data = await fetch_url('/search', query=query)
    data = {i['magnet_key']: format_data(i) for i in raw_data['data']}
    return data


async def make_magnet_link(torrent: TorrentFormatter):
    """
    Asynchronously creates a magnet link for a given torrent.

    Args:
    - torrent (TorrentFormatter): The torrent for which to create a magnet link.

    Returns:
    - TorrentFormatter: The torrent object with the magnet link added.
    """
    async with session_maker() as session:
        async with session.get(
            f'/magnet/{torrent.magnet_key}', ssl=False
        ) as response:
            res = await response.json()
            if res['status_code'] == 200:
                torrent.magnet_link = res['data']['magnet_link']
    return torrent
