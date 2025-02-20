from aiogram import Router
from aiogram.types import Message

import re

# фильтры
from aiogram.filters import Command
from aiogram import F

# состояния
from aiogram.fsm.context import FSMContext
from states import (
    GetMonitorAccountByUserID,
    GetMonitorAccountByPK,
    AddMonitorAccount,
    EditMonitorAccountByPK,
    EditMonitorAccountByUserID,
    DeleteMonitorAccountByPK,
    DeleteMonitorAccountByUserID,
    AuthMonitorAccountByPK,
)

# клавиатуры
from keyboards.reply_kb import (
    get_admin_panel_keyboard
)
from keyboards.inline_kb import (
    MonitorAccountsKeyboard,
    MonitorSettingsKeyboard,
    MonitoredAccountsKeyboard,
    AdditionalFunctionsKeyboard
)

# сервисы
from services.api_services.seeonline_api import SeeOnlineAPI

# конфиг
from config import load_config

config = load_config()

router = Router()


# ----------------COMMANDS----------------

@router.message(Command('admin'))
async def cmd_admin(message: Message):
    formatted_message = (
        "🛠 <b>Добро пожаловать в админ-панель!</b>\n\n"
        "⚡ Тут ты, скорее всего, проведешь всю оставшуюся жизнь.\n\n"
        "🎛 <b>Работаем с кнопочками</b>\n\n"
        "⚠️ <b>Перед работой читаем документацию:</b>\n/admin_docs\n"
        "💻 <b>Для работы с командами:</b>\n/admin_commands"
    )

    await message.answer(formatted_message, parse_mode="HTML", reply_markup=get_admin_panel_keyboard())


@router.message(Command('admin_commands'))
async def cmd_admin_commands(message: Message):
    formatted_message = (
        "⚡ <b>Команды:</b>\n\n"

        "👨‍💻 <b>Функции рядовых админов:</b>\n\n"

        "‍💻 <b>Мониторинг-аккаунты</b>\n"
        "📡 Получение мониторинг-аккаунтов - /get_monitors\n"
        "➕ Добавление мониторинг-аккаунта - /set_monitor\n"
        "✏️ Изменение мониторинг-аккаунта - /edit_monitor\n"
        "❌ Удаление мониторинг-аккаунта - /delete_monitor\n\n"

        "⚙️ <b>Настройки мониторинг-аккаунтов:</b>\n"
        "🔍 Получение настроек - /get_monitor_settings\n"
        "➕ Добавление настроек - /set_monitor_settings\n"
        "✏️ Изменение настроек - /edit_monitor_settings\n"
        "❌ Удаление настроек - /delete_monitor_settings\n\n"

        "📊 <b>Отслеживаемые аккаунты:</b>\n"
        "👀 Получение отслеживаемых аккаунтов - /get_monitored_accounts\n"
        "➕ Добавление отслеживаемого аккаунта - /set_monitored_accounts\n"
        "✏️ Изменение отслеживаемого аккаунта - /edit_monitored_accounts\n"
        "❌ Удаление отслеживаемого аккаунта - /delete_monitored_account\n"
        "⏳ Получение периода онлайна - /get_online_period\n"
        "🔑 Авторизация мониторинг-аккаунта - /auth_monitor\n\n"

        "👑 <b>Функции высших админов:</b>\n\n"

        "🛠 <b>String сессии:</b>\n"
        "🔓 Получение session_string - /get_session_string\n"
        "➕ Добавление session_string - /set_session_string\n"
        "✏️ Изменение session_string - /edit_session_string\n"
        "❌ Удаление session_string - /delete_session_string\n\n"

        "📜 <b>Дополнительно:</b>\n"
        "📖 Краткое руководство по параметрам команд — /admin_commands_docs"
    )

    await message.answer(formatted_message, parse_mode="HTML")


# ----------------TEXT----------------

@router.message(F.text == "📡 Монитор-аккаунты")
async def monitor_accounts_menu(message: Message):
    formatted_message = (
        "📡 <b>Монитор-аккаунты</b>\n\n"
        "✨ <b>Возможности:</b>\n"
        "🔹 Получить монитор-аккаунты\n"
        "🔹 Добавить новые аккаунты для мониторинга\n"
        "🔹 Изменить данные существующих монитор-аккаунтов\n"
        "🔹 Удалить ненужные аккаунты\n"
        "🔹 Авторизовать аккаунты\n\n"
        "⚠️ Все действия выполняются через инлайн-клавиатуру ниже\n\n"
        "⚙️ Если есть желание попу рвать то можешь попробовать команды\n /admin_commands"
    )

    await message.answer(formatted_message, parse_mode="HTML")
    await message.answer('Выберите действие:', reply_markup=MonitorAccountsKeyboard.get_keyboard('main'))


@router.message(F.text == "👀 Отслеживаемые аккаунты")
async def monitored_accounts_menu(message: Message):
    formatted_message = (
        "👀 <b>Отслеживаемые аккаунты</b>\n\n"
        "✨ <b>Возможности:</b>\n"
        "🔹 Получить отслеживаемые аккаунты\n"
        "🔹 Добавить новые аккаунты в список отслеживаемых\n"
        "🔹 Изменять отслеживаемые аккаунта\n"
        "🔹 Удалить аккаунты из списка отслеживаемых\n"
        "⚠️ Все действия выполняются через инлайн-клавиатуру ниже\n\n"
        "⚙️ Если есть желание попу рвать то можешь попробовать команды\n /admin_commands"
    )

    await message.answer(formatted_message, parse_mode="HTML")
    await message.answer('Выберите действие:', reply_markup=MonitoredAccountsKeyboard.get_keyboard('main'))


@router.message(F.text == "⚙️ Настройки монитор-аккаунтов")
async def monitor_settings_menu(message: Message):
    formatted_message = (
        "⚙️ <b>Настройки монитор-аккаунтов</b>\n\n"
        "✨ <b>Возможности:</b>\n"
        "🔹 Получить текущие настройки\n"
        "🔹 Добавить новые параметры настроек\n"
        "🔹 Изменить существующие настройки\n"
        "🔹 Удалить ненужные настройки\n\n"
        "⚠️ Все действия выполняются через инлайн-клавиатуру ниже\n\n"
        "⚙️ Если есть желание попу рвать то можешь попробовать команды\n /admin_commands"
    )

    await message.answer(formatted_message, parse_mode="HTML")
    await message.answer('Выберите действие:', reply_markup=MonitorSettingsKeyboard.get_keyboard('main'))


@router.message(F.text == "🛠 Доп. функции")
async def additional_functions_menu(message: Message):
    formatted_message = (
        "🛠 <b>Дополнительные функции</b>\n\n"
        "✨ <b>Возможности:</b>\n"
        "🔹 Проверить системную информацию\n"
        "🔹 Получить метрики\n"
        "⚠️ Все действия выполняются через инлайн-клавиатуру ниже\n\n"
        "⚙️ Если есть желание попу рвать то можешь попробовать команды\n /admin_commands"
    )
    await message.answer(formatted_message, parse_mode="HTML")
    await message.answer('Выберите действие:', reply_markup=AdditionalFunctionsKeyboard.get_keyboard('main'))


@router.message(F.text == "❌ Отменить")
async def additional_functions_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Отменено", reply_markup=get_admin_panel_keyboard())


# ----------------STATES----------------
# ------------Monitor Accounts------------
# --------GET--------
@router.message(GetMonitorAccountByPK.waiting_for_pk)
async def process_get_monitor_account_by_pk(message: Message, state: FSMContext):
    api = SeeOnlineAPI(config.SEEONLINE_API_URL)

    try:
        pk = int(message.text)
    except ValueError:
        await message.answer("❌ Введите корректный ID (число)")
        return

    try:
        account = await api.get_monitor_account(pk=pk)
    except ValueError:
        await message.answer("📭 Аккаунт с таким ID не найден")
        return

    response = (
        f"🔹 <b>ID:</b> {account['id']}\n"
        f"👤 <b>User ID:</b> <code>{account['user_id']}</code>\n"
        f"🆔 <b>API ID:</b> <code>{account['api_id']}</code>\n"
        f"🔑 <b>API Hash:</b> <code>{account['api_hash']}</code>\n"
        f"✅ <b>Активен:</b> {'Да' if account['is_active'] else 'Нет'}\n"
        f"🔐 <b>Авторизован:</b> {'Да' if account['is_auth'] else 'Нет'}\n"
        f"🕒 <b>Создан:</b> {account['created_at']}\n"
        f"🔄 <b>Обновлён:</b> {account['updates_at']}\n"
    )
    await message.answer(response, parse_mode="HTML", reply_markup=get_admin_panel_keyboard())

    await state.clear()


@router.message(GetMonitorAccountByUserID.waiting_for_user_id)
async def process_get_monitor_account_by_pk(message: Message, state: FSMContext):
    api = SeeOnlineAPI(config.SEEONLINE_API_URL)

    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer("❌ Введите корректный UserID (число)")
        return

    try:
        account = await api.get_monitor_account(user_id=user_id)
    except ValueError:
        await message.answer("📭 Аккаунт с таким ID не найден")
        return

    response = (
        f"🔹 <b>ID:</b> {account['id']}\n"
        f"👤 <b>User ID:</b> <code>{account['user_id']}</code>\n"
        f"🆔 <b>API ID:</b> <code>{account['api_id']}</code>\n"
        f"🔑 <b>API Hash:</b> <code>{account['api_hash']}</code>\n"
        f"✅ <b>Активен:</b> {'Да' if account['is_active'] else 'Нет'}\n"
        f"🔐 <b>Авторизован:</b> {'Да' if account['is_auth'] else 'Нет'}\n"
        f"🕒 <b>Создан:</b> {account['created_at']}\n"
        f"🔄 <b>Обновлён:</b> {account['updates_at']}\n"
    )
    await message.answer(response, parse_mode="HTML", reply_markup=get_admin_panel_keyboard())

    await state.clear()


# --------ADD--------
@router.message(AddMonitorAccount.waiting_for_form)
async def process_add_monitor_account(message: Message, state: FSMContext):
    api = SeeOnlineAPI(config.SEEONLINE_API_URL)

    lines = message.text.strip().split("\n")

    if len(lines) != 3:
        await message.answer("❌ Данные строго по шаблону в 3 строки\n(User_ID, Api_ID, Api_Hash)")
        return

    user_id, api_id, api_hash = lines

    if not user_id.isdigit():
        await message.answer("❌ User_ID должен содержать только цифры")
        return

    if not api_id.isdigit():
        await message.answer("❌ Api_ID должен содержать только цифры")
        return

    # todo в проде убрать \d+| тк для удобства разработки
    if not re.fullmatch(r"\d+|[a-fA-F0-9]{32}", api_hash):
        await message.answer("❌ Api_Hash должен быть 32-значным хэшем.")
        return

    data = {
        "user_id": int(user_id),
        "api_id": int(api_id),
        "api_hash": api_hash
    }

    success = await api.create_monitor_account(data)

    if success:
        await message.answer("✅ Монитор-аккаунт успешно добавлен!")
    else:
        await message.answer("❌ Ошибка при добавлении аккаунта. Попробуйте позже.")

    await state.clear()


# --------EDIT--------
# todo тут все переебашить нахуй, копипаста полная

# Изменение по PK
@router.message(EditMonitorAccountByPK.waiting_for_pk)
async def process_edit_monitor_account_by_pk(message: Message, state: FSMContext):
    api = SeeOnlineAPI(config.SEEONLINE_API_URL)

    try:
        pk = int(message.text)
    except ValueError:
        await message.answer("❌ Введите корректный ID (число)")
        return

    try:
        account = await api.get_monitor_account(pk=pk)
    except ValueError:
        await message.answer("📭 Аккаунт с таким ID не найден")
        return

    formatted_message = (
        "✅ <b>Аккаунт найден</b>\n\n"
        f"🔹 <b>ID:</b> {account['id']}\n"
        f"👤 <b>User ID:</b> <code>{account['user_id']}</code>\n"
        f"🆔 <b>API ID:</b> <code>{account['api_id']}</code>\n"
        f"🔑 <b>API Hash:</b> <code>{account['api_hash']}</code>\n"
        f"✅ <b>Активен:</b> {'Да' if account['is_active'] else 'Нет'}\n"
        f"🔐 <b>Авторизован:</b> {'Да' if account['is_auth'] else 'Нет'}\n"
        f"🕒 <b>Создан:</b> {account['created_at']}\n"
        f"🔄 <b>Обновлён:</b> {account['updates_at']}\n\n"
        "✏️ <b>Введи новые данные. Можно изменить одно или несколько полей:</b>\n"
        "<b>Формат:</b>\n"
        "<code>user_id=1234567890</code>\n"
        "<code>api_id=12345678</code>\n"
        "<code>api_hash=abcdef1234567890abcdef1234567890</code>\n"
        "<code>is_active=1</code>\n"
        "<code>is_auth=0</code>\n\n"
        "⚠️ Если поле не нужно менять, просто пропусти его."
    )

    await message.answer(formatted_message, parse_mode="HTML")

    await state.update_data(pk=pk)
    await state.set_state(EditMonitorAccountByPK.waiting_for_form)


@router.message(EditMonitorAccountByPK.waiting_for_form)
async def process_edit_monitor_account_by_pk_form(message: Message, state: FSMContext):
    stored_data = await state.get_data()
    pk = stored_data.get("pk")

    if not pk:
        await message.answer("❌ В состоянии не найден 'pk'. Операция прервана", reply_markup=get_admin_panel_keyboard())
        await state.clear()
        return

    api = SeeOnlineAPI(config.SEEONLINE_API_URL)
    lines = message.text.strip().split("\n")

    valid_fields = {"user_id", "api_id", "api_hash", "is_active", "is_auth"}
    update_data = {}

    for line in lines:
        if "=" not in line:
            await message.answer(f"❌ Строка '{line}' не соответствует формату key=value")
            return

        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()

        if key not in valid_fields:
            await message.answer(f"❌ Поле '{key}' нельзя изменить")
            return

        if key in ["user_id", "api_id"]:
            if not value.isdigit():
                await message.answer(f"❌ {key} должен содержать только цифры")
                return
            update_data[key] = int(value)

        elif key == "api_hash":
            if not re.fullmatch(r"\d+|[a-fA-F0-9]{32}", value):
                await message.answer("❌ api_hash должен быть 32-значным шестнадцатеричным хэшем")
                return
            update_data[key] = value

        elif key in ["is_active", "is_auth"]:
            if value not in {"0", "1"}:
                await message.answer(f"❌ {key} может быть только '0' (Нет) или '1' (Да)")
                return
            update_data[key] = bool(int(value))

    if not update_data:
        await message.answer("⚠️ Не указано ни одного корректного параметра для обновления")
        return

    try:
        response = await api.update_monitor_account(update_data, pk=pk)
    except ValueError as e:
        await message.answer(f"❌ Ошибка при обновлении аккаунта: {e}", reply_markup=get_admin_panel_keyboard())
        await state.clear()
        return

    formatted_message = (
        f"✅ <b>Аккаунт успешно обновлён</b>\n\n"
        f"🔹 <b>ID:</b> {response['id']}\n"
        f"👤 <b>User ID:</b> <code>{response['user_id']}</code>\n"
        f"🆔 <b>API ID:</b> <code>{response['api_id']}</code>\n"
        f"🔑 <b>API Hash:</b> <code>{response['api_hash']}</code>\n"
        f"✅ <b>Активен:</b> {'Да' if response['is_active'] else 'Нет'}\n"
        f"🔐 <b>Авторизован:</b> {'Да' if response['is_auth'] else 'Нет'}\n"
        f"🕒 <b>Создан:</b> {response['created_at']}\n"
        f"🔄 <b>Обновлён:</b> {response['updates_at']}"
    )

    await message.answer(formatted_message, parse_mode="HTML", reply_markup=get_admin_panel_keyboard())

    await state.clear()


# Изменение по user_id
@router.message(EditMonitorAccountByUserID.waiting_for_user_id)
async def process_edit_monitor_account_by_user_id(message: Message, state: FSMContext):
    api = SeeOnlineAPI(config.SEEONLINE_API_URL)

    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Введите корректный User ID (число)")
        return

    try:
        account = await api.get_monitor_account(user_id=user_id)
    except ValueError:
        await message.answer("📭 Аккаунт с таким user_id не найден")
        return

    formatted_message = (
        "✅ <b>Аккаунт найден</b>\n\n"
        f"🔹 <b>ID:</b> {account['id']}\n"
        f"👤 <b>User ID:</b> <code>{account['user_id']}</code>\n"
        f"🆔 <b>API ID:</b> <code>{account['api_id']}</code>\n"
        f"🔑 <b>API Hash:</b> <code>{account['api_hash']}</code>\n"
        f"✅ <b>Активен:</b> {'Да' if account['is_active'] else 'Нет'}\n"
        f"🔐 <b>Авторизован:</b> {'Да' if account['is_auth'] else 'Нет'}\n"
        f"🕒 <b>Создан:</b> {account['created_at']}\n"
        f"🔄 <b>Обновлён:</b> {account['updates_at']}\n\n"
        "✏️ <b>Введи новые данные. Можно изменить одно или несколько полей:</b>\n"
        "<b>Формат:</b>\n"
        "<code>user_id=1234567890</code>\n"
        "<code>api_id=12345678</code>\n"
        "<code>api_hash=abcdef1234567890abcdef1234567890</code>\n"
        "<code>is_active=1</code>\n"
        "<code>is_auth=0</code>\n\n"
        "⚠️ Если поле не нужно менять, просто пропусти его"
    )
    await message.answer(formatted_message, parse_mode="HTML")

    await state.update_data(user_id=user_id)

    await state.set_state(EditMonitorAccountByUserID.waiting_for_form)


@router.message(EditMonitorAccountByUserID.waiting_for_form)
async def process_edit_monitor_account_by_user_id_form(message: Message, state: FSMContext):
    stored_data = await state.get_data()
    user_id = stored_data.get("user_id")

    if not user_id:
        await message.answer("❌ Не найден user_id в состоянии. Операция прервана")
        await state.clear()
        return

    api = SeeOnlineAPI(config.SEEONLINE_API_URL)

    lines = message.text.strip().split("\n")

    valid_fields = {"user_id", "api_id", "api_hash", "is_active", "is_auth"}
    update_data = {}

    for line in lines:
        if "=" not in line:
            await message.answer(f"❌ Строка '{line}' не соответствует формату key=value")
            return

        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()

        if key not in valid_fields:
            await message.answer(f"❌ Поле '{key}' нельзя изменить")
            return

        if key in ["user_id", "api_id"]:
            if not value.isdigit():
                await message.answer(f"❌ {key} должен содержать только цифры")
                return
            update_data[key] = int(value)

        elif key == "api_hash":
            if not re.fullmatch(r"\d+|[a-fA-F0-9]{32}", value):
                await message.answer("❌ api_hash должен быть 32-значным шестнадцатеричным хэшем")
                return
            update_data[key] = value

        elif key in ["is_active", "is_auth"]:
            if value not in {"0", "1"}:
                await message.answer(f"❌ {key} может быть только '0' (Нет) или '1' (Да)")
                return
            update_data[key] = bool(int(value))

    if not update_data:
        await message.answer("⚠️ Не указано ни одного корректного параметра для обновления")
        return

    try:
        response = await api.update_monitor_account(update_data, pk=None, user_id=user_id)
    except ValueError as e:
        await message.answer(f"❌ Ошибка при обновлении аккаунта: {e}", reply_markup=get_admin_panel_keyboard())
        await state.clear()
        return

    formatted_message = (
        f"✅ <b>Аккаунт успешно обновлён</b>\n\n"
        f"🔹 <b>ID:</b> {response['id']}\n"
        f"👤 <b>User ID:</b> <code>{response['user_id']}</code>\n"
        f"🆔 <b>API ID:</b> <code>{response['api_id']}</code>\n"
        f"🔑 <b>API Hash:</b> <code>{response['api_hash']}</code>\n"
        f"✅ <b>Активен:</b> {'Да' if response['is_active'] else 'Нет'}\n"
        f"🔐 <b>Авторизован:</b> {'Да' if response['is_auth'] else 'Нет'}\n"
        f"🕒 <b>Создан:</b> {response['created_at']}\n"
        f"🔄 <b>Обновлён:</b> {response['updates_at']}"
    )

    await message.answer(formatted_message, parse_mode="HTML", reply_markup=get_admin_panel_keyboard())
    await state.clear()


# --------DELETE--------

@router.message(DeleteMonitorAccountByPK.waiting_for_pk)
async def process_delete_monitor_account_by_pk(message: Message, state: FSMContext):
    api = SeeOnlineAPI(config.SEEONLINE_API_URL)

    try:
        pk = int(message.text)
    except ValueError:
        await message.answer("❌ Введите корректный ID (число)")
        return

    try:
        await api.delete_monitor_account(pk=pk)
    except ValueError:
        await message.answer("📭 Аккаунт с таким ID не найден")
        return

    await message.answer("✅ Аккаунт удален", parse_mode="HTML", reply_markup=get_admin_panel_keyboard())

    await state.clear()


@router.message(DeleteMonitorAccountByUserID.waiting_for_user_id)
async def process_delete_monitor_account_by_user_id(message: Message, state: FSMContext):
    api = SeeOnlineAPI(config.SEEONLINE_API_URL)

    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer("❌ Введите корректный UserID (число)")
        return

    try:
        await api.delete_monitor_account(user_id=user_id)
    except ValueError:
        await message.answer("📭 Аккаунт с таким ID не найден")
        return

    await message.answer("✅ Аккаунт удален", parse_mode="HTML", reply_markup=get_admin_panel_keyboard())

    await state.clear()


# --------AUTH--------

# todo перепилить ебаную авторизацию

@router.message(AuthMonitorAccountByPK.waiting_for_pk)
async def process_auth_monitor_account_by_pk(message: Message, state: FSMContext):
    pass
    # api = SeeOnlineAPI(config.SEEONLINE_API_URL)
    #
    # try:
    #     pk = int(message.text)
    # except ValueError:
    #     await message.answer("❌ Введите корректный ID (число)")
    #     return
    #
    # try:
    #     auth_data = await api.start_auth_monitor_account(pk=pk)
    # except ValueError as e:
    #     await message.answer(f"❌ Не удалось начать авторизацию: {e}", reply_markup=get_admin_panel_keyboard())
    #     await state.clear()
    #     return
    #
    # await state.update_data(
    #     phone_number=auth_data["phone_number"],
    #     phone_code_hash=auth_data["phone_code_hash"],
    #     api_id=auth_data["api_id"],
    #     api_hash=auth_data["api_hash"],
    #     monitor_id=auth_data["monitor_id"]
    # )
    #
    # await message.answer(
    #     f"Код отправлен на номер <b>{auth_data['phone_number']}</b>\n"
    #     f"Введите код из Telegram/SMS:",
    #     parse_mode="HTML"
    # )
    #
    # await state.set_state(AuthMonitorAccountByPK.waiting_for_code)


# todo допилить блять заебали

@router.message(AuthMonitorAccountByPK.waiting_for_code)
async def process_auth_monitor_account_by_pk_code(message: Message, state: FSMContext):
    pass
    # api = SeeOnlineAPI(config.SEEONLINE_API_URL)
    # code = message.text.strip()
    #
    # data = await state.get_data()
    #
    # phone_number = data.get("phone_number")
    # phone_code_hash = data.get("phone_code_hash")
    # api_id = data.get("api_id")
    # api_hash = data.get("api_hash")
    # monitor_id = data.get("monitor_id")
    # temp_sesion = data.get("temp_sesion")
    #
    # if not all([phone_number, phone_code_hash, api_id, api_hash, monitor_id]):
    #     await message.answer("❌ Не хватает данных для авторизации. Операция прервана",
    #                          reply_markup=get_admin_panel_keyboard())
    #     await state.clear()
    #     return
    #
    # try:
    #     session_str = await api.complete_auth_monitor_account(
    #         code=code,
    #         phone_number=phone_number,
    #         phone_code_hash=phone_code_hash,
    #         api_id=api_id,
    #         api_hash=api_hash,
    #         monitor_id=monitor_id,
    #         temp_session=temp_sesion
    #     )
    # except ValueError as e:
    #     await message.answer(f"❌ Ошибка авторизации: {e}", reply_markup=get_admin_panel_keyboard())
    #     await state.clear()
    #     return
    #
    # await message.answer(f"✅ Аккаунт успешно авторизован!\n {session_str}", reply_markup=get_admin_panel_keyboard())
    #
    # await state.clear()
