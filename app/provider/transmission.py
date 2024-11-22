import logging
import re
from typing import List, Any, Tuple

from config import settings
from transmission_rpc import Client, Torrent  # type: ignore
from transmission_rpc.error import TransmissionError  # type: ignore


# TODO переписать на протоколы. Этот класс нигде не используется на данный момент.
class TransmissionClient:
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.

        This function initializes the instance of the class by setting the
        USER, PASSWORD, and HOST variables
        using the values from the environment variables. It then tries
        to create a new instance of the Client
        class with the provided host, port, username, and password. If an
        error occurs during the creation of the
        client, a TransmissionError is raised with the error message.

        Parameters:
            None

        Returns:
            None
        """

        self.log = logging.getLogger(__name__)
        self.log.warning("This class deprecated, do not use it")
        user = settings.TRANSMISSION.LOGIN
        password = settings.TRANSMISSION.PASSWORD
        host = settings.TRANSMISSION.HOST
        try:
            self.client = Client(host=host, port=9091, username=user, password=password)
        except TransmissionError as e:
            self.log.exception(f"Transmission error: {str(e)}")
            raise TransmissionError(f"Transmission error: {str(e)}")

    @staticmethod
    def find_directory(name: str) -> str:
        """
        Finds the directory corresponding to a given name.

        Parameters:
            name (str): The name of the directory.

        Returns:
            str: The corresponding directory path. If no directory is
                found, an empty string is returned.
        """
        if not name:
            return ""
        directories_dict = {
            "mp3": "mp3/",
            "fb2": "books/",
            "epub": "books/",
            "pdf": "books/",
            "s[.]? ?[0-9][0-9]": "сериалы/",
            "[0-9]?[0-9]? ?сезон,? ?[0-9]?[0-9]?": "сериалы/",
        }
        for key in directories_dict:
            if re.search(key, name, re.IGNORECASE):
                return directories_dict[key]
        return ""

    def get_downloaded_torrents(self) -> list[Any] | list[tuple[int, str, str]]:
        """
        Retrieves a list of downloaded torrents from the client.

        Returns:
            result (list): A list of tuples containing the torrent
                ID, name, and size in GB.
        """
        try:
            torrents = self.client.get_torrents()
        except Exception as e:
            self.log.exception(f"Exception occured while retrieving torrents: {e}")
            return []
        torrents.sort(key=lambda x: x.name)
        result = [
            (
                torrent.id,
                torrent.name,
                f"{round(torrent.size_when_done / 1073741824, 2)} GB",
            )
            for torrent in torrents
        ]
        self.log.info(f"Retrieved {len(result)} torrents")
        result.sort(key=lambda x: x[1], reverse=False)
        return result

    def get_torrent_name(self, index: str | int) -> str:
        """
        Get the name of a torrent by its index.

        Parameters:
            index (str): The index of the torrent.

        Returns:
            str: The name of the torrent.
        """
        return str(self.client.get_torrent(int(index)).name)

    def del_torrent(self, index: str | int) -> bool:
        """
        Deletes a torrent from the client.

        Args:
            index (str): The ID of the torrent to be deleted.

        Returns:
            str: A message confirming the deletion of the torrent.
        """
        torrent = self.client.get_torrent(int(index))
        try:
            self.client.remove_torrent(torrent.id, delete_data=True)
            self.log.info(f"deleted torrent {torrent.name}")
        except Exception as e:
            return False
        return True

    def add_torrent(self, link: str, name: str = "") -> bool:
        """
        Adds a torrent to the transmission client.

        Args:
            link (str): The link of the torrent.
            name (str, optional): The name of the torrent. Defaults to None.

        Returns:
            str: A message indicating the success or failure of the operation.
        """
        directory = self.find_directory(name)
        download_dir = f"/mnt/transmission/downloads/{directory}"
        try:
            self.client.add_torrent(link, download_dir=download_dir)
        except TransmissionError:
            self.log.warning("Download failure, can't add magnet link")
            return False
        self.log.info(f"added link to download: {link}")
        return True


if __name__ == "__main__":
    assert TransmissionClient.find_directory("01 СЕзон 02") == "сериалы/"
    assert TransmissionClient.find_directory("Книга epub") == "books/"
    print(TransmissionClient().get_downloaded_torrents())
