from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

router = Router()

@router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):
    await callback.answer(
        text="Ты долбаеб?",
        show_alert=False
    )