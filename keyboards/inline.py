from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ALLOWED_USERS

def inline_del_torrent_kb(torrent : int):
    """
    Generates an inline keyboard markup for deleting a torrent.

    Parameters:
    - torrent (int): The ID of the torrent to be deleted.

    Returns:
    - InlineKeyboardMarkup: The generated inline keyboard markup.
    """
    del_yes_callback = f'del_yes_{torrent}'
    del_no_callback = f'del_no_{torrent}'
    return (
        InlineKeyboardMarkup()
        .row(InlineKeyboardButton(
            text='Да', callback_data=del_yes_callback),
        InlineKeyboardButton(
            text='Нет', callback_data=del_no_callback),
        )
    )

def inline_add_torrent_kb():
    """
    Creates an inline keyboard markup with two buttons for choice for delete
    a torrent.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup with two buttons for adding a torrent.
    """
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton(text='Да', callback_data='add_yes'),
        InlineKeyboardButton(text='Нет', callback_data='add_no'),
    )
    return kb

def inline_start_menu_kb(user_id: int):
    """
    Generates an inline keyboard markup for the start menu.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        InlineKeyboardMarkup: The generated inline keyboard markup.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text='🔎  Найти', callback_data='menu_find'))
    if user_id in ALLOWED_USERS:
        keyboard.row(
            InlineKeyboardButton(text='🧲 Ссылка', callback_data='menu_downloadmagnet'),
            InlineKeyboardButton(text='📂 Скачанные торренты', callback_data='menu_list')
        )
    return keyboard

    # на данный момент библиотека не поддерживает наш пылесос, поэтому ждем обновлений
    # https://github.com/rytilahti/python-miio/issues/1114
    # вот ссылка на issues (Add Xiaomi Vacuum 1C dreame.vacuum.mc1808 to Vacuum_Miio Integration #1182)
    # .row(InlineKeyboardButton(text='🧹 ▶️ ', callback_data='menu_vacuum_start'),InlineKeyboardButton(text='🧹⏹️ ', callback_data='menu_vacuum_stop'))
