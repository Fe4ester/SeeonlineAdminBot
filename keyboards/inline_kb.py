from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_inline_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    # Каждая кнопка обычно содержит callback_data или URL
    kb_builder.row(
        InlineKeyboardButton(
            text="Кнопка A",
            callback_data="buttonA"
        ),
        InlineKeyboardButton(
            text="Кнопка B",
            callback_data="buttonB"
        )
    )
    return kb_builder.as_markup()
