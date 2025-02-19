from aiogram import Router
from aiogram.types import Message

# фильтры
from aiogram.filters import Command
from aiogram import F

# клавиатуры
from keyboards.reply_kb import get_admin_panel_keyboard
from keyboards.inline_kb import (
    get_monitor_accounts_inline_keyboard,
    get_monitored_accounts_inline_keyboard,
    get_monitor_settings_inline_keyboard,
    get_additional_functions_inline_keyboard
)

router = Router()


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
    await message.answer('Выберите действие:', reply_markup=get_monitor_accounts_inline_keyboard())


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
    await message.answer('Выберите действие:', reply_markup=get_monitored_accounts_inline_keyboard())


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
    await message.answer('Выберите действие:', reply_markup=get_monitor_settings_inline_keyboard())


@router.message(F.text == "🛠 Доп. функции")
async def additional_functions_menu(message: Message):
    formatted_message = (
        "🛠 <b>Дополнительные функции</b>\n\n"
        "✨ <b>Возможности:</b>\n"
        "🔹 Проверить системную информацию\n"
        "🔹 Получить метрики\n"
        "🔹 Авторизовать монитор-аккаунты\n\n"
        "⚠️ Все действия выполняются через инлайн-клавиатуру ниже\n\n"
        "⚙️ Если есть желание попу рвать то можешь попробовать команды\n /admin_commands"
    )
    await message.answer(formatted_message, parse_mode="HTML")
    await message.answer('Выберите действие:', reply_markup=get_additional_functions_inline_keyboard())


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
