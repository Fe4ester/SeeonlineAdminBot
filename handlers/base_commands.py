from aiogram import Router
from aiogram.types import Message

from aiogram.filters import Command

from keyboards.reply_kb import get_test_keyboard

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
        "📡 /smsbower — Работа с API SmsBower\n"
        "🧑‍💻 /admin — Админ-панель\n\n"
        "⚠️ А больше нихуя нет, так что иди нахуй"
    )
    await message.answer(formatted_message, parse_mode="HTML")


@router.message(Command('admin'))
async def cmd_admin(message: Message):
    formatted_message = (
        "🛠 <b>Добро пожаловать в админ-панель!</b>\n\n"
        "⚡ Тут ты, скорее всего, проведешь всю оставшуюся жизнь.\n\n"
        "🎛 <b>Работаем с кнопочками</b>\n"
        "⚠️ <b>Перед работой читаем документацию:</b> /admin_docs\n"
        "💻 <b>Для работы с командами:</b> /admin_commands"
    )

    await message.answer(formatted_message, parse_mode="HTML", reply_markup=get_test_keyboard())
