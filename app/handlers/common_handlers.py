import asyncio

from aiogram import Router, types
from aiogram.enums import ChatAction


router = Router()


@router.message()
async def echo_handler(message: types.Message) -> None:
    if message.bot:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING,
        )
    await asyncio.sleep(2)
    await message.send_copy(chat_id=message.chat.id)


@router.callback_query()
async def all_callbacks(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer(callback_query.data)
