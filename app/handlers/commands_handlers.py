from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards import start_menu_kb
from middlewares import IsAdminMiddleware
from utils import render_message
from enums import MessageType

router = Router()
router.message.middleware(IsAdminMiddleware())


@router.message(CommandStart())
async def command_start_handler(message: Message, is_admin: bool) -> None:
    start_message = render_message(
        MessageType.start_menu,
        name=message.from_user.full_name,
        is_admin=is_admin,
    )
    await message.answer(
        start_message,
        reply_markup=start_menu_kb(is_admin=is_admin),
    )
