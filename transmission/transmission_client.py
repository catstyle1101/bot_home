import logging
import os
import re

from transmission_rpc import Client
from transmission_rpc.error import (TransmissionConnectError, TransmissionAuthError,
    TransmissionError)


class TransmissionClient:
    def __init__(self):
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
        USER = os.getenv('TR_LOGIN')
        PASSWORD = os.getenv('TR_PASSWORD')
        HOST = '192.168.1.1'
        #HOST = 'catstyle1101.ddns.net'
        try:
            self.client = Client(host=HOST, port=9091, username=USER, password=PASSWORD)
        except TransmissionError as e:
            logging.warning(f"Transmission error: {str(e)}")
            raise TransmissionError(f"Transmission error: {str(e)}")

    @staticmethod
    def find_directory(name: str):
        """
        Finds the directory corresponding to a given name.

        Parameters:
            name (str): The name of the directory.

        Returns:
            str: The corresponding directory path. If no directory is found, an empty string is returned.
        """
        if not name:
            return ''
        DIRECTORIES_DICT = {
            'mp3': 'mp3/',
            'fb2': 'books/',
            'epub': 'books/',
            'pdf': 'books/',
            's[.]? ?[0-9][0-9]': 'сериалы/',
            '[0-9]?[0-9]? ?сезон,? ?[0-9]?[0-9]?': 'сериалы/'
        }
        for key in DIRECTORIES_DICT:
            if re.search(key, name, re.IGNORECASE):
                return DIRECTORIES_DICT[key]
        return ''

    def get_downloaded_torrents(self):
        """
        Retrieves a list of downloaded torrents from the client.

        Returns:
            result (list): A list of tuples containing the torrent ID, name, and size in GB.
        """
        torrents = self.client.get_torrents()
        result = [(torrent.id, torrent.name,
                f"{round(torrent.size_when_done / 1073741824, 2)} GB")
                for torrent in torrents]
        return result

    def get_torrent_name(self, number: str):
        """
        Get the name of a torrent by its number.

        Parameters:
            number (str): The number of the torrent.

        Returns:
            str: The name of the torrent.
        """
        return self.client.get_torrent(int(number)).name

    def del_torrent(self, number: str):
        """
        Deletes a torrent from the client.

        Args:
            number (str): The ID of the torrent to be deleted.

        Returns:
            str: A message confirming the deletion of the torrent.
        """
        torrent = self.client.get_torrent(int(number))
        self.client.remove_torrent(torrent.id, delete_data=True)
        logging.info(f"deleted torrent {torrent.name}")
        return f"Удалена позиция №{number} {torrent.name}"

    def add_torrent(self, link: str, name: str|None = None):
        """
        Adds a torrent to the transmission client.

        Args:
            link (str): The link of the torrent.
            name (str, optional): The name of the torrent. Defaults to None.

        Returns:
            str: A message indicating the success or failure of the operation.
        """
        directory = self.find_directory(name)
        download_dir = f'/mnt/transmission/downloads/{directory}'
        try:
            self.client.add_torrent(link, download_dir=download_dir)
        except TransmissionError:
            logging.warning("Download failure, can't add magnet link")
            return "Произошла ошибка"
        logging.info(f"added link to download: {link}")
        return "Закачка добавлена"


if __name__ == '__main__':
    assert TransmissionClient.find_directory('01 СЕзон 02') == 'сериалы/'
    assert TransmissionClient.find_directory('Книга epub') == 'books/'
    print(TransmissionClient().get_downloaded_torrents())
