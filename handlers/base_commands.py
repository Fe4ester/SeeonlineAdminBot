from aiogram import Router
from aiogram.types import Message

from aiogram.filters import Command

router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer("Привет, админ епта\nБольше инфы по функционалу - /help")

@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer("""
Ну чо епта, пробежимся по функционалу
/smsbower - работа с API SmsBower
А больше нихуя нет так что иди нахуй
""")