import logging
import os
import re

from transmission_rpc import Client
from transmission_rpc.error import TransmissionConnectError, TransmissionAuthError, TransmissionError, \
    TransmissionTimeoutError


class TransmissionClient:
    def __init__(self):
        USER = os.getenv('TR_LOGIN')
        PASSWORD = os.getenv('TR_PASSWORD')
        HOST = '192.168.1.1'
        #HOST = 'catstyle1101.ddns.net'
        try:
            self.client = Client(host=HOST, port=9091, username=USER, password=PASSWORD)
        except TransmissionAuthError:
            logging.warning(f"Transmission login failed")
            raise TransmissionAuthError("Wrong Transmission login/password")
        except TransmissionConnectError:
            logging.warning(f"Transmission client unavailable")
            raise TransmissionConnectError("Transmission server :w"
                                           "unavailable")

    @staticmethod
    def find_directory(name: str):
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
        return [(torrent.id, torrent.name, str(round(torrent.size_when_done / 1073741824, 2)) + " GB")
                for torrent in self.client.get_torrents()]

    def get_torrent_name(self, number: str):
        return self.client.get_torrent(int(number)).name

    def del_torrent(self, number: str):
        torrent = self.client.get_torrent(int(number))
        self.client.remove_torrent(torrent.id, delete_data=True)
        logging.info(f"deleted torrent {torrent.name}")
        return f"Удалена позиция №{number} {torrent.name}"

    def add_torrent(self, link: str, name: str|None = None):
        directory = self.find_directory(name)
        try:
            self.client.add_torrent(link, download_dir='/mnt/transmission/downloads/' + directory)
        except TransmissionError:
            logging.warning("Download failure, can't add magnet link")
            return "Произошла ошибка"
        logging.info(f"added link to download: {link}")
        return "Закачка добавлена"


if __name__ == '__main__':
    assert TransmissionClient.find_directory('01 СЕзон 02') == 'сериалы/'
    assert TransmissionClient.find_directory('Книга epub') == 'books/'
    print(TransmissionClient().get_downloaded_torrents())
