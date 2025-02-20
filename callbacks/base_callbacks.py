from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F

# клавиатуры
from keyboards.inline_kb import MonitorAccountsKeyboard

router = Router()


# ----------------MAIN----------------
@router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):
    await callback.answer(
        text="Ты долбаеб?",
        show_alert=False
    )


# ----------------Monitor Accounts-----------------

# кнопочка возвращения, общая для всех действий monitor-accounts
@router.callback_query(F.data == "back-monitor-accounts")
async def back_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text('Выберите действие:', reply_markup=MonitorAccountsKeyboard.get_keyboard('main'))
