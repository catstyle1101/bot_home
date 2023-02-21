import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp
from config import MODERATORS, ADMINS
from keyboards import inline_start_menu_kb
from transmission.transmission_client import TransmissionClient


class FSMmagnet(StatesGroup):
    magnet = State()


@dp.callback_query_handler(Text(startswith='menu_downloadmagnet'), state=None)
async def download_magnet(callback: types.CallbackQuery):
    await FSMmagnet.magnet.set()
    await callback.message.answer('Скинь ссылку')


@dp.message_handler(state=FSMmagnet.magnet)
async def add_link_to_downloads(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['magnet'] = message.text
    allowed_users = ADMINS + MODERATORS
    if message.from_user.id in allowed_users:
        if message.text.startswith('magnet'):
            try:
                transmission_client = TransmissionClient()
                answer = transmission_client.add_torrent(str(message.text))
                await message.reply(
                    answer, reply_markup=inline_start_menu_kb()
                )
                logging.info(f'Добавлена ссылка {message.text}')
            except Exception as e:
                await message.reply(
                    'Возникла ошибка при подключении к серверу Transmission'
                )
                logging.warning(f"Magnet link is not added because of {e}")
        else:
            await message.reply(
                'Это не magnet ссылка', reply_markup=inline_start_menu_kb()
            )
    else:
        await message.reply('Это только для жителей квартиры)')
    await message.delete()
    await state.finish()
