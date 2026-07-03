"""Inline and reply keyboards for the bot."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def remove_keyboard():
    from aiogram.types import ReplyKeyboardRemove
    return ReplyKeyboardRemove()


def phone_request_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="✏️ Raqamni qo'lda yozish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def continue_simulation_keyboard(simulation_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎁 MUKOFOTNI OLISH",
                    url=simulation_url,
                )
            ],
        ]
    )
