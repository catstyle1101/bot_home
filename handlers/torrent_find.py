from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp
from config import settings
from messages import format_torrent
from torrent_api.fetch import make_magnet_link, scrap_torrents
from transmission.transmission_client import TransmissionClient


class FSMFindTorrents(StatesGroup):
    title = State()


@dp.callback_query_handler(Text(equals='menu_find'), state=None)
async def find_title(callback: types.CallbackQuery):
    """
    A callback query handler that handles the 'menu_find' text.
    It sets the FSMFindTorrents.title state and sends a message
    to the callback's message with the text 'Скинь название торрента'.

    Parameters:
    - callback: A types.CallbackQuery object representing the callback query.

    Returns:
    - None
    """
    await FSMFindTorrents.title.set()
    await callback.message.answer('Скинь название торрента')


@dp.message_handler(state=FSMFindTorrents.title)
async def show_torrents(message: types.Message, state: FSMContext):
    """
    This function is a message handler for the FSMFindTorrents state.
    It takes in a message and a state context as parameters.
    The function retrieves the 'title' from the state context and uses
    it to scrape torrents. It then formats the torrents and sends them as
    a reply to the original message. Finally, it finishes the state context.

    Parameters:
    - message: A types.Message object representing the message received.
    - state: A FSMContext object representing the state context.

    Returns:
    - None
    """
    async with state.proxy() as data:
        data['title'] = message.text
        global torrents
        torrents = await scrap_torrents(message.text)
        answer = ''.join(
            [format_torrent(torrent) for torrent in torrents.values()])
        await message.reply(answer)
    await state.finish()


@dp.message_handler(Text(startswith='/link_'))
async def download_torrent(message: types.Message):
    """
    Handles the download of a torrent based on a message.

    Args:
    - message (types.Message): The message object containing the command.

    Returns:
    - None
    """
    if 'torrents' not in globals():
        await message.answer('Сделай поиск заново, ссылки устарели')
        return

    magnet_key = message.text.split('_')[1]
    torrent = await make_magnet_link(torrents.get(magnet_key))

    if torrent.magnet_link.startswith('magnet'):
        if message.from_user.id in settings.ALLOWED_USERS:
            client = TransmissionClient()
            client.add_torrent(torrent.magnet_link)
            await message.answer('Закачка добавлена')

        await message.answer(
            format_torrent(torrents.get(magnet_key), short=True))
        await message.answer(torrent.magnet_link)
