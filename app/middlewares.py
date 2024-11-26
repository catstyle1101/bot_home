from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from config import settings


class IsAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,  # type: ignore
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user:
            is_admin = settings.user_is_admin(event.from_user.id)
            data["is_admin"] = is_admin
            return await handler(event, data)
        else:
            return await handler(event, data)
