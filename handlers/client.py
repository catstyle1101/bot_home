import logging

from aiogram import types
from aiogram.dispatcher.filters import Text
from config import settings
from create_bot import dp, bot
from keyboards import inline_del_torrent_kb, inline_start_menu_kb
from transmission.transmission_client import TransmissionClient
from digits_emoji import random_heart


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    """
    Handles the 'start' and 'help' commands.

    Args:
    - message (types.Message): The message object received.

    Returns:
    - None
    """
    add = (
        'P.S. Ты - моя любовь' + random_heart()
        if message.from_user.id == settings.SPECIAL_USER else ''
    )
    await message.answer(
        'Привет! Что будем делать?\n' +
        add, reply_markup=inline_start_menu_kb(message.from_user.id)
    )


@dp.callback_query_handler(Text(equals='menu_list'))
async def command_downloaded_torrents(message: types.CallbackQuery):
    """
    Bot sends a list of downloaded torrents with a delete button for admins.
    """
    transmission_client = TransmissionClient()
    list_of_torrents = transmission_client.get_downloaded_torrents()
    answer_template = '🟣\t{}\t{}\t'
    answer_delete_template = '🗑/delete_{}'
    answer = ''
    for torrent_number, torrent_name, torrent_size in list_of_torrents:
        torrent_name = ' '.join(torrent_name.split('.'))
        answer += answer_template.format(torrent_name, torrent_size)
        if message.from_user.id in settings.ALLOWED_USERS:
            answer += answer_delete_template.format(torrent_number)
        answer += "\n\n"
    if len(answer) > 4096:
        for x in range(0, len(answer), 4096):
            await bot.send_message(message.from_user.id, answer[x:x+4096])
    else:
        await bot.send_message(message.from_user.id, answer)


@dp.message_handler(Text(startswith='/delete_'))
async def del_call(message: types.Message):
    """
    Handles the deletion of a torrent.

    Args:
    - message (types.Message): The message object containing the command.

    Returns:
    - None
    """
    transmission_client = TransmissionClient()
    torrent_id = message.text.split('_')[1]

    name = transmission_client.get_torrent_name(torrent_id)
    answer = f'Удалить позицию №{torrent_id} {name}?'
    if message.from_user.id in settings.ALLOWED_USERS:
        await message.answer(
            answer, reply_markup=inline_del_torrent_kb(torrent_id)
        )
        await message.delete()
    else:
        await message.answer('Тебе нельзя удалять тут ничего')


@dp.callback_query_handler(Text(startswith='del_'))
async def delete_torrent(callback: types.CallbackQuery):
    """
    Handles the callback query for deleting a torrent.

    Args:
    - callback (types.CallbackQuery): The callback query object.

    Returns:
    - None
    """
    transmission_client = TransmissionClient()
    res = callback.data.split('_')
    if res[1] == 'yes':
        await callback.answer(
            transmission_client.del_torrent(res[2]), show_alert=True)
    else:
        await callback.answer('Ок, ничего не удаляю')
    await callback.message.delete()
