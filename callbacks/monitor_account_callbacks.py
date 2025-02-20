# базовые иморты для бота
from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext

# состояния
from states import (
    GetMonitorAccountByPK,
    GetMonitorAccountByUserID,
    AddMonitorAccount,
    EditMonitorAccountByPK,
    EditMonitorAccountByUserID,
    DeleteMonitorAccountByPK,
    DeleteMonitorAccountByUserID,
)

# клавиатуры
from keyboards.inline_kb import MonitorAccountsKeyboard
from keyboards.reply_kb import (
    get_cancel_keyboard
)

# сервисы
from services.pagination import show_monitor_accounts_page

# конфиг
from config import load_config

router = Router()

config = load_config()


# обработка состояний в handlers.admin_panel STATES!!!!


# ----------------MAIN----------------

@router.callback_query(F.data == "get-monitor-accounts")
async def get_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Выберите способ получения:',
        reply_markup=MonitorAccountsKeyboard().get_keyboard('get')
    )


# тут без доп клавиатуры тк добавление по форме сразу без доп данных
@router.callback_query(F.data == "add-monitor-accounts")
async def add_monitor_accounts_callback(callback: CallbackQuery, state: FSMContext):
    formatted_message = (
        "📝 <b>Добавление монитор-аккаунта</b>\n\n"
        "🔹 Введи данные по следующей форме:\n"
        "⚠️ <b>То что в скобках писать не надо, чисто данные</b>\n\n"
        "<code>1234567890</code>(<del>User_ID:</del>)\n"
        "<code>12345678</code>(<del>Api_ID:</del>)\n"
        "<code>1234567890abcdef1234567890abcdef</code>(<del>Api_Hash:</del>)`\n\n"
        "⚠️ <b>Внимательно, пожалуйста!</b> Если что-то сломаешь — "
        "по ебалу точно отхватишь"
    )

    await callback.message.answer(formatted_message, parse_mode="HTML", reply_markup=get_cancel_keyboard())
    await state.set_state(AddMonitorAccount.waiting_for_form)
    await callback.answer()


@router.callback_query(F.data == "edit-monitor-accounts")
async def edit_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Выберите способ изменения:',
        reply_markup=MonitorAccountsKeyboard().get_keyboard('edit')
    )


@router.callback_query(F.data == "delete-monitor-accounts")
async def delete_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Выберите способ удаления:',
        reply_markup=MonitorAccountsKeyboard().get_keyboard('delete')
    )


# todo допилить
@router.callback_query(F.data == "auth-monitor-accounts")
async def auth_monitor_accounts_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        'Текущий callback:\n auth-monitor-accounts',
        reply_markup=MonitorAccountsKeyboard.get_keyboard('main')
    )
    await callback.answer()


# ----------------GET---------------

# todo убрать кеширование и перенести его на уровень приложения
# ---- с пагинацией, не путаться ----
@router.callback_query(F.data == "get-list-monitor-accounts")
async def get_list_monitor_accounts_callback(callback: CallbackQuery):
    TTL = 120
    PAGE_SIZE = 4

    page = 1
    await show_monitor_accounts_page(
        callback=callback,
        page=page,
        page_size=PAGE_SIZE,
        ttl=TTL,
        edit=False
    )


# ---- с пагинацией 2 ----
@router.callback_query(lambda c: c.data.startswith("monitor_accounts_page:"))
async def paginate_monitor_accounts_callback(callback: CallbackQuery):
    _, page_str = callback.data.split(":")
    try:
        page = int(page_str)
    except ValueError:
        page = 1

    TTL = 120
    PAGE_SIZE = 4
    await show_monitor_accounts_page(
        callback=callback,
        page=page,
        page_size=PAGE_SIZE,
        ttl=TTL,
        edit=True
    )


@router.callback_query(F.data == "get-monitor-account-by-pk")
async def get_monitor_account_by_pk_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔍 Введите ID (PK) аккаунта для поиска:", reply_markup=get_cancel_keyboard())
    await state.set_state(GetMonitorAccountByPK.waiting_for_pk)
    await callback.answer()


@router.callback_query(F.data == "get-monitor-account-by-user_id")
async def get_monitor_account_by_user_id_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔍 Введите UserID аккаунта для поиска:", reply_markup=get_cancel_keyboard())
    await state.set_state(GetMonitorAccountByUserID.waiting_for_user_id)
    await callback.answer()


# ----------------EDIT----------------

@router.callback_query(F.data == "edit-monitor-account-by-pk")
async def edit_monitor_account_by_pk_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔍 Введите ID (PK) аккаунта для изменения:", reply_markup=get_cancel_keyboard())
    await state.set_state(EditMonitorAccountByPK.waiting_for_pk)
    await callback.answer()


@router.callback_query(F.data == "edit-monitor-account-by-user_id")
async def edit_monitor_account_by_user_id_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔍 Введите UserID аккаунта для изменения:", reply_markup=get_cancel_keyboard())
    await state.set_state(EditMonitorAccountByUserID.waiting_for_user_id)
    await callback.answer()


# ----------------DELETE---------------

@router.callback_query(F.data == "delete-monitor-account-by-pk")
async def delete_monitor_account_by_pk_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔍 Введите ID (PK) аккаунта для удаления:", reply_markup=get_cancel_keyboard())
    await state.set_state(DeleteMonitorAccountByPK.waiting_for_pk)
    await callback.answer()


@router.callback_query(F.data == "delete-monitor-account-by-user_id")
async def delete_monitor_account_by_user_id_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔍 Введите UserID аккаунта для удаления:", reply_markup=get_cancel_keyboard())
    await state.set_state(DeleteMonitorAccountByUserID.waiting_for_user_id)
    await callback.answer()
