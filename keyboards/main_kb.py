from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Скачанные_торренты')
b2 = KeyboardButton('/заглушка')
b3 = KeyboardButton('/Скачать_magnet')
b4 =  KeyboardButton('/Найти_торрент')

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)

kb_main.add(b1).add(b2).add(b3).add(b4)