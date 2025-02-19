from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

from keyboards.inline_kb import MonitoredAccountsKeyboard

router = Router()


@router.callback_query(F.data == "get-monitored-accounts")
async def get_monitored_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n get-monitored-accounts",
        reply_markup=MonitoredAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "add-monitored-accounts")
async def add_monitored_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n add-monitored-accounts",
        reply_markup=MonitoredAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "edit-monitored-accounts")
async def edit_monitored_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n edit-monitored-accounts",
        reply_markup=MonitoredAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


@router.callback_query(F.data == "delete-monitored-accounts")
async def delete_monitored_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Текущий callback:\n delete-monitored-accounts",
        reply_markup=MonitoredAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()
