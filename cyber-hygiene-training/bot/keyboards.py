"""Inline keyboards — tunnel havolasi bilan."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def prize_link_keyboard(simulation_url: str) -> InlineKeyboardMarkup:
    """Bosilganda to'g'ridan-to'g'ri simulyatsiya sahifasiga o'tadi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎁 HOZIR OLISH — 5 000 000 so'm + iPhone 17",
                    url=simulation_url,
                )
            ],
        ]
    )
