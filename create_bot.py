import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_TOKEN_MANHATTAN = os.getenv('TELEGRAM_TOKEN_MANHATTAN')

bot = Bot(token=TELEGRAM_TOKEN_MANHATTAN)
dp = Dispatcher(bot, storage=MemoryStorage())