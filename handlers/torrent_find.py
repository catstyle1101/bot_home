from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp
from config import MODERATORS, ADMINS
from messages import format_torrent
from torrent_api.fetch import make_magnet_link, scrap_torrents
from transmission.transmission_client import TransmissionClient


class FSMFindTorrents(StatesGroup):
    title = State()


@dp.callback_query_handler(Text(equals='menu_find'), state=None)
async def find_title(callback: types.CallbackQuery):
    await FSMFindTorrents.title.set()
    await callback.message.answer('Скинь название торрента')


@dp.message_handler(state=FSMFindTorrents.title)
async def show_torrents(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    allowed_users = ADMINS + MODERATORS
    if message.from_user.id in allowed_users:
        global torrents
        torrents = await scrap_torrents(message.text)
        answer = ''
        for torrent in torrents.values():
            answer += format_torrent(torrent)
        await message.reply(answer)

    else:
        await message.reply('Это только для жителей квартиры)')
    await state.finish()


@dp.message_handler(Text(startswith='/link_'))
async def download_torrent(message: types.Message):
    if 'torrents' not in globals():
        await message.answer('Сделай поиск заново, ссылки устарели')
        return
    magnet_key = message.text.split('_')[1]
    client = TransmissionClient()
    torrent = await make_magnet_link(torrents.get(magnet_key))
    if torrent.magnet_link.startswith('magnet'):
        client.add_torrent(torrent.magnet_link)
        await message.answer('Закачка добавлена')
        await message.answer(
            format_torrent(torrents.get(magnet_key), short=True))
        await message.answer(torrent.magnet_link)
