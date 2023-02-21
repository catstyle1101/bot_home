from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from config import MODERATORS, ADMINS
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import inline_add_torrent_kb
from torrents import get_list_of_torrents, get_magnet
from transmission.transmission_client import TransmissionClient


class FSMScrapping(StatesGroup):
    name = State()


async def start(message: types.CallbackQuery):
    await FSMScrapping.name.set()
    await message.message.answer('Напиши название')


async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    global scrapping_torrents_list
    try:
        scrapping_torrents_list = get_list_of_torrents(data['name'])
        mess = str()
        for i in scrapping_torrents_list:
            mess += (str(i[0]) + '\t' + str(i[1]) + '\t'
                     + '/download_' + str(i[0]) + '\t'
                     + i[2] + '\t' + i[4] + '\n' + i[3])
        await message.reply(mess)
    except Exception:
        await message.reply(
            'Похоже сеть или сайт недоступны, либо перефразируй запрос'
        )
    await state.finish()


async def find_magnet(message: types.Message):
    res = message.text.split('_')
    global magnet
    try:
        magnet = get_magnet(scrapping_torrents_list[int(res[1])-1][3])
    except Exception:
        await message.reply('Сылки нет!')
        await message.delete()
        return
    global torrent_name
    torrent_name = scrapping_torrents_list[int(res[1])-1][1]
    torrent_size = scrapping_torrents_list[int(res[1])-1][4]
    allowed_users = ADMINS + MODERATORS
    if message.from_user.id in allowed_users:
        await message.reply(
            magnet + f'\n\n{torrent_name}\t{ torrent_size}\n\nСкачать файл?',
            reply_markup=inline_add_torrent_kb()
        )
    else:
        await message.reply(
            magnet + f'\n\n{torrent_name}\t'
            f'{ torrent_size}\n\nвот magnet ссылка на файл'
        )
    await message.delete()


async def start_download(callback: types.CallbackQuery):
    transmission_client = TransmissionClient()
    res = callback.data.split('_')
    if res[1] == 'yes':
        await callback.answer(
            transmission_client.add_torrent(magnet, torrent_name),
            show_alert=True
        )
    else:
        await callback.answer('Ок, ничего не добавляю', show_alert=True)
    await callback.message.delete()


def register_handlers_scrapping(dp: Dispatcher):
    dp.register_callback_query_handler(start, Text(startswith='menu_find'),
                                       state=None)
    dp.register_message_handler(get_name, state=FSMScrapping.name)
    dp.register_message_handler(find_magnet, Text(startswith='/download_'))
    dp.register_callback_query_handler(start_download, Text(startswith='add_'))
