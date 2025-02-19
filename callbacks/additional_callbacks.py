from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

from keyboards.inline_kb import AdditionalFunctionsKeyboard

router = Router()


@router.callback_query(F.data == "get-system-info")
async def get_system_info_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n get-system-info",
        reply_markup=AdditionalFunctionsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "get-metrics")
async def get_metrics_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n get-metrics",
        reply_markup=AdditionalFunctionsKeyboard.get_keyboard('main')
    )
    await callback.answer()
