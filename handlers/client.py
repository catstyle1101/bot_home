import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from config import ADMINS, MODERATORS
from create_bot import dp, bot
from keyboards import  inline_del_torrent_kb, inline_start_menu_kb
from transmission.transmission_client import TransmissionClient
from digits_emoji import convert_digits_to_emoji,  random_heart


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    add =''
    if message.from_user.id == 454690652:
        add += 'P.S. Ты -  моя любовь' + random_heart()
    try:
        await message.answer('Привет! Что будем делать?\n' + add, reply_markup=inline_start_menu_kb())
    except:
        await message.reply('Напиши боту в ЛС')


@dp.callback_query_handler(Text(startswith='menu_list'))
async def command_downloaded_torrents(message: types.CallbackQuery):
    """бот высылает список скачанных торрентов, с кнопкой удаления для админов"""
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
    await bot.send_message(message.from_user.id, answer)


@dp.message_handler(Text(startswith='/delete_'))
async def del_call(message: types.Message):
    """формирую запрос на удаление определенного торрента"""
    transmission_client = TransmissionClient()
    res = message.text.split('_')
    name = transmission_client.get_torrent_name(res[1])
    answer = f'Удалить позицию №{res[1]} {name}?'
    await message.answer(answer, reply_markup=inline_del_torrent_kb(res[1]))
    await message.delete()


@dp.callback_query_handler(Text(startswith='del_'))
async def delete_torrent(callback: types.CallbackQuery):
    """удаляем торрент, если ответ в инлайн кнопке ДА"""
    transmission_client = TransmissionClient()
    res = callback.data.split('_')
    if res[1] == 'yes':
        await callback.answer(transmission_client.del_torrent(res[2]), show_alert=True)
        await callback.message.delete()
    else:
        await callback.answer('Ок, ничего не удаляю')
        await callback.message.delete()


def register_handlers_client(dp: Dispatcher):
    pass
    #dp.register_message_handler(command_start, commands=[ 'start', 'help'])
    #dp.register_callback_query_handler(command_downloaded_torrents, Text(startswith='menu_list'))
    #dp.register_message_handler(del_call, Text(startswith='/delete_'))
    #dp.register_callback_query_handler(delete_torrent, Text(startswith='del_'))
