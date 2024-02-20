import asyncio
import logging

from aiogram import Router, types
from aiogram.enums import ChatAction

from handlers.callback_query_handlers import router

router = Router()


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING,
        )
        await asyncio.sleep(2)
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


@router.callback_query()
async def all_callbacks(callback_query: types.CallbackQuery):
    await callback_query.answer(callback_query.data)
