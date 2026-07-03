"""
Telegram bot entry point for Cyber Hygiene Awareness Training.
Welcomes users with an educational scam simulation message.
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.types import BotCommand

from bot.config import bot_settings
from bot.handlers import register_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not bot_settings.telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN is not set. Copy .env.example to .env and configure it.")
        sys.exit(1)

    bot = Bot(
        token=bot_settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await bot.set_my_commands([
        BotCommand(command="start", description="Mukofot dasturida qatnashish"),
        BotCommand(command="status", description="[Instruktor] Platforma holati"),
        BotCommand(command="tunnel", description="[Instruktor] Tunnel sozlash"),
        BotCommand(command="about", description="[Instruktor] Loyiha haqida"),
    ])

    dp = Dispatcher(storage=MemoryStorage())
    register_handlers(dp)

    logger.info("Starting Cyber Hygiene Awareness Training bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
