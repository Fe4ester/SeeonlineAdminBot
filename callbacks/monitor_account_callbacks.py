from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

import json

from keyboards.inline_kb import MonitorAccountsKeyboard

from services.seeonline_api import SeeOnlineAPI

from config import load_config

router = Router()

config = load_config()


# MAIN

@router.callback_query(F.data == "get-monitor-accounts")
async def get_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Выберите способ получения:',
        reply_markup=MonitorAccountsKeyboard().get_keyboard('get')
    )


# todo допилить
@router.callback_query(F.data == "add-monitor-accounts")
async def add_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n add-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


# todo допилить
@router.callback_query(F.data == "edit-monitor-accounts")
async def edit_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n edit-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


# todo допилить
@router.callback_query(F.data == "delete-monitor-accounts")
async def delete_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n delete-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


# todo допилить
@router.callback_query(F.data == "auth-monitor-accounts")
async def auth_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n auth-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


# GET

# todo добавить пагинацию для аккаунтов
@router.callback_query(F.data == "get-list-monitor-accounts")
async def get_list_monitor_accounts_callback(callback: CallbackQuery):
    api = SeeOnlineAPI(config.SEEONLINE_API_URL)

    monitor_accounts = await api.get_monitor_account()

    if not monitor_accounts:
        await callback.message.answer("📭 Список мониторинга пуст.")
        return await callback.answer()

    response = "📋 <b>Список мониторинговых аккаунтов:</b>\n\n"

    for account in monitor_accounts:
        response += (
            f"🔹 <b>ID:</b> {account['id']}\n"
            f"👤 <b>User ID:</b> <code>{account['user_id']}</code>\n"
            f"🆔 <b>API ID:</b> <code>{account['api_id']}</code>\n"
            f"🔑 <b>API Hash:</b> <code>{account['api_hash']}</code>\n"
            f"✅ <b>Активен:</b> {'Да' if account['is_active'] else 'Нет'}\n"
            f"🔐 <b>Авторизован:</b> {'Да' if account['is_auth'] else 'Нет'}\n"
            f"🕒 <b>Создан:</b> {account['created_at']}\n"
            f"🔄 <b>Обновлён:</b> {account['updates_at']}\n"
            f"────────────────────────\n"
        )

    await callback.message.answer(response, parse_mode="HTML")
    await callback.answer()


# todo добавить конечные состояния(fsm)
@router.callback_query(F.data == "get-monitor-account-by-pk")
async def get_monitor_account_by_pk_callback(callback: CallbackQuery):
    pass


@router.callback_query(F.data == "get-monitor-account-by-user_id")
async def get_monitor_account_by_user_id_callback(callback: CallbackQuery):
    pass
