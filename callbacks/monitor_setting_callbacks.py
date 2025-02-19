from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

from keyboards.inline_kb import MonitorSettingsKeyboard

router = Router()


@router.callback_query(F.data == "get-monitor-settings")
async def get_monitor_settings_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n get-monitor-settings",
        reply_markup=MonitorSettingsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "add-monitor-settings")
async def add_monitor_settings_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n add-monitor-settings",
        reply_markup=MonitorSettingsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "edit-monitor-settings")
async def edit_monitor_settings_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n edit-monitor-settings",
        reply_markup=MonitorSettingsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "delete-monitor-settings")
async def delete_monitor_settings_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n delete-monitor-settings",
        reply_markup=MonitorSettingsKeyboard.get_keyboard('main')
    )
    await callback.answer()
