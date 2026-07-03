"""Inline and reply keyboards for the bot."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from bot.config import bot_settings


def remove_keyboard():
    from aiogram.types import ReplyKeyboardRemove
    return ReplyKeyboardRemove()


def phone_request_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Share Phone (Simulation)", request_contact=True)],
            [KeyboardButton(text="✏️ Type Phone Manually")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def continue_simulation_keyboard(simulation_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 Continue Simulation",
                    url=simulation_url,
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ About This Training",
                    callback_data="about_training",
                )
            ],
        ]
    )


def restart_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Start New Training", callback_data="restart")]
        ]
    )
