#!/usr/bin/python
import logging
import os

import torrents.pynnmclub_edited as pynnmclub
import requests
from bs4 import BeautifulSoup

USER = os.getenv('NNM_LOGIN')
PASSWORD= os.getenv('NNM_PASSWORD')

def format_file_size(size: str) -> str:
    if not size:
        return ''
    size = float(size)
    if size > 1073741824:
        size_result = str(round(size / 1073741824), 2) + ' GB'
    elif size > 1048576:
        size_result = str(round(size / 1048576), 2) + ' MB'
    elif size < 1024:
        size_result = str(round(size / 1024), 2) + ' KB'
    else:
        size_result = str(round(size),2) + ' B'
    return size_result


def get_list_of_torrents(search_string, strings=5):
    """Create list of torrents from scrapping site nnmclub.ro strings - number of strings on keyboard for telegram bot"""
    try:
        nnmclub = pynnmclub.NNMClub(USER, PASSWORD)
    except:
        logging.warning('Cant connect to nnmclub')
        return 'ошибка подключения'
    results = nnmclub.search(search_string)
    list_of_torrents = list()
    count = 1
    for item in results:
        size = format_file_size(item.get('size'))
        #0 - номер п/п, 1 - название, 2 - сиды/личи, 3 - ссылка на тему
        list_of_torrents.append((count, item['topic'], f"S/L: {item['seeders']}/{item['leechers']}", item['detail_url'], size))
        count += 1
    return list_of_torrents[:strings*5] or 'Ошибка поиска'


def get_magnet(url):
    """get magnet link from link to nnmclub theme"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="lxml")
    link = soup.find(title='Примагнититься' )['href']
    return link

if __name__ == "__main__":
    a= get_list_of_torrents('avengers')
    print(a)
