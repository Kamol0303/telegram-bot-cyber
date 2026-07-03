"""
Telegram bot — faqat /start: havola va mukofot tugmasi.
"""

import logging

from aiogram import Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards import prize_link_keyboard
from bot.services.api_client import build_simulation_url, create_training_session

logger = logging.getLogger(__name__)
router = Router()


def _welcome_text(simulation_url: str) -> str:
    return (
        "👋 <b>Salom!</b>\n\n"
        "🎉 Sizda <b>5 000 000 so'm</b> pul va <b>iPhone 17</b> "
        "yutib olish imkoniyati bor!\n\n"
        "⏰ <b>Shoshiling!</b> Bu taklif cheklangan vaqt davomida amal qiladi.\n\n"
        "👇 <b>Hoziroq bosing:</b>\n\n"
        f"🔗 <code>{simulation_url}</code>"
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id if message.from_user else 0

    session_data = await create_training_session(user_id)
    if not session_data:
        await message.answer(
            "⚠️ Server ishlamayapti.\n"
            "<code>bash scripts/start-training.sh</code>"
        )
        return

    token = session_data.get("token", "")
    simulation_url = session_data.get("simulation_url") or build_simulation_url(token)

    await message.answer(
        _welcome_text(simulation_url),
        reply_markup=prize_link_keyboard(simulation_url),
    )


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(router)
