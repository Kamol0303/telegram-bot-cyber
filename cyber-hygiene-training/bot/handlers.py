"""
Bot message handlers for the educational training flow.
Collects name/phone only in memory — passed via URL fragment, never stored server-side.
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
    restart_keyboard,
)
from bot.services.api_client import create_training_session
from bot.states import TrainingFlow

logger = logging.getLogger(__name__)
router = Router()

SCAM_WELCOME = """
🎉 <b>Congratulations!</b> 🎉

You have been selected for a chance to win one of the following prizes:

🚗 <b>BYD Champion</b>
📱 <b>iPhone 17</b>
💰 <b>5,000,000 UZS</b>
🏠 <b>Apartment</b>
🚙 <b>Luxury Car</b>

<i>⚠️ EDUCATIONAL SIMULATION — This message intentionally resembles common online scam patterns for cybersecurity awareness training.</i>

To continue the <b>awareness simulation</b>, please provide:

👤 Your <b>Full Name</b>
"""

PRIVACY_NOTICE = """
🔒 <b>Privacy Notice (Educational Simulation)</b>

The information you provide is used <b>only within this training simulation</b> and is <b>NOT stored</b> on any server.

Your name will appear only on your local training certificate.
"""

ABOUT_TEXT = """
🛡️ <b>Cyber Hygiene Awareness Training</b>

This Telegram bot is part of an <b>educational cybersecurity simulation</b>.

You will experience a realistic scam scenario to learn how to recognize:
• Fake lottery messages
• Phishing websites
• Payment card traps
• SMS/OTP theft

<b>No real data is collected or transmitted.</b>

Use /start to begin the training.
"""


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(SCAM_WELCOME)
    await message.answer(PRIVACY_NOTICE)
    await message.answer("Please enter your <b>Full Name</b>:")
    await state.set_state(TrainingFlow.waiting_for_name)


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(ABOUT_TEXT)


@router.callback_query(F.data == "about_training")
async def callback_about(callback: CallbackQuery):
    await callback.message.answer(ABOUT_TEXT)
    await callback.answer()


@router.callback_query(F.data == "restart")
async def callback_restart(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(SCAM_WELCOME)
    await callback.message.answer(PRIVACY_NOTICE)
    await callback.message.answer("Please enter your <b>Full Name</b>:")
    await state.set_state(TrainingFlow.waiting_for_name)
    await callback.answer()


@router.message(TrainingFlow.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    name = (message.text or "").strip()
    if len(name) < 2 or len(name) > 100:
        await message.answer("Please enter a valid full name (2–100 characters):")
        return
    await state.update_data(display_name=name)
    await message.answer(
        f"Thank you, <b>{name}</b>!\n\n"
        "Now please provide your <b>Phone Number</b> for the simulation.\n\n"
        "<i>Remember: this is NOT stored on any server.</i>",
        reply_markup=phone_request_keyboard(),
    )
    await state.set_state(TrainingFlow.waiting_for_phone)


@router.message(TrainingFlow.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else ""
    await _finish_registration(message, state, phone)


@router.message(TrainingFlow.waiting_for_phone, F.text == "✏️ Type Phone Manually")
async def process_phone_manual_prompt(message: Message):
    await message.answer(
        "Please type your phone number (simulation only):",
        reply_markup=remove_keyboard(),
    )


@router.message(TrainingFlow.waiting_for_phone)
async def process_phone_text(message: Message, state: FSMContext):
    phone = (message.text or "").strip()
    if len(phone) < 5:
        await message.answer("Please enter a valid phone number:")
        return
    await _finish_registration(message, state, phone)


async def _finish_registration(message: Message, state: FSMContext, phone: str):
    data = await state.get_data()
    name = data.get("display_name", "Trainee")
    user_id = message.from_user.id if message.from_user else 0

    session_data = await create_training_session(user_id)
    if not session_data:
        await message.answer(
            "⚠️ Training server is temporarily unavailable. Please try again later with /start",
            reply_markup=remove_keyboard(),
        )
        await state.clear()
        return

    token = session_data["token"]
    base_url = session_data["simulation_url"].split("?")[0]

    # PII passed via URL fragment — never sent to server, only stored in browser sessionStorage
    fragment = f"name={quote(name)}&phone={quote(phone)}"
    simulation_url = f"{base_url}?token={token}#{fragment}"

    await message.answer(
        "✅ <b>Registration Complete (Simulation)</b>\n\n"
        "You are now ready to continue the cybersecurity awareness training.\n\n"
        "Click the button below to open the <b>simulated lottery website</b>.\n\n"
        "⚠️ <i>This is an educational simulation. No real prizes exist.</i>",
        reply_markup=remove_keyboard(),
    )
    await message.answer(
        "👇 Press to continue:",
        reply_markup=continue_simulation_keyboard(simulation_url),
    )
    await state.clear()


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(router)
