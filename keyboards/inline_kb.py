from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_monitor_accounts_inline_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text="Получить аккаунты",
            callback_data="get-monitor-accounts"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Добавить аккаунты",
            callback_data="add-monitor-accounts"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Изменить данные",
            callback_data="edit-monitor-accounts"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Удалить аккаунты",
            callback_data="delete-monitor-accounts"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Авторизовать аккаунты",
            callback_data="auth-monitor-accounts"
        )
    )
    return kb_builder.as_markup()


def get_monitored_accounts_inline_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text="Получить аккаунты",
            callback_data="get-monitored-accounts"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Добавить аккаунты",
            callback_data="add-monitored-accounts"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Изменить аккаунты",
            callback_data="edit-monitored-accounts"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Удалить аккаунты",
            callback_data="delete-monitored-accounts"
        )
    )
    return kb_builder.as_markup()


def get_monitor_settings_inline_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text="Получить настройки",
            callback_data="get-monitor-settings"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Добавить настройки",
            callback_data="add-monitor-settings"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Изменить настройки",
            callback_data="edit-monitor-settings"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Удалить настройки",
            callback_data="delete-monitor-settings"
        )
    )
    return kb_builder.as_markup()


def get_additional_functions_inline_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text="Получить системную информацию",
            callback_data="get-system-info"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Получить метрики",
            callback_data="get-metrics"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text="Авторизовать монитор-аккаунты",
            callback_data="auth-monitor-accounts"
        )
    )
    return kb_builder.as_markup()
