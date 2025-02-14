from aiogram import Router
from aiogram.types import Message

from aiogram.filters import Command

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    formatted_message = (
        "👋 <b>Привет, админ епта!</b>\n\n"
        "ℹ️ Больше инфы по функционалу: /help"
    )
    await message.answer(formatted_message, parse_mode="HTML")


@router.message(Command('help'))
async def cmd_help(message: Message):
    formatted_message = (
        "🛠 <b>Ну чо епта, пробежимся по функционалу</b>\n\n"
        "📡 /smsbower — Работа с API SmsBower\n\n"
        "⚠️ А больше нихуя нет, так что иди нахуй"
    )
    await message.answer(formatted_message, parse_mode="HTML")
