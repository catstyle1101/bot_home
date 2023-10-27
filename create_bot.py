import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from config import settings

bot = Bot(token=settings.TELEGRAM_TOKEN_MANHATTAN)
dp = Dispatcher(bot, storage=MemoryStorage())
