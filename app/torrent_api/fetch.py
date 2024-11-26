import asyncio
import logging
from typing import Any

import aiohttp
from aiohttp import ClientResponseError, ClientError

from config import settings
from torrent_api.schemas import TorrentApi


logger = logging.getLogger(__name__)


def session_maker() -> aiohttp.ClientSession:
    """
    Create and return a session object for making HTTP requests.

    Returns:
    - aiohttp.ClientSession: A session object for making HTTP requests.
    """
    session = aiohttp.ClientSession(base_url=settings.TORRENT_API)
    return session


async def fetch_url(
    url: str,
    *,
    query: str,
    trackers: list[str] = settings.FIND_TORRENTS_TRACKERS,
    order_by: str = "s",
    filter_by_size: str = "",
    limit: int = settings.FIND_TORRENTS_LIMIT,
    offset: int = 0,
    full_match: bool = True,
    token: str = "",
) -> Any:
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
    try:
        async with session_maker() as session:
            async with session.post(url, json=data, ssl=False) as response:
                response.raise_for_status()  # Raise exception for HTTP error codes
                return await response.json()
    except ClientResponseError as e:
        logger.error(f"HTTP Error {e.status}: {e.message}")
        return {"error": f"HTTP Error {e.status}: {e.message}"}
    except ClientError as e:
        logger.error(f"Client error: {str(e)}")
        return {"error": f"Client error: {str(e)}"}
    except asyncio.TimeoutError:
        logger.error("Request timed out")
        return {"error": "Request timed out"}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}


async def scrap_torrents(
    token: str = settings.FREEDOMIST_TOKEN,
    **kwargs: Any,
) -> dict[str, TorrentApi]:
    """
    An asynchronous function that scrapes torrents based on a given query.

    Parameters:
    - query (str): The query string used to search for torrents.

    Returns:
    - dict[str, TorrentApi]: A dictionary containing the magnet
        keys and their corresponding formatted torrent data.
    """
    try:
        raw_data = await fetch_url("/search", **kwargs, token=token)
        if "error" in raw_data:
            raise ValueError(raw_data["error"])
        return {
            i["magnet_key"]: TorrentApi.model_validate(i)
            for i in raw_data.get("data", [])
        }
    except ValueError as e:
        logger.error(f"Data error: {str(e)}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error in scrap_torrents: {str(e)}")
        return {}


async def list_of_trackers() -> list[str]:
    trackers = []
    try:
        async with session_maker() as session:
            async with session.get("/trackers", ssl=False) as response:
                response.raise_for_status()
                trackers = (await response.json()).get("data", [])
                return trackers
    except ClientError as e:
        logger.error(f"Error fetching trackers: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return []


async def make_magnet_link(torrent: TorrentApi) -> TorrentApi:
    """
    Asynchronously creates a magnet link for a given torrent.

    Args:
    - torrent (TorrentApi): The torrent for which to create a magnet link.

    Returns:
    - TorrentApi: The torrent object with the magnet link added.
    """
    try:
        async with session_maker() as session:
            async with session.get(
                f"/magnet/{torrent.magnet_key}",
                ssl=False,
            ) as response:
                response.raise_for_status()
                res = await response.json()
                if res.get("status_code") == 200:
                    torrent.magnet_link = res["data"]["magnet_link"]
                else:
                    logger.error(
                        "Failed to fetch magnet link: "
                        f"{res.get('message', 'Unknown error')}"
                    )
    except ClientError as e:
        logger.error(f"Error fetching magnet link: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    return torrent
