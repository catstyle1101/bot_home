import logging

from aiogram import types
from aiogram.dispatcher.filters import Text
from config import ADMINS, MODERATORS
from create_bot import dp, bot
from keyboards import inline_del_torrent_kb, inline_start_menu_kb
from transmission.transmission_client import TransmissionClient
from digits_emoji import random_heart


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    add = ''
    if message.from_user.id == 454690652:
        add += 'P.S. Ты -  моя любовь' + random_heart()
    try:
        await message.answer(
            'Привет! Что будем делать?\n' +
            add, reply_markup=inline_start_menu_kb()
        )
    except Exception as e:
        logging.error(e)
        await message.reply('Напиши боту в ЛС')


@dp.callback_query_handler(Text(equals='menu_list'))
async def command_downloaded_torrents(message: types.CallbackQuery):
    """
    Бот высылает список скачанных торрентов,
    с кнопкой удаления для админов.
    """
    transmission_client = TransmissionClient()
    list_of_torrents = transmission_client.get_downloaded_torrents()
    allowed_users = ADMINS + MODERATORS
    answer_template = "🟣\t{}\t{}\t"
    answer_delete_template = "🗑/delete_{}\n\n"
    answer = str()
    for torrent in list_of_torrents:
        torrent_name = ' '.join(torrent[1].split('.'))
        torrent_size = torrent[2]
        torrent_number = torrent[0]
        answer += answer_template.format(torrent_name, torrent_size)
        if message.from_user.id in allowed_users:
            answer += answer_delete_template.format(torrent_number)
        else:
            answer += "\n\n"
    if len(answer) > 4096:
        for x in range(0, len(answer), 4096):
            await bot.send_message(message.from_user.id, answer[x:x+4096])
    else:
        await bot.send_message(message.from_user.id, answer)


@dp.message_handler(Text(startswith='/delete_'))
async def del_call(message: types.Message):
    """формирую запрос на удаление определенного торрента"""
    allowed_users = ADMINS + MODERATORS
    transmission_client = TransmissionClient()
    res = message.text.split('_')
    name = transmission_client.get_torrent_name(res[1])
    answer = f'Удалить позицию №{res[1]} {name}?'
    if message.from_user.id in allowed_users:
        await message.answer(
            answer, reply_markup=inline_del_torrent_kb(res[1])
        )
        await message.delete()
    else:
        await message.answer('Тебе нельзя удалять тут ничего')


@dp.callback_query_handler(Text(startswith='del_'))
async def delete_torrent(callback: types.CallbackQuery):
    """удаляем торрент, если ответ в инлайн кнопке ДА"""
    transmission_client = TransmissionClient()
    res = callback.data.split('_')
    if res[1] == 'yes':
        await callback.answer(
            transmission_client.del_torrent(res[2]), show_alert=True
        )
        await callback.message.delete()
    else:
        await callback.answer('Ок, ничего не удаляю')
        await callback.message.delete()
