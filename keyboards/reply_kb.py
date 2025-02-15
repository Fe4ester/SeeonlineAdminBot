from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_test_keyboard() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.row(
        KeyboardButton(text="Монитор аккаунты"),
        KeyboardButton(text="Мониторинг аккаунты"),
    )
    kb_builder.row(
        KeyboardButton(text="Настройка монитор аккаунтов"),
        KeyboardButton(text="Кнопка 4"),
    )

    return kb_builder.as_markup(resize_keyboard=True)
