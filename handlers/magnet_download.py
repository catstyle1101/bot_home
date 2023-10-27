import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp
from config import ALLOWED_USERS
from keyboards import inline_start_menu_kb
from transmission.transmission_client import TransmissionClient


class FSMmagnet(StatesGroup):
    magnet = State()


@dp.callback_query_handler(Text(startswith='menu_downloadmagnet'), state=None)
async def download_magnet(callback: types.CallbackQuery):
    """
    Handles the callback query for downloading a magnet.

    Args:
    - callback: A `types.CallbackQuery` object representing the callback query.

    Returns:
    - None
    """
    await FSMmagnet.magnet.set()
    await callback.message.answer('Скинь ссылку')


@dp.message_handler(state=FSMmagnet.magnet)
async def add_link_to_downloads(message: types.Message, state: FSMContext):
    """
    Handles the message received when the state is FSMmagnet.magnet.

    Args:
    - message (types.Message): The message received.
    - state (FSMContext): The state of the conversation.

    Returns:
    - None
    """
    async with state.proxy() as data:
        data['magnet'] = message.text

    if message.from_user.id not in ALLOWED_USERS:
        await message.reply('Это только для жителей квартиры)')
        await message.delete()
        await state.finish()
        return

    if not message.text.startswith('magnet'):
        await message.reply(
            'Это не magnet ссылка',
            reply_markup=inline_start_menu_kb(message.from_user.id),
        )
        await message.delete()
        await state.finish()
        return

    try:
        transmission_client = TransmissionClient()
        answer = transmission_client.add_torrent(str(message.text))
        await message.reply(
            answer,
            reply_markup=inline_start_menu_kb(message.from_user.id),
        )
        logging.info(f'Добавлена ссылка {message.text}')
    except Exception as e:
        await message.reply(
            'Возникла ошибка при подключении к серверу Transmission'
        )
        logging.warning(f"Magnet link is not added because of {e}")

    await message.delete()
    await state.finish()
