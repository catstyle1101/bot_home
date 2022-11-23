from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def inline_del_torrent_kb(torrent : int):
    return InlineKeyboardMarkup().row(InlineKeyboardButton(text='Да', callback_data='del_yes_' + str(torrent)), InlineKeyboardButton(text='Нет', callback_data='del_no_'+ str(torrent)))

def inline_add_torrent_kb():
    return InlineKeyboardMarkup().row(InlineKeyboardButton(text='Да', callback_data='add_yes'), InlineKeyboardButton(text='Нет', callback_data='add_no'))

def inline_start_menu_kb():
    return InlineKeyboardMarkup()\
        .row(InlineKeyboardButton(text='📂 Скачанные торренты', callback_data='menu_list'))\
        .row(InlineKeyboardButton(text='🧲 Ссылка', callback_data='menu_downloadmagnet'), InlineKeyboardButton(text='🔎  Найти', callback_data='menu_find'))\

        #на данный момент библиотека не поддерживает наш пылесос, поэтому ждем обновлений
        #https://github.com/rytilahti/python-miio/issues/1114
        #вот ссылка на issues (Add Xiaomi Vacuum 1C dreame.vacuum.mc1808 to Vacuum_Miio Integration #1182)
        #.row(InlineKeyboardButton(text='🧹 ▶️ ', callback_data='menu_vacuum_start'),InlineKeyboardButton(text='🧹⏹️ ', callback_data='menu_vacuum_stop'))

