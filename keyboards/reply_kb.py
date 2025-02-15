from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_admin_panel_keyboard() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    # Первый ряд
    kb_builder.row(
        KeyboardButton(text="📡 Монитор-аккаунты"),
        KeyboardButton(text="👀 Отслеживаемые аккаунты")
    )

    # Второй ряд
    kb_builder.row(
        KeyboardButton(text="⚙️ Настройки монитор-аккаунтов"),
        KeyboardButton(text="🛠 Доп. функции")
    )

    return kb_builder.as_markup(resize_keyboard=True)
