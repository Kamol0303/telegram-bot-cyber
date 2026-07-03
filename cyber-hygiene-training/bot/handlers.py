"""
Telegram bot — /start da salomlashadi va tunnel havolasini beradi.
Havola zphisher ngrok/serveo o'rniga platforma tunnel URL dan olinadi.
"""

import logging

from aiogram import Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import prize_link_keyboard
from bot.services.api_client import (
    build_simulation_url,
    create_training_session,
    fetch_tunnel_status,
    get_public_base_url,
)

logger = logging.getLogger(__name__)
router = Router()


def _welcome_text(public_url: str) -> str:
    return (
        "👋 <b>Salom!</b>\n\n"
        "🎉 <b>Tabriklaymiz!</b> Sizda quyidagilarni yutib olish imkoniyati bor:\n\n"
        "💰 <b>5 000 000 so'm</b> naqd pul\n"
        "📱 <b>iPhone 17</b>\n\n"
        "⏰ <b>Shoshiling!</b> Bu taklif faqat cheklangan vaqt davomida amal qiladi.\n"
        "Ko'p odamlar allaqachon mukofotini oldi — o'z navbatingizni qo'ldan boy bermang!\n\n"
        f"👇 <b>Hoziroq bosing va mukofotingizni oling:</b>\n"
        f"<a href=\"{public_url}\">{public_url}</a>"
    )


ABOUT_TEXT = """
🛡️ <b>Cyber Hygiene Awareness Training</b> (instruktor)

Bu bot ta'lim simulyatsiyasi uchun.
Havola tunnel (ngrok/serveo) orqali avtomatik yaratiladi.

<b>/status</b> — joriy havola
<b>/link</b> — yangi havola yaratish
"""


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id if message.from_user else 0

    session_data = await create_training_session(user_id)
    if not session_data:
        await message.answer(
            "⚠️ Server hozir ishlamayapti.\n\n"
            "Instruktor: <code>bash scripts/start-training.sh</code>"
        )
        return

    token = session_data.get("token", "")
    simulation_url = build_simulation_url(token)

    await message.answer(
        _welcome_text(simulation_url),
        reply_markup=prize_link_keyboard(simulation_url),
        disable_web_page_preview=False,
    )


@router.message(Command("link"))
async def cmd_link(message: Message):
    """Instruktor: yangi sessiya va havola."""
    user_id = message.from_user.id if message.from_user else 0
    session_data = await create_training_session(user_id)
    if not session_data:
        await message.answer("⚠️ Backend ulanmagan.")
        return
    url = build_simulation_url(session_data["token"])
    await message.answer(
        f"🔗 <b>Yangi havola:</b>\n<code>{url}</code>",
        reply_markup=prize_link_keyboard(url),
    )


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(ABOUT_TEXT)


@router.message(Command("status"))
async def cmd_status(message: Message):
    status = await fetch_tunnel_status()
    if not status:
        await message.answer(
            "⚠️ <b>Backend ulanmagan</b>\n\n"
            "<code>bash scripts/start-training.sh</code>"
        )
        return

    public = status.get("public_url") or status.get("base_url", "—")
    tunnel_type = status.get("tunnel_type", "none")

    await message.answer(
        "📡 <b>Platforma holati</b>\n\n"
        f"🌐 <b>Tunnel havolasi:</b>\n<code>{public}</code>\n\n"
        f"🔗 <b>Tunnel turi:</b> {tunnel_type}\n"
        f"🏠 <b>Mahalliy:</b> <code>{status.get('local_url')}</code>\n\n"
        "Foydalanuvchilar botga <b>/start</b> yuboradi — havola avtomatik beriladi."
    )


@router.message(Command("tunnel"))
async def cmd_tunnel(message: Message):
    await message.answer(
        "🔧 <b>Tunnel sozlash</b>\n\n"
        "<code>bash scripts/start-training.sh</code>\n\n"
        "Tanlov: Ngrok (2) tavsiya etiladi.\n"
        "Tunnel ishga tushgach <b>/status</b> bilan havolani ko'ring."
    )


@router.callback_query(lambda c: c.data == "get_prize")
async def callback_get_prize(callback: CallbackQuery):
    """Tugma bosilganda yangi sessiya + havola."""
    user_id = callback.from_user.id if callback.from_user else 0
    session_data = await create_training_session(user_id)
    if session_data:
        url = build_simulation_url(session_data["token"])
        await callback.message.answer(
            "👇 Mukofotni olish uchun bosing:",
            reply_markup=prize_link_keyboard(url),
        )
    await callback.answer()


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(router)
