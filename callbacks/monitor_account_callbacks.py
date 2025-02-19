from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

from keyboards.inline_kb import MonitorAccountsKeyboard

router = Router()


@router.callback_query(F.data == "get-monitor-accounts")
async def get_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n get-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard().get_keyboard('main')
    )


@router.callback_query(F.data == "add-monitor-accounts")
async def add_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n add-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "edit-monitor-accounts")
async def edit_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n edit-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "delete-monitor-accounts")
async def delete_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n delete-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "auth-monitor-accounts")
async def auth_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n auth-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()
