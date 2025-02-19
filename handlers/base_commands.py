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
        "🛠 <b>Ну чо, пробежимся по функционалу</b>\n\n"
        "👑 <b>/admin</b> — <b>Святая святых, админ-панель</b>\n"
        "     (Тут ты хозяин, тут ты бог, тут вся власть в твоих руках)\n\n"
        "❌ <s>/smsbower</s> — Работа с API SmsBower\n"
        "     (Отрублено нахуй — говно ебаное, работало хуже, чем Windows Vista)\n"
        "     (Если ты спросишь, когда оно вернётся — можешь сразу идти нахуй)\n\n"
        "⚠️ А больше нихуя нет, так что иди нахуй"
    )

    await message.answer(formatted_message, parse_mode="HTML")
